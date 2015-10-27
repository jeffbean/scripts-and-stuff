#!/bin/bash

ssh root@$1 "ipmitool lan set 1 ipsrc static && ipmitool lan set 1 ipaddr $2 && ipmitool lan set 1 defgw ipaddr $3 && ipmitool lan set 1 netmask 255.255.254.0"
