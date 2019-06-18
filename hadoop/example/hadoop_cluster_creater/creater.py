import os
import time

import docker

YML_HEADER = '''\
version: "{version}"
services:
'''

YML_NODE_FORMAT = '''\
  {node_name}:
    image: {image}
    hostname: {node_name}
    container_name: {node_name}
    volumes:
      - {node_ssh_dir}:/root/.ssh
'''


class Creater(object):

    COMPOSE_YML_NAME = "creater.yml"

    def __init__(self, cluster, compose_dir, ssh_dir, version="3.7", image="hadoop:2.9.2"):
        self.master = cluster["master"]
        self.slaves = cluster["slaves"]
        self.version = version
        self.image = image
        self.compose_dir = compose_dir
        self.ssh_dir = ssh_dir

        self.nodes = [self.master]+self.slaves
        self.compose_yml_path = os.path.join(self.compose_dir, self.COMPOSE_YML_NAME)

    def create_docker_compose(self):
        '''创建集群初始化docker-compose文件'''
        yml_data = ""
        yml_data += YML_HEADER.format(version=self.version)

        for node_name in self.nodes:
            node_ssh_dir = os.path.join(self.ssh_dir, node_name)
            yml_data += YML_NODE_FORMAT.format(image=self.image, node_name=node_name, node_ssh_dir=node_ssh_dir)

        with open(self.compose_yml_path, "w") as f:
            f.write(yml_data)

    def init_ssh(self):
        '''
        初始化SSH配置：设置集群间免密登录
        注意：该方法只用执行一次，一旦创建出密钥文件和授权文件后则不需要再执行
        '''
        # 初次启动集群
        os.system("docker-compose -f {} up -d ".format(self.compose_yml_path))

        client = docker.from_env()
        containers = {node_name:client.containers.get(node_name) for node_name in self.nodes}

        while True:
            for container in containers.values():
                if container.status != "running":
                    break
            else:
                break
            time.sleep(0.001)
        print("集群容器已经全部启动，开始初始化SSH配置，并设置集群间免验证登录")

        # 为每个节点容器创建ssh密钥
        for container in containers.values():
            container.exec_run("ssh-keygen -t rsa -N '' -f /root/.ssh/id_rsa")

        # 由于绑定了数据卷，直接操作本地文件系统，追加授权信息
        # 给主节点添加来自主节点访问的授权
        master_ssh_dir = os.path.join(self.ssh_dir, self.master)
        os.system("cat {} >> {}".format(
            os.path.join(master_ssh_dir, "id_rsa.pub"),
            os.path.join(master_ssh_dir, "authorized_keys"),
        ))

        # 遍历每一个从节点
        for slave_node in self.slaves:
            slave_ssh_dir = os.path.join(self.ssh_dir, slave_node)
            # 给从节点添加来自自己的授权
            os.system("cat {} >> {}".format(
                os.path.join(slave_ssh_dir, "id_rsa.pub"),
                os.path.join(slave_ssh_dir, "authorized_keys"),
            ))
            # 给Master添加来自从节点访问的授权
            os.system("cat {} >> {}".format(
                os.path.join(slave_ssh_dir, "id_rsa.pub"),
                os.path.join(master_ssh_dir, "authorized_keys"),
            ))
            # 给从节点添加来自Master访问的授权
            os.system("cat {} >> {}".format(
                os.path.join(master_ssh_dir, "id_rsa.pub"),
                os.path.join(slave_ssh_dir, "authorized_keys"),
            ))
            # 修改权限
            os.system("chmod 600 {}".format(os.path.join(slave_ssh_dir, "authorized_keys")))
        # 修改权限
        os.system("chmod 600 {}".format(os.path.join(master_ssh_dir, "authorized_keys")))

        # 添加known_hosts
        for node_name in self.nodes:
            container = containers[node_name]
            with open(os.path.join(self.ssh_dir, node_name+"/known_hosts"), "wb") as f:
                for _node_name in self.nodes:
                    value = container.exec_run("ssh-keyscan -t rsa {},0.0.0.0".format(_node_name)).output
                    f.write(value)

        os.system("docker-compose -f {} down".format(self.compose_yml_path))

