import socket


class HostByName(object):

    ips = {}

    def __init__(self, domain):
        self.domain = domain

    def __get__(self, obj=None, objtype=None):
        if self.domain in self.ips:
            return self.ips[self.domain]

        # Basic validation for malformed domain names
        if not self.domain or self.domain.startswith('.') or self.domain.endswith('.') or '..' in self.domain:
            sys.stderr.write(f'[error] Malformed domain name "{self.domain}". Skipping resolution.\n')
            sys.stderr.flush()
            ip = None
        else:
            try:
                ip = socket.getaddrinfo(self.domain, 80)[1][4][0]
            except OSError:
                ip = None
            except UnicodeEncodeError as e: # Catch the specific error
                sys.stderr.write(f'[error] UnicodeEncodeError for domain "{self.domain}": {e}. Skipping resolution.\n')
                sys.stderr.flush()
                ip = None

        self.ips[self.domain] = ip
        return ip

    def __set__(self, obj=None, val=None):
        raise AttributeError
