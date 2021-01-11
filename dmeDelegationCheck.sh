#!/bin/bash

if [ $# -lt 1 ]; then
	echo ""
	echo "This script will run a list of domains against their respective TLD's and show the ones not delegate to dnsmadeeasy."
	echo "--- Incorrect Syntax ----"
	echo "Usage: tldns <file of domains>"
	echo "Example: tldns dnsmadeeasy.txt"
	echo ""
	exit
fi

for x in `grep -v ^# $1 | awk '{print $1}'`; do
	NAMESERVERS=`dig ns $x @f.root-servers.net +trace +noanswer | grep $x | grep 'IN\sNS' | awk '{print $5}' | sort | uniq`
	if [[ "$NAMESERVERS" != *"dnsmadeeasy"* ]]; then
        echo "$x is not delegated to DNS Made Easy. Nameservers are:"
        echo "$NAMESERVERS"
        echo
    fi
done