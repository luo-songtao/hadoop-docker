import os
import time

import docker

from config import CLUSTER_SSH_DIR_PATH, SSH_INIT_COMPOSE_YML_PATH


class SSHInitializer(object):

    def __init__(self, nodes_config):
        self.master = nodes_config["master"]["node_name"]
        self.slaves = [i["node_name"] for i in nodes_config["slaves"]]

        self.nodes = [self.master]+self.slaves

    def init(self):
        '''
        初始化SSH配置：设置集群间免密登录
        注意：该方法只用执行一次，一旦创建出密钥文件和授权文件后则不需要再执行
        '''
        # 初次启动集群
        os.system("docker-compose -f {} up -d ".format(SSH_INIT_COMPOSE_YML_PATH))

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
        master_ssh_dir = os.path.join(CLUSTER_SSH_DIR_PATH, self.master)
        os.system("cat {} >> {}".format(
            os.path.join(master_ssh_dir, "id_rsa.pub"),
            os.path.join(master_ssh_dir, "authorized_keys"),
        ))

        # 遍历每一个从节点
        for slave_node in self.slaves:
            slave_ssh_dir = os.path.join(CLUSTER_SSH_DIR_PATH, slave_node)
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
            with open(os.path.join(CLUSTER_SSH_DIR_PATH, node_name+"/known_hosts"), "wb") as f:
                for _node_name in self.nodes:
                    value = container.exec_run("ssh-keyscan -t rsa {},0.0.0.0".format(_node_name)).output
                    f.write(value)

        os.system("docker-compose -f {} down".format(SSH_INIT_COMPOSE_YML_PATH))


if __name__ == '__main__':
    # cluster, compose_dir, ssh_dir
    from config import CLUSTER_CONFIG_TEMPLATE
    sshInitializer = SSHInitializer(CLUSTER_CONFIG_TEMPLATE)
    sshInitializer.init()
