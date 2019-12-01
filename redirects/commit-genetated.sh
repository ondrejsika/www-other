#!/bin/sh

cd "$(dirname $0)"
git add docker-compose.yml nginx-site.conf
git commit -S -n -m "[generated] redirects - Generate Docker Compose & Nginx config from ./generate.py configuration"
