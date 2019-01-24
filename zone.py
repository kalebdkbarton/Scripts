#! /usr/bin/python
import sys
file=sys.argv[1]
if (file == ""):
    print ("")
    print ("This script will turn a zone file into the correct format for DNS Made Easy.")
    print ("--- Incorrect Syntax ----")
    print ("Usage: zone <zone file>")
    print ("Example: zone dnsmadeeasy.txt")
    print ("Example: zone constellix.txt")
    print ("")
    print (file)