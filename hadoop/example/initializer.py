from hadoop_cluster_creater import Creater

from config import *


if __name__ == '__main__':
    # cluster, compose_dir, ssh_dir
    creater = Creater(CLUSTER, COMPOSE_DIR, CLUSTER_SSH_DIR)
    creater.create_docker_compose()
    creater.init_ssh()
