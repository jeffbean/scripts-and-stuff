#!/usr/bin/env python
# coding=utf-8
import sys
from twisted.internet import defer, protocol
from twisted.names import dns, server, client, cache
from twisted.application import service, internet
from twisted.python import log

DNS_NAMESERVERS = [("10.21.223.53", 53), ("10.21.223.54", 53), ("10.21.223.55", 53)]


class MyProtocol(protocol.Protocol):
    def connectionMade(self):
        log.msg("connection from: ", self.transport.getPeer())


class DNSResolver(client.Resolver):
    def __init__(self, servers):
        client.Resolver.__init__(self, servers=servers)

    def lookupAddress(self, name, timeout=None):
        """
        Lets try to lookup in the DB for any physname +  domain

        """
        return self._lookup(name, dns.IN, dns.A, timeout)

    def lookupIPV6Address(self, name, timeout=None):
        """
        Lets try to lookup in the DB for any physname +  domain

        """
        return self._lookup(name, dns.IN, dns.AAAA, timeout)


# App name, UID, GID to run as. (root/root for port 53 bind)
application = service.Application('db_driven_dns', 1, 1)

# Set the secondary resolver
db_dns_resolver = DNSResolver(DNS_NAMESERVERS)

# Create the protocol handlers
f = server.DNSServerFactory(caches=[cache.CacheResolver()], clients=[db_dns_resolver])
p = dns.DNSDatagramProtocol(f)
f.noisy = p.noisy = False

# Register as a tcp and udp service
ret = service.MultiService()
PORT = 53

for (klass, arg) in [(internet.TCPServer, f), (internet.UDPServer, p)]:
    s = klass(PORT, arg)
    s.setServiceParent(ret)

# Run all of the above as a twistd application
ret.setServiceParent(service.IServiceCollection(application))

if __name__ == "__main__":
    # If called directly, instruct the user to run it through twistd
    if __name__ == '__main__':
        print "Usage: sudo twistd -y %s (background) OR sudo twistd -noy %s (foreground)" % (sys.argv[0], sys.argv[0])