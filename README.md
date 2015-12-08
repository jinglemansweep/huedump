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

To view lights in a formatted table, use the ```lights``` action:

```
$ huedump lights
```