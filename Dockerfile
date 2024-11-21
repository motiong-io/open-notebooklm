# 使用 Python 3.12 基础镜像
FROM python:3.12

# 设置无缓冲模式
ENV PYTHONUNBUFFERED 1

# 定义环境变量
ARG DOCKER_HOME="/opt/motiong"
ARG DOCKER_CODE="/opt/motiong/code"
ARG DOCKER_GROUP="motiong"
ARG DOCKER_USER="motiong"
ARG DOCKER_UID=5000

ENV ZSH="/opt/motiong/.oh-my-zsh"

# 设置工作目录
WORKDIR ${DOCKER_CODE}

# 创建用户和组
RUN groupadd -g ${DOCKER_UID} ${DOCKER_GROUP} \
    && useradd -r -u ${DOCKER_UID} -g ${DOCKER_GROUP} -d ${DOCKER_HOME} ${DOCKER_USER} \
    && chown -R ${DOCKER_USER}:${DOCKER_GROUP} ${DOCKER_HOME}

# 安装基础依赖
RUN apt-get update && \
    apt-get install -y curl sudo cargo ffmpeg libsm6 libxext6 protobuf-compiler zsh git openssh-client && \
    pip install --upgrade pip && \
    pip install poetry==1.8.3

# 安装 oh-my-zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# 设置 SSH 和环境
RUN mkdir ${DOCKER_HOME}/.ssh && \
    chown -R ${DOCKER_USER} ${DOCKER_HOME}/.ssh && \
    ssh-keyscan bitbucket.org >> ${DOCKER_HOME}/.ssh/known_hosts && \
    echo "alias docker='sudo docker'" > ${DOCKER_HOME}/.bashrc

# 复制项目文件到容器中
COPY --chown=${DOCKER_USER} . ${DOCKER_CODE}

# 切换到非 root 用户
USER ${DOCKER_USER}

# 安装 Python 项目依赖
RUN pip install --no-cache-dir -r ${DOCKER_CODE}/requirements.txt

# 暴露服务端口（如需）
EXPOSE 7860

# 容器启动命令
ENTRYPOINT [ "python", "app.py" ]
