#!/bin/bash

if [ $# -lt 1 ]; then
	echo ""
	echo "This script will compare the current name server's of a domain to a provided list of name servers and email you if they do not match."
	echo "--- Incorrect Syntax ----"
	echo "Usage: $0 <domain> <list of name servers> <email address>"
	echo "Example: $0 constellix.com ns.txt username@example.com"
	echo ""
	exit
fi


IFS=$'\n' read -d '' -r -a listedNS < $2 #read file to array
NAMESERVERS=(`dig ns $1 @f.root-servers.net +trace +noanswer | grep $1 | grep 'IN\sNS' | awk '{print $5}' | sort | uniq`) #get domain's name server and read to array
diff=$(diff <(printf "%s\n" "${NAMESERVERS[@]}") <(printf "%s\n" "${listedNS[@]}")) #compare arrays
if [[ -z "$diff" ]]; then
	exit
else
    echo "The domain $1 has had a change in name servers. The current name server's are ${NAMESERVERS[@]}" | mail -s "Name server change on domain $1" $3 #send email
fi