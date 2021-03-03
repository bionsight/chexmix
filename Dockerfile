FROM jupyter/datascience-notebook:latest
LABEL maintainer="Bionsight <dev@bionsight.com>"

# avoid TERM related warnings. See https://github.com/phusion/baseimage-docker/issues/58
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# install basic utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    bzip2 \
    ca-certificates \
    curl \
    git \
    gosu \
    sudo \
    tmux \
    vim \
    wget \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
