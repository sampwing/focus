#/usr/bin/env python3
from .config import Configuration
from .etc_hosts import EtcHosts

if __name__ == '__main__':
    config = Configuration.load()
    etc_hosts = EtcHosts()
    # etc_hosts.add_domains(config.domains)
    etc_hosts.remove_domains(config.domains)
