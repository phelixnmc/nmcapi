# -*- coding: utf-8 -*-

# todo: error handling (name not found, / no data source)
#  block height

import namerpc
import traceback
import json
import os
import nameprocess
import sys
import hashfuscate
from bottle import route, run, default_app, request

### Options ###
basePath = "/beta1"
suffixJson = ".json"
serverDatadir = "/home/namecoin/.namecoin"
defaultPort = 8080  # can be set via command line: -port=
timeout = 0.1  # seconds
debug = True
###############

### Globals ###
public = None  # can be set via command line
port = None
datadir = None if os.name == "nt" else serverDatadir
standalone = None
lenSuffixJson = len(suffixJson)
useWaitress = None
rpcOptions = namerpc.CoinRpc(connectionType="client",
                             datadir=datadir).options  # cache looked up rpc options
###############

class MyNameProcess(nameprocess.NameProcess):
    def __init__(self, debug):
        nameprocess.NameProcess.__init__(self, debug=debug)
        
        # instantiate session rpc (relatively fast)
        self.rpc = namerpc.CoinRpc(connectionType="client", options=rpcOptions,
                                   timeout=timeout)
        
    def get_name_show(self, key):
        data = self.rpc.nm_show(key)
        if self.debug:
            print "get_name_show:data:", type(data), data        
        return data

##def _name(key, processed):
##    if key.endswith(suffixJson):
##        key = key[:-lenSuffixJson]
##    mnp = MyNameProcess(debug=debug)
##    try:
##        if processed:
##            data = mnp.get_name_processed(key)
##        else:
##            data = mnp.get_name_show(key)
##        return json.dumps(data, separators=(',', ':'))
##    except namerpc.NameDoesNotExistError:
##        return {"ERROR" : "Name does not seem to exist."}
##    except:
##        return {"ERROR" : "Internal Error" +
##                (": " + traceback.format_exc() if debug else "")}
##
##@route(basePath + '/name/<key:path>')
##def name(key):
##    """Return raw value data."""
##    return _name(key, processed=False)
##
##@route(basePath + '/namep/<key:path>')
##def namep(key):
##    """Return raw value data."""
##    return _name(key, processed=True)

def _xname(x, processed):
    try:
        key = hashfuscate.decode(x)
    except hashfuscate.HashfuscateDecodeError as e:
        return {"ERROR" : "HashfuscateDecodeError: " + str(e)}
    mnp = MyNameProcess(debug=debug)
    try:
        if processed:
            data = mnp.get_name_processed(key)
        else:
            data = mnp.get_name_show(key)
        s = json.dumps(data, separators=(',', ':'))        
        return hashfuscate.encode(s)
    except namerpc.NameDoesNotExistError:
        return {"ERROR" : "Name does not seem to exist."}
    except namerpc.RpcConnectionError:
        return {"ERROR" : "RPC connection error" +
                (": " + traceback.format_exc() if debug else "")}
    except:
        return {"ERROR" : "Internal Error" +
                (": " + traceback.format_exc() if debug else "")}

@route(basePath + '/xname/<x:path>')
def xname(x):
    """Return raw value data."""
    return _xname(x, processed=False)

@route(basePath + '/xnamep/<x:path>')
def xnamep(x):
    """Return processed value data."""
    return _xname(x, processed=True)

# command line options
for arg in sys.argv:
    if arg.startswith("-port="):
        port = arg.split("=")[1]
        break
if port == None:
    port = defaultPort
    
if "-waitress" in sys.argv:
    useWaitress = True

if "-public" in sys.argv:
    if debug:
        raise Exception("Both public and debug flags set.")
    public = True

print "public:", public
print "port:", port
print "waitress:", useWaitress
print "basePath:", basePath
print "timeout:", timeout

if 1:
    if public:
        host = "0.0.0.0"
    else:
        host = "127.0.0.1"
    if useWaitress:
        # waitress to improve server performance
        bottleApp = default_app()
        from waitress import serve
        serve(bottleApp, host=host, port=port)
    else:        
        run(host=host, port=port)

else:
    standalone = True
    print "hashfuscate 'd/nx':", hashfuscate.encode("d/nx")
    print "xname d/nx:\n", xname(hashfuscate.encode("d/nx"))
    print "xname d/nameid:\n", xname(hashfuscate.encode("d/nameid"))
    print "xnamep d/nameid:\n", xnamep(hashfuscate.encode("d/nameid"))
