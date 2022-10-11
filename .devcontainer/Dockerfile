# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}


# [Optional] Uncomment this section to install additional OS packages.
RUN apt update && export DEBIAN_FRONTEND=noninteractive \
    && apt -y install --no-install-recommends \
    curl \
    libgtk-3-0 \
    libgstreamer1.0-0 \
    mesa-utils \
    libmtdev-dev \
    libsdl2-dev \
    mesa-common-dev

COPY /assets /assets


ENV POETRY_VERSION=1.2.1
# Install Poetry
ENV POETRY_HOME=/etc/poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
ENV PATH="${POETRY_HOME}/bin:${PATH}"

# RUN poetry config virtualenvs.create false \
# 	&& poetry run pip install --upgrade pip \
# 	&& poetry install --no-interaction --no-ansi
