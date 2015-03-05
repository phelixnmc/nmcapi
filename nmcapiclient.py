# -*- coding: utf-8 -*-

#apiUrl = "http://localhost:8080/beta1"
apiUrl = "https://api.namecoin.info/beta1"
useHashfuscate = True
timeout = 3  # seconds

import ssl
import urllib2
import hashfuscate
import json
import os
import traceback

class NmcApiError(Exception):
    pass

if not apiUrl.startswith("http://"):
    try:
        sslContext = ssl.create_default_context()
    except AttributeError:
            raise NmcApiError("httpS:// connection not available. " +
                              "Upgrade to a newer Python version "+
                              "or change API URL to plain http://")
    opener = urllib2.build_opener(urllib2.HTTPHandler(),
                              urllib2.HTTPSHandler(context=sslContext))
else:
    opener = urllib2.build_opener(urllib2.HTTPHandler())

opener.addheaders = [('User-agent', 'nmcapiclient 100 ' + str(os.name))]

def get_name(name, processed=True):
    try:
        url = apiUrl + "/"
        if useHashfuscate:
            url += "x"
        if processed:
            url += "namep/"
        else:
            url += "name/"
        if useHashfuscate:
            name = hashfuscate.encode(name)
        url += name
        f = opener.open(url, timeout=timeout)  # "with" not available
        data = f.read()
        try:
            f.close()
        except:
            pass
        if useHashfuscate:
            data, h = hashfuscate.decode(data, returnHash=True)
        jData = json.loads(data)
    except:
        raise NmcApiError(traceback.format_exc())
    return jData

def get_name_show(name):
    return get_name(name, processed=False)

def get_name_processed(name):
    return get_name(name, processed=True)

if __name__ == "__main__":
    print "get_name_show d/nx:", get_name_show("d/nx"), "\n"
    print "get_name_show d/nameid:", get_name_show("d/nameid"), "\n"
    print "get_name_processed d/nameid:", get_name_processed("d/nameid")
