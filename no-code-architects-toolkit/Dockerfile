FROM stephengpope/no-code-architects-toolkit:146
USER root
RUN apt-get update && \
    apt-get install -y fonts-noto-cjk && \
    rm -rf /var/lib/apt/lists/*
USER appuser