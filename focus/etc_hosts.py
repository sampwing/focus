#/usr/bin/env python3
import re

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
