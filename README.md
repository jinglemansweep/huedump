# huedump

Dump Philips Hue lights, groups and scenes configuration and state to multiple formats

## Installation

Checkout the project:

```
$ git clone https://github.com/jinglemansweep/huedump.git
```

(Optional) Create a Python virtual environment and install dependencies:

```
$ virtualenv -p /usr/bin/python2 ~/.virtualenvs/huedump
$ cd /path/to/huedump
$ pip install -r requirements.txt
```

## Running

You can specify the bridge hostname and username as command line arguments:

```
$ huedump --bridge <hostname-of-hue-bridge> --user <bridge-username>
```

You can also use a configuration files (`~/.huedump/config`):

```
[bridge]
host=192.168.1.21
user=a9daa3b1388368f39ac904310ef6817
```

For further help, use the help command:

```
$ huedump --help
```

## Actions

To dump the bridges entire state and configuration, use the ```dump``` action:

```
$ huedump dump
```

```
{ 
  "config": {...},
  "lights": {...},
  ...
}
```

To view lights in a formatted table, use the ```lights``` action:

```
$ huedump lights
```

```
+---+---------------------+---------+--------+----+-----+----+-------+-----+
| # | Name                | Manu    | Model  | On | Bri | CM | Hue   | Sat |
+---+---------------------+---------+--------+----+-----+----+-------+-----+
| 1 | Lounge Lamp Back    | Philips | LWB004 | ON | 21  |    |       |     |
| 2 | Lounge Front        | Philips | LWB004 | ON | 102 |    |       |     |
| 3 | Lounge Colour       | Philips | LLC011 | ON | 202 | xy | 54330 | 253 |
| 4 | Kitchen Colour      | Philips | LLC010 | ON | 164 | xy | 4507  | 178 |
| 5 | Portable Colour     | Philips | LLC020 |    | 5   | hs | 1937  | 0   |
| 6 | Lounge Back Colour  | Philips | LCT001 | ON | 142 | xy | 65527 | 253 |
| 7 | Lounge Front Colour | Philips | LCT001 |    | 33  | xy | 65527 | 253 |
+---+---------------------+---------+--------+----+-----+----+-------+-----+
```

To render output using a [Jinja2](http://jinja.pocoo.org/) template, use the ```render``` action:

```
$ huedump render --template ./templates/openhab.items.j2 > output.txt
```

## Configuration

You can add metadata to all of your lights based on their hubs index number. Metadata values are available
within templates with the respective `_prefix` key which is added to each `lights.*` API value automatically.

The `metadata` example below will set `_ref` and `_groups` values on lights 1, 2 and 3. It will additionally
set a `_brightness` value for light 3.

```
[bridge]
host=192.168.1.21
user=a9daa3b1388368f39ac904310ef6817

[metadata]
ref1=LoungeLampBack
groups1=all,lights,lounge
ref2=LoungeLampFront
groups2=all,lights,lounge
ref3=KitchenBloom
groups3=all,lights,kitchen
brightness3=50
```

### Template Usage

```
{% for idx, l in lights %}
Index:      {{ idx }}
Name:       {{ l.name }}
Ref:        {{ l._ref }}
Groups:     {{ l._groups }}
Brightness: {{ l._brightness }}
```
