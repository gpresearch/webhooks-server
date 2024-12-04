FROM continuumio/miniconda3:24.5.0-0

# Copy the Python script into the container
ADD . /usr/src/app
WORKDIR /usr/src/app

# Setup env variables required to access private crate registry.
# Requires passing in an AWS token as an environment variable/build arg.
ARG CARGO_REGISTRIES_LHAVA_DEV_TOKEN
ENV CARGO_REGISTRIES_LHAVA_DEV_INDEX="sparse+https://lhava-dev-533267214762.d.codeartifact.us-east-2.amazonaws.com/cargo/lhava-dev/"
ENV CARGO_REGISTRY_GLOBAL_CREDENTIAL_PROVIDERS="cargo:token"

# Install gcc/cc compilers & CMake for building Rust binaries.
RUN apt-get update && apt-get install -y build-essential && apt-get install -y cmake

# Install Rust and include cargo in path.
RUN wget -O rustup-init.sh https://sh.rustup.rs && \
    chmod +x ./rustup-init.sh && \
    ./rustup-init.sh -y \
    && . $HOME/.cargo/env \ 
    && cargo --help

ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo --help


# Need this to enable conda command to work.
SHELL ["/bin/bash", "-c"] 
# Need this to be able to pip install github packages from our private repo
# pass in docker build with --build-arg GH_TOKEN=your_token


ARG GH_TOKEN
RUN \ 
    git config --global user.email alex@lhava.io && \
    git config --global url."https://oauth2:${GH_TOKEN}@github.com".insteadOf https://github.com

ENV PYTHONUNBUFFERED=1


RUN conda env create -f webhooks-server-env.yml

#https://pythonspeed.com/articles/activate-conda-dockerfile/
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "webhooks-server", "fastapi", "run", "api.py"]

