#!/bin/bash

# Instructions
if [ $# -lt 1 ]; then
    echo ""
    echo "This script will turn a zone file into the correct format for DNS Made Easy."
    echo "--- Incorrect Syntax ----"
    echo "Usage: zone <zone file>"
    echo "Example: zone dnsmadeeasy.txt"
    echo "Example: zone constellix.txt" 
    echo ""
    exit
fi

# Get the domain
echo "What is the domain?"
read DOMAIN

# Add the $ORIGIN if needed
OR="$(grep ORIGIN $1)"
if [ $OR ]; then
    sed -i '1s/^/$ORIGIN $OR /' $1
fi

# Remove the domain and add the 'IN'
input="$1"
while IFS= read -r x; do
    if [[ x != *"ORIGIN"* ]]; then
       sed -i '/$DOMAIN/c\@' $1
    fi
    if [[ x == *"SOA"* ]]; then
        RECORDTYPE="SOA"
    elif [[ x == *"A"* ]]; then
        RECORDTYPE="A"
    elif [[ x == *"CNAME"* ]]; then
        RECORDTYPE="A"
    elif [[ x == *"TXT"* ]]; then
        RECORDTYPE="TXT"
    elif [[ x == *"SPF"* ]]; then
        RECORDTYPE="SPF"
    elif [[ x == *"MX"* ]]; then
        RECORDTYPE="MX"
    elif [[ x == *"CAA"* ]]; then
        RECORDTYPE="CAA"
    elif [[ x == *"PTR"* ]]; then
        RECORDTYPE="PTR"
    elif [[ x == *"SRV"* ]]; then
        RECORDTYPE="SRV"
   # if [[ x == *"SOA"* ]] || if [[ x == *"A"* ]] || if [[ x == *"CNAME"* ]] || if [[ x == *"TXT"* ]] || if [[ x == *"SPF"* ]] || if [[ x == *"MX"* ]] || if [[ x == *"NS"* ]] || if [[ x == *"CAA"* ]] || if [[ x == *"PTR"* ]] || if [[ x == *"SRV"* ]] && if ![[ x == *"IN"* ]]; then
   #    sed -i 's/$RECORDTYPE/IN   $RECORDTYPE/g'
   # fi
    echo $x
done < "$input"
