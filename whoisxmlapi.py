# -*- coding: utf-8 -*-

import requests

from utils import normalize_proxy, extract_email, extract_name, extract_phone


class WhoisXMLAPI(object):

    request_url = 'http://www.whoisxmlapi.com/whoisserver/WhoisService?' + \
        'domainName={domain}&da=2&outputFormat=json{creds}'

    excludenames = ['domain', 'registrar', 'customfield']
    emailignore = ['abuse@', '@whoisguard.com']

    def __init__(self, username=None, password=None, proxies=None, timeout=None, attempts=5):
        self.user_agent = ''
        self.attempts = attempts
        self.proxies = proxies
        if self.proxies and not isinstance(self.proxies, list):
            self.proxies = [self.proxies]
        self.username = username
        self.password = password
        self.timeout = timeout or (30, 90)  # requests timeout: tuple(connect, read)
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 " +
            "(KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
            'DNT': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5'
        }

    def _get_response(self, url):
        """ General method for request """
        proxies = (self.proxies or []) * self.attempts  # to be sure there is enough proxies
        for attempt in xrange(self.attempts):
            try:
                proxy = normalize_proxy(proxies.pop()) if proxies else None
                resp = requests.get(url, headers=self.headers,
                                    proxies=proxy, timeout=self.timeout)
                if not resp.ok:
                    raise ValueError("HTTP code %s" % resp.status_code)
                return resp.json()
            except Exception:
                pass
        return ""

    def get(self, domain):
        creds = ""
        if self.username and self.password:
            creds = "&username=%s&password=%s" % (self.username, self.password)
        url = self.request_url.format(domain=domain, creds=creds)
        data = self._get_response(url)
        return data

    def extract_contacts(self, data):
        retval = {'emails': [], 'phones': [], 'names': []}

        def _walkdict(dobj):
            if not dobj or not isinstance(dobj, dict):
                return
            for k in dobj:
                val = dobj[k]
                lowerkey = k.lower()
                if lowerkey.find('email') >= 0:
                    eml = extract_email(val)
                    if eml:
                        skipthis = False
                        for ei in self.emailignore:
                            if eml.find(ei) >= 0:
                                skipthis = True
                                break
                        if skipthis:
                            continue
                        retval['emails'].append(eml)
                if lowerkey.find('phone') >= 0:
                    phn = extract_phone(val)
                    if phn:
                        retval['phones'].append(phn)
                if lowerkey.find('name') >= 0:
                    skipthis = False
                    for en in self.excludenames:
                        if lowerkey.find(en) >= 0:
                            skipthis = True
                            break
                    if skipthis:
                        continue
                    name = extract_name(val)
                    if name:
                        # print("name: %s = %s" % (k, val))
                        retval['names'].append(name)
                _walkdict(val)

        _walkdict(data)
        for k in retval:  # remove duplicates
            if isinstance(retval[k], list):
                retval[k] = set(retval[k])
        return retval
