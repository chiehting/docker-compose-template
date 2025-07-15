FROM stephengpope/no-code-architects-toolkit@sha256:0b62e862c87eebe00b1f467a41d5216de26dfd72ce5f31475455c7ee58e42680
USER root
RUN apt-get update && \
    apt-get install -y fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*
USER appuser