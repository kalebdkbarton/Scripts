#!/bin/bash
if [ $# -lt 1 ]; then
	echo ""
	echo "This script will test a domain's DNS resolution on a given name server"
	echo "--- Incorrect Syntax ----"
	echo "Usage: dnstest <domain> <name server>"
	echo "Example: dnstest dnsmadeeasy.com ns1.dnsmadeeasy.com"
	echo ""
	exit
fi
for i in {1..1000}; do 
    dig $1 @$2 | grep "connection timed out"
done