nmcAPI
======

API server for Namecoin names.


Features
=======
Handles imports.
Requests and output are obfuscated (nothing is encrypted for now).
Fetching uncached data takes about a millisecond. This is a bottleneck.
All caching is done in Nginx (10 minutes).
Cached responses should be super fast
Rate limiting in Nginx
namecoind and backend run supervisord


Dependencies
==========
bottle:
    pip install bottle

waitless (optional, to improve performance):
    pip install waitless

How to use
=========
Start a local server:
    python ./nmcapi.py -debug -port=8080
Start a public server:
    python ./nmcapi.py -public

See nmcapiclient.py on how to do lookups. Currently the server can be used with nmcontrol-hyperion and hopefully soon with official nmcontrol.


Performance & Stability
==================
For anything else than personal use the server should run through waitless and nginx and be managed by supervisord. Config files for nginx and to set up supervisord are included. For security you might want to set up a separate user account.


ToDo
====
help at root url (automated via route function?)
improve https handling
check https fingerprint for self signed certs
new query: current block height / block time
serve block headers to improve security
  - for name_op
  - for current height
harden against ddos


License
=======
LGPL unless it says otherwise in the source file.
