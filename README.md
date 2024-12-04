# Lhava Webhooks Server

## Overview

A generic API server for setting up webhooks.


## Setup

## Setup

1. After git-cloning the repo, setup the conda env
```shell
conda env create -f webhooks-server-env.yml
```

2. Activate the conda env after creating
```shell
conda activate webhooks-server
```

3. To update the conda env after changes:
```shell
conda env update --file webhooks-server-env.yml --prune
```

## Usage

1a. To run in development mode:
```
fastapi dev main.py
```

1b. To run in production mode:
```
fastapi run main.py
```

