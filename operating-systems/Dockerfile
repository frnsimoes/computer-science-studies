FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    vim \
    gcc \
    gdb \
    manpages-dev \
    bsdmainutils \
    strace \
    ltrace \
    htop \
    sysstat \
    net-tools \
    iputils-ping \
    iproute2 \
    curl \
    wget \
    unzip \
    sudo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

ENV EDITOR=vim

CMD ["bash"]
