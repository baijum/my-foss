---
layout: single
title: Windows Commands
date: 2014-04-09
categories: technology
---

I had kept these notes in a private wiki page for sometime.
I hope moving it here will be helpful for searching.

### Deleting a Service

`sc delete servicename`

To get name of the service that need to be deleted:

1. Run `services.msc`
1. Right click and get the service name


### Checking whether a port is listening or not

`netstat -na|find "PORTNUMBER"`

### To see all ports listening

`netstat -na|find "LISTENING"`

### To check a service is started or not

`net start|find "C:\Path\to\program"`

### Commenting in batch file

Use `::` or `REM` followed by a space

Example:-

{% raw %}
```
:: this is a comment
REM this is another comment
```
{% endraw %}

### Call a batch program inside another batch file

`call <script.bat>`

### Query and remove terminal server sessions

Use `qwinsta` and `rwinsta` commands.

Example:-

{% raw %}
```
qwinsta /SERVER:IP
rwinsta /SERVER:IP
```
{% endraw %}

### Check uptime of machine

`net statistics server | find "since"`

### Run as different user

`runas`

