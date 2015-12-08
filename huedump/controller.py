import json
import os
import sys
from collections import OrderedDict
from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler
from jinja2 import Environment, FileSystemLoader
from phue import Bridge
from prettytable import PrettyTable as Table
from pygments import highlight, lexers, formatters


class Controller(CementBaseController):

    class Meta:
        label = "base"
        description = "Hue Dump"
        arguments = [
            (["-b", "--bridge"],
              dict(action="store", help="hostname of Hue bridge")),
            (["-u", "--user"],
              dict(action="store", help="username of Hue user")),
            (["-t", "--template"],
              dict(action="store", help="template for output rendering", default="")),
            ]


    @expose(help="Dump the configuration and state of the bridge")
    def dump(self):
        self.login()
        self.app.log.info(self.format_json(self.api))

    @expose(help="Display a summary of lights registered on the bridge")
    def lights(self):
        self.login()
        lights = self.sort_dict(self.api.get("lights"))
        rows = [[i, 
                 l.get("name"), 
                 l.get("_alias"),
                 l.get("manufacturername"),
                 l.get("modelid"),
                 "ON" if l.get("state").get("on") else "",
                 l.get("state").get("bri", ""),
                 l.get("state").get("colormode", ""),
                 l.get("state").get("hue", ""),
                 l.get("state").get("sat", "")
                ] for i, l in lights.iteritems()]
        t = self.table(["#", "Name", "Alias", "Manu", "Model", "On", "Bri", "CM", "Hue", "Sat"], rows)
        self.app.log.info(t)
            
    @expose(help="Render state using a template")
    def render(self):
        self.login()
        tpl = self.template(self.app.pargs.template, self.api)
        print(tpl)

    @expose(hide=True)
    def login(self):
        host = self.app.pargs.bridge or self.app.config.get("bridge", "host")
        user = self.app.pargs.user or self.app.config.get("bridge", "user")
        self.bridge = Bridge(host, user)
        self.bridge.connect()
        try:
            self.api = self.bridge.get_api()
        except Exception, e:
            if e.errno == -2:
                self.app.log.error("Invalid bridge host")
            sys.exit(1)
        self.add_metadata()

    @expose(hide=True)
    def add_metadata(self):
        aliases = dict(self.app.config.items("aliases"))
        for idx, light in sorted(self.api.get("lights").items()):
            ref = "light{}".format(idx)
            val = aliases.get(ref) if ref in aliases else light.get("name")
            self.api.get("lights").get(idx)["_alias"] = val
            
    @expose(hide=True)
    def sort_dict(self, d):
        return OrderedDict(sorted(d.items()))

    @expose(hide=True)
    def table(self, fields, rows):
        table = Table(fields)
        for row in rows:
            table.add_row(row)
        table.align = "l"
        return "\n{}".format(table)

    @expose(hide=True)
    def template(self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        return Environment(
            loader=FileSystemLoader(path or "./")
        ).get_template(filename).render(context)

    @expose(hide=True)
    def format_json(self, json_value):
        return highlight(
            unicode(json.dumps(json_value, indent=4, sort_keys=True), "UTF-8"),
            lexers.JsonLexer(),
            formatters.TerminalFormatter()
        )