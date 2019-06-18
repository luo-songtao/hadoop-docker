import os
import sys


def main():
    if len(sys.argv) == 1:
        print("Usage: python {file_name} $hadoop-version \nSuch As: python {file_name} 2.9.2".format(file_name=__file__.split("/")[-1]))
    else:
        version = sys.argv[1]
        os.system("docker build --build-arg VERSION={version} . -t hadoop:{version}".format(version=version))


if __name__ == '__main__':
    main()
