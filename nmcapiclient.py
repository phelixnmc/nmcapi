# -*- coding: utf-8 -*-

"""
Get Namecoin name_show like data from an API server.

"""

import ssl
import urllib2
import hashfuscate
import json
import os
import traceback

USER_AGENT = 'nmcapiclient 100 ' + str(os.name)

class NmcApiError(Exception):
    pass

class NmcApiOpener(object):
    def __init__(self, url, hashfuscate=True, timeout=None):
        self.url = url
        self.timeout = timeout
        self.useHashfuscate = hashfuscate

        if not url.startswith("http://"):
            try:
                sslContext = ssl.create_default_context()
            except AttributeError:
                raise NmcApiError("httpS connection not available. " +
                                  "Upgrade to a newer Python version "+
                                  "or change API URL to plain http")
            # remove unsafe RC4 ciphers if present (https://hg.python.org/cpython/rev/3596081cfb55)
            if "RC4" in ssl._DEFAULT_CIPHERS.upper().replace("!RC4", ""):
                sslContext.set_ciphers('DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:!eNULL:!MD5')

            self.opener = urllib2.build_opener(urllib2.HTTPHandler(),
                                      urllib2.HTTPSHandler(context=sslContext))
        else:
            self.opener = urllib2.build_opener(urllib2.HTTPHandler())

        self.opener.addheaders = [('User-agent', USER_AGENT)]

    def get_name(self, name, processed=True):
        try:
            url = self.url
            if not url.endswith("/"):
                url += "/"
            if self.useHashfuscate:
                url += "x"
            if processed:
                url += "namep/"
            else:
                url += "name/"
            if self.useHashfuscate:
                name = hashfuscate.encode(name)
            url += name

            if self.timeout:
                f = self.opener.open(url, timeout=timeout)  # "with" not available
            else:
                f = self.opener.open(url)

            data = f.read()
            try:
                f.close()
            except:
                pass
            if data.startswith('{"ERROR": "Name does not seem to exist."}'):
                return {}  # could also use exception
            if data.startswith('{"ERROR":'):
                raise NmcApiError(data)
            if self.useHashfuscate:
                data, h = hashfuscate.decode(data, returnHash=True)
            jData = json.loads(data)
        except:
            raise NmcApiError(traceback.format_exc())
        return jData

    def get_name_show(self, name):
        return self.get_name(name, processed=False)

    def get_name_processed(self, name):
        return self.get_name(name, processed=True)

if __name__ == "__main__":
    url = "https://api.namecoin.org/beta1"
    #url = "http://localhost:8080/beta1"
    nmcApiOpener = NmcApiOpener(url)

    print "get_name_show d/nx:", nmcApiOpener.get_name_show("d/nx"), "\n"
    print "get_name_show d/nameid:", nmcApiOpener.get_name_show("d/nameid"), "\n"
    print "get_name_processed d/nameid:", nmcApiOpener.get_name_processed("d/nameid")
