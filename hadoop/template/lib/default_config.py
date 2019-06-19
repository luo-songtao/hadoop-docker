import os

__all__ = [
    'ABSPATH',
    'CLUSTER_CONFIG_TEMPLATE',
    'CLUSTER_SSH_DIR_PATH',
    'COMPOSE_DIR_PATH',
    'DATA_VOLUMES_DIR',
    'HADOOP_COMMON_CONFIG_PATH',
    'HADOOP_CUSTOM_CONFIG_PATH',
    'HADOOP_DEFAULT_CONFIG_PATH',
    'SSH_INIT_COMPOSE_YML_PATH',
    'STARTER_COMPOSE_YML_PATH',
    'VERSION',
    '_SSH_INIT_YML_NODE_FORMAT',
    '_STARTER_MASTER_NODE_FORMAT',
    '_STARTER_SLAVE_NODE_FORMAT',
    '_YML_FOOTER',
    '_YML_HEADER',
    'JAVA_HOME',
    'HADOOP_HOME'
]

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
HADOOP_COMMON_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/common")
HADOOP_CUSTOM_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/custom")
HADOOP_DEFAULT_CONFIG_PATH = os.path.join(ABSPATH, "hadoop-config/default")
# docker compose 版本
VERSION = "3.7"

# HADOOP环境信息
HADOOP_HOME = "/apache/hadoop/"
JAVA_HOME = "/usr/lib/jvm/java-8-openjdk-amd64"

'''SSHInitializer配置'''
SSH_INIT_COMPOSE_YML_PATH = os.path.join(COMPOSE_DIR_PATH, "sshInitializer.yml")

''' 配置'''
STARTER_COMPOSE_YML_PATH = os.path.join(COMPOSE_DIR_PATH, "starter_compose.yml")

'''YML Config Template'''

_YML_HEADER = '''\
version: "{version}"
services:
'''

_YML_FOOTER = '''\
networks:
  default:
    name: hadoop-cluster
'''

_SSH_INIT_YML_NODE_FORMAT = '''\
  {node_name}:
    image: {image}
    hostname: {hostname}
    container_name: {container_name}
    volumes:
      - {node_ssh_dir}:/root/.ssh
'''

_STARTER_SLAVE_NODE_FORMAT = '''\
  {node_name}:
    image: {image}
    hostname: {hostname}
    container_name: {container_name}
    volumes:
      - {node_ssh_dir}:/root/.ssh
      - {hadoop_config_dir}:/apache/hadoop/etc/hadoop/
      - {hadoop_data_dir}:/data/
'''

_STARTER_MASTER_NODE_FORMAT = _STARTER_SLAVE_NODE_FORMAT + '''\
    ports:
      - 50070:50070
      - 8088:8088
'''

'''Cluster Config'''

CLUSTER_CONFIG_TEMPLATE = {
    "master": {
        "node_name": "master",
        "image": "hadoop:2.9.2",
        "node_ssh_dir": "ssh_dir",
        "hadoop_config_dir": "hadoop-config/common",
        "hadoop_data_dir": "volumes/data"
    },
    "slaves": [
        {
            "node_name": "slave1",
            "image": "hadoop:2.9.2",
            "node_ssh_dir": "ssh_dir",
            "hadoop_config_dir": "hadoop-config/common",
            "hadoop_data_dir": "volumes/data"
        },
        {
            "node_name": "slave2",
            "image": "hadoop:2.9.2",
            "node_ssh_dir": "ssh_dir",
            "hadoop_config_dir": "hadoop-config/common",
            "hadoop_data_dir": "volumes/data"
        },
        {
            "node_name": "slave3",
            "image": "hadoop:2.9.2",
            "node_ssh_dir": "ssh_dir",
            "hadoop_config_dir": "hadoop-config/common",
            "hadoop_data_dir": "volumes/data"
        }
    ]
}

if __name__ == '__main__':
    from pprint import pprint
    import default_config
    pprint(dir(default_config))