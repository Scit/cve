#!/usr/bin/env python
import sys
import getopt
import urllib2
import urlparse
import re

from bs4 import BeautifulSoup
from multiprocessing import Pool


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:')
    except getopt.GetoptError:
        print("Usage: %s [-f <filename>]" % sys.argv[0])
        sys.exit(2)

    handle = sys.stdout
    for opt, arg in opts:
        if opt == '-f':
            handle = open(arg, 'w')

    cves_url = 'https://access.redhat.com'
    content = urllib2.urlopen(urlparse.urljoin(cves_url, '/security/cve/'))
    soup = BeautifulSoup(content)
    cves = soup.find(id='cves_table').find('tbody').find_all('a', class_='internal')

    cve_pairs = []
    for cve in cves:
        title = cve.get_text()
        description_url = urlparse.urljoin(cves_url, cve['href'])

        cve_pairs.append(
            {'title': title,
             'description_url': description_url}
        )

    pool = Pool(processes=20)
    results = pool.map(get_cve_info, cve_pairs)

    for result in results:
        handle.write('%s %s\n' % result)

    if handle is not sys.stdout:
        handle.close()


def get_cve_info(cve_pair):
    content = urllib2.urlopen(cve_pair['description_url'], timeout=5).read()
    soup = BeautifulSoup(content)

    try:
        errata = soup.find('table', class_='docstable').find('td', text=re.compile('Red Hat Enterprise Linux version 6')).parent.find('a', class_='internal')['href']
    except AttributeError:
        errata = ''
    return cve_pair['title'], errata


if __name__ == '__main__':
    main()
