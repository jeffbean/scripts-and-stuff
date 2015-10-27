#!/bin/bash

docker run --name rdocker_redis --restart="always" -d -p 6379:6379 dockerfile/redis

docker run --name rdocker_registry --net host --restart="always" -d -v /opt/docker_registry_config.yml:/config.yml -v /opt/hcp.py:/usr/local/lib/python2.7/dist-packages/docker_registry/drivers/hcp.py -e DOCKER_REGISTRY_CONFIG=/config.yml -e SETTINGS_FLAVOR=hcp -e AWS_KEY="ZG9ja2Vy" -e AWS_SECRET="a3b9c163f6c520407ff34cfdb83ca5c6" -e AWS_BUCKET=docker -e AWS_HOST=panama.hcp.mcp.com -e CACHE_LRU_REDIS_HOST=localhost -e CACHE_LRU_REDIS_PORT=6379 registry:0.8.1
