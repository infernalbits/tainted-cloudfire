import urllib.request
import http.client
from urllib.error import HTTPError
import zipfile
import os
import sys
import time


class Updater:
    def run():
        if Updater.uptodate():
            return

        downloads = [
            ['https://www.cloudflare.com/ips-v4', 'lists/cloudflare_ipv4'],
            ['https://www.cloudflare.com/ips-v6', 'lists/cloudflare_ipv6'],
        ]

        for d in downloads:
            Updater.download(d[0], d[1])

        Updater.last_updated(Updater.today())

    def uptodate():
        try:
            last_updated = open('lists/last_updated', 'r').read()
            if last_updated == Updater.today():
                return True
        except FileNotFoundError:
            sys.stdout.write('[info] lists/last_updated not found, forcing update.\n')
            sys.stdout.flush()
        return False

    def last_updated(date):
        with open('lists/last_updated', 'w') as file:
            file.write(date)

    def today():
        return time.strftime("%Y-%m-%d")

    def download(url, file):
        sys.stdout.write('[download] %s\n' % url)
        sys.stdout.flush()
        try:
            urllib.request.urlretrieve(url, file)
            sys.stdout.write('[info] Downloaded %s to %s\n' % (url, file))
            sys.stdout.flush()
        except HTTPError as e:
            sys.stderr.write('[error] Failed to download %s: HTTP Error %s - %s\n' % (url, e.code, e.reason))
            sys.stderr.flush()
        except (OSError, http.client.BadStatusLine) as e:
            sys.stderr.write('[error] Failed to download %s: %s\n' % (url, e))
            sys.stderr.flush()
