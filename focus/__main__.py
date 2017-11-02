#/usr/bin/env python3
import sched

from .config import Configuration
from .etc_hosts import EtcHosts

if __name__ == '__main__':
    config = Configuration.load()
    etc_hosts = EtcHosts()
    etc_hosts.add_domains(config.domains)

    print("Focusing for {} minute(s)".format(config.minutes))

    seconds = config.minutes * 60
    scheduler = sched.scheduler()
    scheduler.enter(seconds, 1, etc_hosts.remove_domains, (config.domains, ))
    scheduler.run()
