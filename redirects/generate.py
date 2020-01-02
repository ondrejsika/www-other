#!/usr/bin/env python

_CONFIG = {
    'https://skolenie.kubernetes.sk/': ['kubernetes.sk'],
    'https://training.kubernetes.is/': ['kubernetes.is'],
    'https://training.kubernetes.lu/': ['kubernetes.lu'],
    'https://trainera.io/': ['trainera.cz'],
    'https://ondrej-sika.cz/': ['ondrejsika.cz'],
    'https://sika.io/': ['ondrejsika.ch', 'docker-training.eu', 'git-training.eu'],
    'https://ondrejsika.com/': ['os.oxs.cz'],
}

_CONFIG_PATH = {
    'sedu.cz': {
        "redirects": {
            "/terminy": "https://ondrej-sika.cz/verejne-terminy/",
            "/kontakt": "https://ondrej-sika.cz/kontakt/",
            "/kurzy/docker": "https://ondrej-sika.cz/skoleni/docker/",
            "/kurzy/ansible": "https://ondrej-sika.cz/skoleni/ansible/",
            "/kurzy/kubernetes": "https://ondrej-sika.cz/skoleni/kubernetes/",
            "/kurzy/git": "https://ondrej-sika.cz/skoleni/git/",
            "/kurzy/terraform": "https://ondrej-sika.cz/skoleni/terraform/",
            "/kurzy/gitlab-ci": "https://ondrej-sika.cz/skoleni/gitlab-ci/",
            "/kurzy/kvm-virtualizace": "https://ondrej-sika.cz/skoleni/proxmox/",
        },
        "default": "https://ondrej-sika.cz",
        "status_code": "301"
    }
}

CONFIG = {}
for target, sources in _CONFIG.items():
    CONFIG[target] = sources
    CONFIG[target] += map(lambda x: 'www.%s' % x, sources)

NGINX_SITE_TEMPLATE = '''
server {
  listen 80;

  server_name %s;
  return 302 %s;
}
'''

NGINX_SITE_WITH_PATHS_TEMPLATE = '''
server {
  listen 80;

  server_name %s;
  %s
}
'''

NGINX_PATH_TEMPLATE = '''
  location ^~ %s {
    return %s %s;
  }
'''

DOCKER_COMPOSE_TEMPLATE = '''# GENERATED by ./generate.py
version: '3.7'
services:
  app:
    build: .
    image: ${IMAGE:-registry.sikahq.com/www/www-other/redirects}
    labels:
      traefik.frontend.rule: Host:%s
      traefik.enable: 'true'
    networks:
        - traefik

networks:
  traefik:
    external:
      name: traefik
'''


with file('nginx-site.conf', 'w') as f:
    out = []
    out += ['# GENERATED by ./generate.py\n']
    out += [
        NGINX_SITE_TEMPLATE % (' '.join(sources), target) for target, sources in CONFIG.items()
    ]

    for domain, conf in _CONFIG_PATH.items():
        path_list = [NGINX_PATH_TEMPLATE % (src, conf["status_code"], dest) for src, dest in conf["redirects"].items()]
        path_list.append(NGINX_PATH_TEMPLATE % ('/', conf["status_code"], conf["default"]))
        out.append(NGINX_SITE_WITH_PATHS_TEMPLATE % ("%s www.%s" % (domain, domain), "".join(path_list)))

    f.write(''.join(out))

with file('docker-compose.yml', 'w') as f:
    f.write(DOCKER_COMPOSE_TEMPLATE % (','.join([','.join(sources) for sources in CONFIG.values()]  + [ '%s,www.%s' % (domain, domain) for domain in _CONFIG_PATH.keys()])))
