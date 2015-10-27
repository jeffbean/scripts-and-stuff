# tried but failed
[jbean@jbean ~/centos]$ export RSYNC_PROXY=http://rproxy.mcp.com:3128
[jbean@jbean ~/centos]$  rsync --progress  -av --delete --delete-excluded --exclude "local*" --exclude "isos" --exclude "i386"  rsync://mirrors.kernel.org/centos/7.0/ /repo/centos/7.0/
rsync: getaddrinfo: http //rproxy.: Servname not supported for ai_socktype
rsync error: error in socket IO (code 10) at clientserver.c(122) [Receiver=3.0.9]

