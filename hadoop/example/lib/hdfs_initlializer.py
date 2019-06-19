import os
import docker

from config import STARTER_COMPOSE_YML_PATH


class HDFSInitializer(object):

    def __init__(self, nodes_config):
        self.master_name = nodes_config["master"]["node_name"]

    def init(self):
        # 启动集群
        os.system("docker-compose -f {} up -d ".format(STARTER_COMPOSE_YML_PATH))

        client = docker.from_env()
        master = client.containers.get(self.master_name)
        temp = master.exec_run("/apache/hadoop/bin/hadoop namenode -format")
        print(temp.output.decode())

        os.system("docker-compose -f {} down ".format(STARTER_COMPOSE_YML_PATH))