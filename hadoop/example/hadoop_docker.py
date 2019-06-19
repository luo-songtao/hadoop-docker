import sys

from lib import HadoopStarter, HadoopStoper, HadoopStatusChecker
from config import CLUSTER_CONFIG

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] not in ["start", "stop", "status"]:
        print("Usage: python {} start/stop".format(__file__.split("/")[-1]))
    else:
        if sys.argv[1] == "start":
            HadoopStarter(CLUSTER_CONFIG).run()
        if sys.argv[1] == "stop":
            HadoopStoper(CLUSTER_CONFIG).run()
        if sys.argv[1] == "status":
            HadoopStatusChecker(CLUSTER_CONFIG).run()
