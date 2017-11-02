#/usr/bin/env python3
import configparser
import os
import re
import sys
import validators
from pathlib import Path


def exit():
    print("Goodbye.")
    sys.exit(1)

class EtcHosts(object):

    HOSTS_LOCATION = '/etc/hosts'

    def __init__(self):
        self.existing_domains = set()
        with open(self.HOSTS_LOCATION) as fd:
            self.lines = [line.strip() for line in fd.readlines()]
        for line in self.lines:
            if line.startswith('#'):
                continue
            try:
                address, domain = list(filter(None, re.split(r'\s+', line)))
                self.existing_domains.add(domain)
            except IndexError:
                # not a valid line
                pass

    def save(self):
        try:
            with open(self.HOSTS_LOCATION, 'w') as fd:
                fd.write('\n'.join(self.lines))
            print('Updated hosts file')
        except Exception as e:
            print("Failure updating hosts file: {}".format(e))
            exit()

    def add_domains(self, domains):
        for domain in domains:
            if domain in self.existing_domains:
                continue
            line = "127.0.0.1\t{}".format(domain)
            self.lines.append(line)
        self.save()

    def remove_domains(self, domains):
        for domain in domains:
            if domain in self.existing_domains:
                lines_to_remove = []
                for idx, line in enumerate(self.lines):
                    if re.search(domain, line):
                        lines_to_remove.append(idx)
                if lines_to_remove:
                    for idx in lines_to_remove[::-1]:
                        # remove the lines in reverse order
                        self.lines.pop(idx)
        self.save()

class Configuration(object):

    DEFAULT = 'DEFAULT'
    MINUTES = 'minutes'
    DOMAINS = 'domains'
    CONFIG_LOCATION = os.path.expanduser("~/.focusconf")

    def __init__(self, minutes=None, domains=None):
        self.minutes = minutes
        self.domains = domains

    @classmethod
    def _load(cls):
        config = configparser.ConfigParser()
        config.read_file(open(cls.CONFIG_LOCATION))

        minutes = config[cls.DEFAULT][cls.MINUTES]
        domains = config[cls.DEFAULT][cls.DOMAINS].split(',')
        print("minutes: {}".format(minutes))
        print("domains: {}".format(domains))
        return Configuration(minutes=minutes, domains=domains)

    def _save(self):
        config = configparser.ConfigParser()
        config[self.DEFAULT] = {
            self.MINUTES: self.minutes,
            self.DOMAINS: ','.join(self.domains)
        }
        with open(self.CONFIG_LOCATION, 'w') as configfile:
            config.write(configfile)

    @classmethod
    def load(cls):
        config_exists = Path(cls.CONFIG_LOCATION).is_file()
        if not config_exists:
            response = input("No config file exists - would you like to create one now? [Y/N]").lower()
            if response:
                print("You chose: {}".format(response))
                response = response.lower()[0]
                if response == 'y':
                    # do stuff
                    config = cls.create_configuration()
                    config._save()
                    return config
            exit()
        else:
            print("Loading configuration file")
            config = cls._load()
            return config

    @classmethod
    def create_configuration(cls):
        print("Creating configuration:")
        while True:
            minutes = input("Once activated how many minutes do you want to focus for: ")
            try:
                minutes = int(minutes)
                break
            except:
                pass
            print("Invalid input, you specified: '{}', please try again".format(minutes))

        domains = set()
        while True:
            domain = input("Enter a domain to blacklist while you focus (or press enter to continue): ")
            if not domain:
                break
            domain = domain.lower()
            if validators.domain(domain):
                domains.add(domain)
            else:
                print("Invalid domain, you specified: '{}', please try again".format(domain))

        print("Once activated you will focus for {}m - which will prevent access to the following domains:".format(minutes))
        for domain in domains:
            print("\t{}".format(domain))

        return Configuration(minutes=minutes, domains=domains)

if __name__ == '__main__':
    config = Configuration.load()
    etc_hosts = EtcHosts()
    # etc_hosts.add_domains(config.domains)
    etc_hosts.remove_domains(config.domains)


