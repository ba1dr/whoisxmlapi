# -*- coding: utf-8 -*-

import re

emailre = re.compile(r"([-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@" +
                     "(?:[a-z0-9](?:[-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|" +
                     "info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z]))", re.I)


def normalize_proxy(proxy):
    """ Returns proxy in the request's format
        Only HTTP proxies supported yet - requesocks can be used
    """
    if not proxy:
        return None
    p = None
    if isinstance(proxy, (str, unicode)):  # just string like '192.168.0.1:3128'
        if not (proxy.startswith('http://') or proxy.startswith('https://')):  # proxy should include protocol
            p = {'http': "http://%s" % proxy, 'https': "http://%s" % proxy}
        else:
            p = {'http': proxy, 'https': proxy}
    elif isinstance(proxy, dict):
        dproxy = ""
        host, auth = "", ""
        proto = proxy.get('proto', None) or proxy.get('protocol', None) or proxy.get('type', None) or 'http'
        if proto.lower() in ['socks', 'socks5', 'socks4']:
            raise ValueError("SOCKS proxies are not supported yet")
        for hn in ['ip', 'ipaddress', 'host', 'hostname']:
            if hn in proxy:
                host = proxy.get(hn, '')
                break
        port = proxy.get('port', 3128)
        username = proxy.get('user', None)
        password = proxy.get('pass', None) or proxy.get('password', None)
        if username and password:
            auth = "%s:%s@" % (username, password)
        dproxy = "%s://%s%s:%s" % (proto.lower(), auth, host, port)
        p = {'http': dproxy, 'https': dproxy}
    return p


def extract_email(value):
    if not isinstance(value, (str, unicode)):
        return ""
    for e in emailre.findall(value):
        return e
    return ""


def extract_phone(value):
    if not isinstance(value, (str, unicode)):
        return ""
    phone_re1 = re.compile(r'\d+', re.I)
    phn = ''.join([p for p in phone_re1.findall(value)])
    return phn


def extract_name(value):
    if not isinstance(value, (str, unicode)):
        return ""
    return value
