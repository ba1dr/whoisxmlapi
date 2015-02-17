# whoisxmlapi

Python parser fow www.whoisxmlapi.com

Supports queries through the list of proxies (rotating in multiple attempts)

Thanks to [dalek2point3/whoisxmlapi-parser](https://github.com/dalek2point3/whoisxmlapi-parser) for the idea

Usage:

```python

from whoisxmlapi import WhoisXMLAPI

w = WhoisXMLAPI()
domaininfo = w.get('google.com')

print(domaininfo)

print w.extract_contacts(domaininfo)

```
