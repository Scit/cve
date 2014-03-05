import sys
import urllib2
import urlparse
import re

from bs4 import BeautifulSoup


target = None

if '-f' in sys.argv:
    if len(sys.argv) < 3:
        print 'Use: cve.py [-f <outputfile>]'
        sys.exit(2)
    target = sys.argv[2]

main_url = 'https://access.redhat.com'
content = urllib2.urlopen(urlparse.urljoin(main_url, '/security/cve/'))
soup = BeautifulSoup(content)

handle = open(target, 'w') if target else sys.stdout

items = soup.find(id='cves_table').find('tbody').find_all('a', class_='internal')
for item in items:
    title = item.get_text()

    rhsa_site = urlparse.urljoin(main_url, item['href'])
    rhsa_content = urllib2.urlopen(rhsa_site)
    soup = BeautifulSoup(rhsa_content)

    try:
        rhsa = soup.find('table', class_='docstable').find('td', text=re.compile('Red Hat Enterprise Linux version 6')).parent.find('a', class_='internal')['href']
    except AttributeError:
        rhsa = ''

    handle.write('%s %s\n' % (title, rhsa))

if handle is not sys.stdout:
    handle.close
