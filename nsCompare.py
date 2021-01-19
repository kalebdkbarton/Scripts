import sys, socket
import dns.resolver, dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

try:
    domain = sys.argv[1]
    nserver1 = sys.argv[2]
    nserver2 = sys.argv[3]
except:
    print ("This script will compare the same zone on 2 different name servers. AXFR requests will need to be allowed from the first server.")
    print ("----Error: incorrect syntax----")
    print ("Usage: python3 nsCompare.py <domain> <name server 1> <name server 2>")
    print ("Example: python3 nsCompare.py kalebbarton.com axfr2.dnsmadeeasy.com ns11.constellix.com")
    sys.exit(1)

output = dns.zone.from_xfr(dns.query.xfr(nserver1, domain, lifetime=100)) #get axfr report
zone = [output[n].to_text(n) for n in output.nodes.keys()]
with open('zone.tmp', 'w') as f:
    for record in zone:
        f.write(record+"\n")

z = dns.zone.from_file("zone.tmp", domain, relativize=False) #check against the file
r = dns.resolver.Resolver(configure=False)
try:
    r.nameservers = socket.gethostbyname_ex(nserver2)[2]
except socket.error:
    print ("Error: could not resolve 'host' %s" % nserver2)
    sys.exit(2)

#compare
matches=0
mismatches=0
for (name, rdataset) in z.iterate_rdatasets():
    if rdataset.rdtype == SOA:
        continue
    if rdataset.rdtype == NS:
        continue
    match = False
    result = None
    try:
        ans = r.query(name, rdataset.rdtype, rdataset.rdclass)
        result = ans.rrset.to_rdataset()
        if result == rdataset:
            match = True
    except DNSException:
        pass
    if match:
        matches += 1
    else:
        print ("\n(MIS-MATCH) query: %s" % name)
        if result != None and len(result) > 1:
            print ("Expected:")
            print (rdataset)
            print ("Received: ")
            print (result)
        else:
            print ("Expected: ", rdataset)
            print ("Received: ", result)
        mismatches += 1
print ("done")
print ("\nResults:")
print ("Matches:       ", matches)
print ("Mis-matches:   ", mismatches)