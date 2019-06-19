import os

import docker

from config import STARTER_COMPOSE_YML_PATH, JAVA_HOME, HADOOP_HOME


class HadoopStarter(object):

    def __init__(self, nodes_config):
        self.master_name = nodes_config["master"]["node_name"]

    def run(self):
        # 启动集群
        os.system("docker-compose -f {} up -d ".format(STARTER_COMPOSE_YML_PATH))

        client = docker.from_env()
        master = client.containers.get(self.master_name)
        temp = master.exec_run(os.path.join(HADOOP_HOME, "sbin/start-dfs.sh"))
        print(temp.output.decode())
        temp = master.exec_run(os.path.join(HADOOP_HOME, "sbin/start-yarn.sh"))
        print(temp.output.decode())


class HadoopStoper(object):

    def __init__(self, nodes_config):
        self.master_name = nodes_config["master"]["node_name"]

    def run(self):
        client = docker.from_env()
        master = client.containers.get(self.master_name)
        temp = master.exec_run(os.path.join(HADOOP_HOME, "sbin/stop-yarn.sh"))
        print(temp.output.decode())
        temp = master.exec_run(os.path.join(HADOOP_HOME, "sbin/stop-dfs.sh"))
        print(temp.output.decode())
        os.system("docker-compose -f {} down ".format(STARTER_COMPOSE_YML_PATH))


class HadoopStatusChecker(object):

    def __init__(self, nodes_config):
        self.master_name = nodes_config["master"]["node_name"]
        self.nodes = [nodes_config["master"]["node_name"]] + \
                     [n["node_name"] for n in nodes_config["slaves"]]

    def run(self):
        client = docker.from_env()
        for node_name in self.nodes:
            container = client.containers.get(node_name)
            temp = container.exec_run(os.path.join(JAVA_HOME, "bin/jps"))
            print(node_name, ":")
            print(temp.output.decode())
