
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04 as os-base

RUN apt update --fix-missing && apt upgrade -y

FROM os-base as python-base

ARG PYTHON_VER=3.12.4
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1


# Base for majority
ARG BUILD_DEPS="wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev"
RUN apt update --fix-missing && \
    apt upgrade -y && \
    apt install --fix-missing -y $BUILD_DEPS

# Add psycog dependencies
ARG BUILD_DEPS2="libpq-dev postgresql-server-dev-all libsqlite3-dev"
RUN apt update --fix-missing && apt install --fix-missing -y $BUILD_DEPS2

# Add additional dependencies - operators
ARG BUILD_DEPS3="dpkg-dev gcc libbluetooth-dev libbz2-dev libc6-dev libexpat1-dev liblzma-dev make tk-dev uuid-dev xz-utils"
RUN apt update --fix-missing && apt install --fix-missing -y $BUILD_DEPS3

# Add additional dependencies - automl
ARG BUILD_DEPS4="libomp-dev ca-certificates netbase tzdata libgomp1 g++ ffmpeg libsm6 libxext6"
RUN apt update --fix-missing && apt install --fix-missing -y $BUILD_DEPS4

RUN wget https://www.python.org/ftp/python/$PYTHON_VER/Python-$PYTHON_VER.tgz && \
    tar xzf Python-$PYTHON_VER.tgz && cd Python-$PYTHON_VER && \
    ./configure --enable-optimizations && \
    make altinstall && \
    /usr/local/bin/pip3.12 install --upgrade setuptools && \
    ln -sf /usr/local/bin/python3.12 /usr/local/bin/python && \
    rm -rf /Python-$PYTHON_VER.tgz /Python-$PYTHON_VER

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && rm get-pip.py

RUN apt autoremove -y --purge && apt clean -y

FROM python-base as app-base

ENV PYTHONUNBUFFERED 1
# to prevent run as root
ARG DOCKER_HOME="/opt/motiong"
ARG DOCKER_CODE="/opt/motiong/code"
ARG DOCKER_GROUP="motiong"
ARG DOCKER_USER="motiong"
ARG DOCKER_UID=5000

ENV ZSH="/opt/motiong/.oh-my-zsh"

WORKDIR ${DOCKER_CODE}

RUN groupadd -g ${DOCKER_UID} ${DOCKER_GROUP} \
    && useradd -r -u ${DOCKER_UID} -g ${DOCKER_GROUP} -d ${DOCKER_HOME} ${DOCKER_USER} \
    && chown -R ${DOCKER_USER}:${DOCKER_GROUP} ${DOCKER_HOME}

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y git && \
    apt-get install -y postgresql-client && \
    apt-get install -y openssh-client && \
    pip install --upgrade pip && \
    pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt


# Install zsh, omz, plugins
RUN apt-get install -y zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# will add examples to install our own python modules
# maybe not via git+ssh, well we will decide later if we have any
RUN mkdir ${DOCKER_HOME}/.ssh && \
    chown -R ${DOCKER_USER} ${DOCKER_HOME}/.ssh && \
    ssh-keyscan github.com >> ${DOCKER_HOME}/.ssh/known_hosts

ENV PATH "$PATH:/opt/motiong/.local/bin"
ENV PYTHONPATH=.

USER ${DOCKER_USER}
ENTRYPOINT [ "/bin/sh", "-c" ]