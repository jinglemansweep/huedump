# huedump

Dump Philips Hue lights, groups and scenes configuration and state to multiple formats

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
