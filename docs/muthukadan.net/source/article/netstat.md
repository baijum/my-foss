---
title: Netstat
layout: single
permalink: /article/netstat.html
---

## Netstat on Windows

To see listening connections:

```
netstat

```

To see all connections:

```
netstat -a
```

To see network statistics:

```
netstat -e
netstat -s
```

To filter output based on protocols:

```
netstat -p TCP
netstat -p UDP
netstat -p ICMP
netstat -p TCPv6
netstat -p UDPv6
```

To see routing table:

```
netstat -r
```

To see the result in every N seconds:

```
netstat N
```

To see the process name:

```
netstat -b
```

To see the foreign IP address:

```
netstat -n
```

To see the process ID:

```
netstat -o
```

To see the [offload] state:

```
netstat -t
```

[offload]: http://blogs.technet.com/b/brad_rutkowski/archive/2007/08/10/how-to-know-if-tcp-offload-is-working.aspx

## Netstat on GNU/Linux

TBD

[GNU/Linux netstat examples](http://www.binarytides.com/linux-netstat-command-examples/)
