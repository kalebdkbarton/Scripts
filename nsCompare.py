import sys, socket
import dns.resolver, dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *
import requests
import json

def slackMessage(domain, message):
    #setup bot here https://api.slack.com/authentication/basics
    slack_token = ''
    slack_channel = ''
    slack_icon_url = ''
    slack_user_name = ''
    

    def post_message_to_slack(text, blocks = None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': slack_token,
            'channel': slack_channel,
            'text': text,
            'icon_url': slack_icon_url,
            'username': slack_user_name,
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    #If you want it to tag someone, add <@user> to string
    post_message_to_slack('Error in domain {}\n{}'.format(domain,message))

def main():
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
    slackoutput=""
    for (name, rdataset) in z.iterate_rdatasets():
        if rdataset.rdtype == SOA:
            continue
        if rdataset.rdtype == NS and str(domain+".")==str(name):
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
            slackoutput += "\n(MIS-MATCH) query: %s" % name + "\n"
            if result != None and len(result) > 1:
                slackoutput += "Expected:" + "\n"
                slackoutput += str(rdataset) + "\n"
                slackoutput += "Received: " + "\n"
                slackoutput += str(result) + "\n"
            else:
                slackoutput += "Expected: "+ str(rdataset) + "\n"
                slackoutput += "Received: "+ str(result) + "\n"
            mismatches += 1
    slackoutput += "\nResults:" + "\n"
    slackoutput += "Matches:       "+ str(matches) + "\n"
    slackoutput += "Mis-matches:   "+ str(mismatches) + "\n"
    if mismatches>0:
        slackMessage(domain, slackoutput)


main()