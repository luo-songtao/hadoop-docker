import os
import sys

from lib import HadoopStarter, HadoopStoper, HadoopStatusChecker,\
    SSHInitYamlTemplate, StarterYamlTemplate, SSHInitializer, HDFSInitializer
from config import CLUSTER_CONFIG, DATA_VOLUMES_DIR, CLUSTER_SSH_DIR_PATH


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] not in ["start", "stop", "status", "init"]:
        print("Usage: python {} start/stop/status/init".format(__file__.split("/")[-1]))
    else:
        if sys.argv[1] == "start":
            HadoopStarter(CLUSTER_CONFIG).run()
        if sys.argv[1] == "stop":
            HadoopStoper(CLUSTER_CONFIG).run()
        if sys.argv[1] == "status":
            HadoopStatusChecker(CLUSTER_CONFIG).run()
        if sys.argv[1] == "init":
            # 建立yml文件
            SSHInitYamlTemplate(CLUSTER_CONFIG).create()
            StarterYamlTemplate(CLUSTER_CONFIG).create()
            if os.path.exists(CLUSTER_SSH_DIR_PATH):
                ret = input("是否清空SSH数据重新生成?(yes/no):")
                if ret == "yes":
                    os.remove(CLUSTER_SSH_DIR_PATH)
                    # 初始化SSH配置
                    SSHInitializer(CLUSTER_CONFIG).init()
                else:
                    sys.exit(0)
            else:
                # 初始化SSH配置
                SSHInitializer(CLUSTER_CONFIG).init()
            if os.path.exists(DATA_VOLUMES_DIR):
                ret = input("是否清空数据重新格式化HDFS?(yes/no):")
                if ret == "yes":
                    os.remove(DATA_VOLUMES_DIR)
                    HDFSInitializer(CLUSTER_CONFIG).init()
                else:
                    sys.exit(0)
            else:
                # 初始化HDFS
                HDFSInitializer(CLUSTER_CONFIG).init()
