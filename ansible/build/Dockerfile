FROM python:3.7.3-alpine3.9
LABEL maintainer="ting911111@gmai.com"

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN apk add --no-cache build-base libffi-dev openssl-dev openssh openssh-server sshpass \
    && sed -i "s/#PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config \
    && ssh-keygen -t rsa -P "" -f /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -t ecdsa -P "" -f /etc/ssh/ssh_host_ecdsa_key \
    && ssh-keygen -t ed25519 -P "" -f /etc/ssh/ssh_host_ed25519_key \
    && pip install --upgrade pip \
    && pip install ansible jmespath

