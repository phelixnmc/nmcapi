# -*- coding: utf-8 -*-

import json
import traceback

class NameProcess(object):
    def __init__(self, maxImports=7, debug=False):
        self.imports = maxImports  # total number of imports executed for processing
        self.debug = debug

    def get_name_show(self, key):
        """Hook to be replaced. Should return a dict of name_show data."""
        raise Exception("get_name_show hook not set")

    def get_value(self, key=None, data=None):
        """returns a dict if possible, otherwise (unicode)string"""
        if data == None:
            data = self.get_name_show(key)
        value = data["value"]
        try:
            value = json.loads(value)
        except ValueError:
            pass
        if self.debug:
            print "get_value:value:", type(value), value
        return value

    def get_name_processed(self, key):
        data = self.get_name_show(key)
        data["value"] = self.get_value(key=None, data=data)
        if type(data["value"]) == dict:
            data["value"] = self._name_process_recurse(data["value"])
        return data

    def _name_process_recurse(self, data):
        """process 'import' on the given JSON object"""
        # modelled after nmcontrol's pluginData.py
        # lower level imports ?
        # ping pong imports?
        if self.debug:
            print "Processing import for", type(data), data
        if self.imports <= 0:
            data.update({"ERROR" : "name_process: Too many recursive calls."})
            return data
        if type(data) != dict:
            data.update({"ERROR" : "name_process: Import JSON decode failed."})
            return data
        if 'import' in data:
            impName = data['import']
            if self.debug:
                print "Recursing import on", impName
            try:
                impData = self.get_value(key=impName)
            except namerpc.NameDoesNotExistError:
                impData = {"ERROR" : "Name to import does not seem to exist."}
            self.imports -= 1
            impData = self._name_process_recurse(impData)
            data.update(impData)
            if not "ERROR" in data:
                data.pop("import")
        return data

if __name__ == "__main__":

    import namerpc
    import pprint

    class MyNameProcess(NameProcess):
        def __init__(self):
            NameProcess.__init__(self)
            self.rpc = namerpc.CoinRpc()
            pprint.pprint(self.rpc.call("getinfo"))
            print

        def get_name_show(self, key):
            data = self.rpc.nm_show(key)
            if self.debug:
                print "get_name_show:data:", type(data), data
            return data

    mnp = MyNameProcess()
    print "get_name_show:"
    pprint.pprint(mnp.get_name_show("d/nameid"))
    print

    print "get_name_processed:"
    pprint.pprint(mnp.get_name_processed("d/nameid"))
    print


