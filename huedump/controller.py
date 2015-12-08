import json
from collections import OrderedDict

from cement.core.foundation import CementApp
from cement.core.controller import CementBaseController, expose
from cement.core import handler

from phue import Bridge
from prettytable import PrettyTable as Table
from pygments import highlight, lexers, formatters


# b5f093b1388368f39ac904310ef6817

class Controller(CementBaseController):

    class Meta:
        label = "base"
        description = "Hue Dump"
        arguments = [
            (["-b", "--bridge"],
              dict(action="store", help="hostname of Hue bridge")),
            (["-u", "--user"],
              dict(action="store", help="username of Hue user")),
            (["-t"],
              dict(action="store", help="output template")),
            ]

    @expose(help="Dump")
    def dump(self):
        self.app.log.info("Dump")
        self.login()
        self.app.log.info(self.format_json(self.bridge.get_api()))
        print(self.app.config.get("bridge", "host"))

    @expose(help="Lights")
    def lights(self):
        self.app.log.info("Lights")
        self.login()
        lights = self.sort_dict(self.api().get("lights"))
        rows = [[i, l.get("name"), l.get("modelid")] for i, l in lights.iteritems()]
        t = self.table(["Idx", "Name", "Model"], rows)
        self.app.log.info(t)
            
    @expose(hide=True)
    def login(self):
        host = self.app.pargs.bridge or self.app.config.get("bridge", "host")
        user = self.app.pargs.user or self.app.config.get("bridge", "user")
        self.bridge = Bridge(host, user)
        self.bridge.connect()

    @expose(hide=True)
    def api(self):
        return self.bridge.get_api()

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
    def format_json(self, json_value):
        return highlight(
            unicode(json.dumps(json_value, indent=4, sort_keys=True), "UTF-8"),
            lexers.JsonLexer(),
            formatters.TerminalFormatter()
        )