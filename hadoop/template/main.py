import os

from hadoop_cluster_creater import Creater

# 当前路径
ABSPATH = os.path.abspath(".")
VOLUMES_DIR = os.path.join(ABSPATH, "volumes")
CLUSTER_SSH_DIR = os.path.join(VOLUMES_DIR, "hadoop_cluster_ssh")
COMPOSE_DIR = "."

# 一主两从
CLUSTER = {
    "master": "hadoop-master",
    "slaves": ["hadoop-slave1", "hadoop-slave2"]
}


if __name__ == '__main__':
    # cluster, compose_dir, ssh_dir
    creater = Creater(CLUSTER, COMPOSE_DIR, CLUSTER_SSH_DIR)
    creater.create_docker_compose()
    creater.init_ssh()
