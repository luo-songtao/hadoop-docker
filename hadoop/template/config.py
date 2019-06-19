import os

from lib.default_config import *

'''通用配置'''
# 当前路径
ABSPATH = os.path.abspath(".")
# 统一设置的集群的数据卷的根目录
DATA_VOLUMES_DIR = os.path.join(ABSPATH, "data")
# 存放集群的SSH配置信息的根目录
CLUSTER_SSH_DIR_PATH = os.path.join(ABSPATH, "hadoop_cluster_ssh")
# Compose文件存放路径
COMPOSE_DIR_PATH = os.path.join(ABSPATH, ".")
# HADOOP-CONFIG文件存放路径
HADOOP_COMMON_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/common/")
HADOOP_CUSTOM_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/custom/")
HADOOP_DEFAULT_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/default/")

os.system("cp {}* {}".format(HADOOP_DEFAULT_CONFIG_PATH, HADOOP_COMMON_CONFIG_PATH))
os.system("cp {}* {}".format(HADOOP_CUSTOM_CONFIG_PATH, HADOOP_COMMON_CONFIG_PATH))

'''CUSTOM CONFIG'''

IMAGE_NAME = "hadoop:2.9.2"
MASTER_NAME = "hadoop-master"
SLAVES_NAME = ["hadoop-slave1", "hadoop-slave2", "hadoop-slave3"]

master_config = {
    "node_name": MASTER_NAME,
    "image": IMAGE_NAME,
    "node_ssh_dir": os.path.join(CLUSTER_SSH_DIR_PATH, MASTER_NAME),
    "hadoop_config_dir": HADOOP_COMMON_CONFIG_PATH,
    "hadoop_data_dir": os.path.join(DATA_VOLUMES_DIR, MASTER_NAME)
}

slaves_config = [
    {
        "node_name": SLAVE_NAME,
        "image": IMAGE_NAME,
        "node_ssh_dir": os.path.join(CLUSTER_SSH_DIR_PATH, SLAVE_NAME),
        "hadoop_config_dir": HADOOP_COMMON_CONFIG_PATH,
        "hadoop_data_dir": os.path.join(DATA_VOLUMES_DIR, SLAVE_NAME)
    } for SLAVE_NAME in SLAVES_NAME
]

CLUSTER_CONFIG = {
    "master": master_config,
    "slaves": slaves_config
}