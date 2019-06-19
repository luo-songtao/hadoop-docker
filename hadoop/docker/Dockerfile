FROM ubuntu:18.04

LABEL maintainer="ryomawithlst@gmail.com"

# 更换国内阿里镜像源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe " >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe " >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe " >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe " >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe " >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe " >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe " >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe " >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe " >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe " >> /etc/apt/sources.list

# 安装辅助工具：wget、ssh-server
RUN apt-get update && \
    apt-get install -y wget openssh-server && \
    apt-get clean

# 控制安装的Hadoop版本
ARG VERSION

# 下载binary版本直接使用，删除doc以降低镜像大小
RUN cd /root/ && \
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-$VERSION/hadoop-$VERSION.tar.gz && \
    tar -xvf hadoop-$VERSION.tar.gz && \
    rm -rf hadoop-$VERSION/share/doc && rm -rf hadoop-$VERSION.tar.gz && \
    mkdir /apache && mv hadoop-$VERSION /apache/hadoop && \
    echo "export PATH=\$PATH:/apache/hadoop/bin" >> /root/.bashrc

# 安装jdk8以后，配置JAVA_HOME: /usr/lib/jvm/java-8-openjdk-amd64
# 注意: 不同版本系统，JAVA_HOME位置可能不同，这里以18.04为例，因此如果有改写可以从这之后改写Dockerfile
RUN apt-get install -y openjdk-8-jdk && apt-get clean && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /root/.bashrc

RUN echo "export PATH=\$PATH:/apache/hadoop/bin" >> /etc/profile && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> /etc/profile

ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]