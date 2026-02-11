FROM mcr.microsoft.com/devcontainers/python:1-3-bookworm

ENV PYTHONUNBUFFERED 1

# Install Node.js LTS (via nodesource)
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && \
    apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends \
    nodejs \
    build-essential \
    git \
    curl \
    wget \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install commonly needed Python dev tools
RUN pip3 install --no-cache-dir \
    black \
    pylint \
    pytest \
    pytest-cov

# Install Node package managers/tools globally
RUN npm install -g \
    npm@latest \
    yarn \
    pnpm

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY planventure-api/requirements.txt /tmp/pip-tmp/requirements.txt
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp