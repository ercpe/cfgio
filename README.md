cfgio
=====

cfgio is a python library for reading and writing configuration file formats found on a *nix system. The core goal is to provide an r/w API to files in different formats and still maintaining the overall layout (comments, structure) of the files.


## Why?
Because i often need to read and write configuration files on systems. Typically i `open` the file, read it and use a mix of string functions and regular expression to extract the values i need. When it comes to writing configuration files things get nasty. Have you ever tried to diff a config which has been re-written by a program?

# Examples

**Reading entries from /etc/fstab**

	from cfgio import fstab
	fstab = fstab.FstabConfig('/etc/fstab')
	print(fstab.get('/dev/sda2'))

	/dev/sda2 on /boot (ext4), opts: noatime,discard (1/2)


** Reading Xen domU configurations **

    from cfgio.specialized import xen
    cfg = xen.XenConfig('/etc/xen/test.cfg')
    print(cfg.get('memory').value)
    >> 1024
    print(cfg.get('vif').value)
    >> [<cfgio.specialized.xen.XenDomUVifConfigValue object at 0x25e6210>]


# Attention: work in progress

cfgio is far away from being a full-featured library. Some important features are still missing:

* no multiline support. cfgio will skip subsequent lines and mark them as garbage
* cfgio does not uncomment variables. Instead it will add a new line to the file
* Reading bash "configs" using a KeyValueConfig may lead into suprising result. `cfgio` does not handle this very well, e.g. splitting up variable assignments into multiple lines.
* ...