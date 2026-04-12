---
layout: post
title: Setting up OpenVPN on AWS
date: 2014-04-10
categories: technology
---

I had kept these notes in a private wiki page for sometime.
I hope moving it here will be helpful for searching.

### Create and upload RSA public key for SSH access

By deafult, most of the Amazon Linux machines are accessed through SSH
using a public key.

### Create a VPC with public and private sub-nets

Next step is to create a VPC with a unique CIDR.  While choosing CIDR,
you need to discuss with network admins, otherwise you may mess around
with the network topology in the organization.

I created a VPC with a public subnet and private subnet.  Amazon only
allows to use the public subnet for static IPs (EIP in AWS).  I choose
something like this:

* CIDR: 10.107.0.0/16
* Public sub-net: 10.107.0.0/24
* Private sub-net: 10.107.1.0/24

This step will automatically creates a NAT box (Linux) automatically
with a static IP (EIP).  This machine is used for NATing from public
subnet and private subnets.  I am going to use the same box as my
OpenVPN server.

### Create Security Group named "OpenVPNSG" for VPC

Change the NAT box SG to "OpenVPNSG".

In the security group, you can specify the inbound and outbound rules
for the network traffic.

I allowed access to port 1194 for UDP from everywhere (0.0.0.0/0)
which I will change to our public IP addresses when we are going to
add something real in the cloud.  I also enable access to port 22 for
SSH from everywhere.

### Update machine with latest updates and install openvpn package

Login to the machine and run:

{% raw %}
```
yum update
yum install openvpn make
```
{% endraw %}

### Creat server and client X.509 certificates

OpenVPN comes with something called "easy-rsa" for managing X.509 certificates

The steps were something like this:

{% raw %}
```
cd /usr/share/openvpn/easy-rsa/2.0/
make install DESTDIR=/etc/openvpn/rsa
cd /etc/openvpn/rsa
vim vars #edit this file (last few lines)
source ./vars
./clean-all
./build-dh
./pkitool --initca
./pkitool --server server
./pkitool client1
```
{% endraw %}

Copy the ca.crt, client1.crt & client1.key to the client machine

### Create openvpn configuration

{% raw %}
```
cp /usr/share/doc/openvpn-2.1.4/sample-config-files/server.conf /etc/openvpn/openvpn.conf
```
{% endraw %}

vim /etc/openvpn/openvpn.conf

{% raw %}
```
ca /etc/openvpn/rsa/keys/ca.crt
cert /etc/openvpn/rsa/keys/server.crt
key /etc/openvpn/rsa/keys/server.key

dh /etc/openvpn/rsa/keys/dh1024.pem
```
{% endraw %}

Add this line also to revoke certificates
{% raw %}
```
crl-verify /etc/openvpn/rsa/keys/crl.pem

push "route 10.107.0.0 255.255.255.0"
push "route 10.107.1.0 255.255.255.0"
```
{% endraw %}

Add client to client access
http://openvpn.net/index.php/open-source/documentation/howto.html

{% raw %}
```
client-config-dir ccd
route 192.168.1.0 255.255.255.0
client-to-client
push "route 192.168.1.0 255.255.255.0"
```
{% endraw %}

### Create client to client access file

For client to client access created folder named "ccd"

{% raw %}
```
mkdir /etc/openvpn/ccd
cd /etc/openvpn/ccd
echo "iroute 192.168.1.0 255.255.255.0" > client1
```
{% endraw %}

### Update IP Tables with IP masquerade

vim /etc/sysconfig/iptables

{% raw %}
```
*nat
:POSTROUTING ACCEPT [0:0]
:PREROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A POSTROUTING -s 192.168.2.0/24 -d 0.0.0.0/0 -o eth0 -j MASQUERADE
-A POSTROUTING -s 192.168.1.0/24 -d 0.0.0.0/0 -o eth0 -j MASQUERADE
COMMIT
```
{% endraw %}

start service

{% raw %}
```
chkconfig openvpn on
service openvpn restart

service iptables restart
chkconfig iptables on
```
{% endraw %}

### To revoke certificate:

{% raw %}
```
cd /etc/openvpn/rsa

source ./vars
./revoke-full client2
```
{% endraw %}
