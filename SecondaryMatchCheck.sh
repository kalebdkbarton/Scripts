#!/bin/bash
if [ $# -lt 1 ]; then
	echo ""
	echo "This script will compare a list of domains to see if the SOAs match at the primary and secondary DNS provider."
	echo "--- Incorrect Syntax ----"
	echo "Usage: ./SecondaryMatchCheck.sh <file of domain(s)> <primary dns server> <secondary dns server>"
	echo "Example: ./SecondaryMatchCheck.sh domainlist.txt ns5.dnsmadeeasy.com ns1.mydnsserverexample.com"
	echo "Example: ./SecondaryMatchCheck.sh domainlist.txt ns5.dnsmadeeasy.com 10.10.10.10"
	echo ""
	exit
fi

for domain in `grep -v ^# $1 | awk '{print $1}'`;do #iterate file line by line for domain
    primary=`dig $domain soa @$2 +short | awk '{print $3}'` #get SOA from primary
    secondary=`dig $domain soa @$3 +short | awk '{print $3}'` #get SOA from secondary
    if [[ $primary != $secondary ]]; then #comapare SOAs
        echo $domain #print domains with SOAs that do not match
    fi
done