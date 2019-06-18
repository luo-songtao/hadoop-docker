import os

# 当前路径
ABSPATH = os.path.abspath(".")
VOLUMES_DIR = os.path.join(ABSPATH, "volumes")
CLUSTER_SSH_DIR = os.path.join(VOLUMES_DIR, "hadoop_cluster_ssh")
COMPOSE_DIR = "docker-compose"

# 一主两从
CLUSTER = {
    "master": "hadoop-master",
    "slaves": ["hadoop-slave1", "hadoop-slave2"]
}