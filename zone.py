#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import sys
if len(sys.argv) <= 1:
    print ("")
    print ("This script will turn a zone file into the correct format for DNS Made Easy.")
    print ("--- Incorrect Syntax ----")
    print ("Usage: zone <zone file>")
    print ("Example: zone dnsmadeeasy.txt")
    print ("Example: zone constellix.txt")
    print ("")
else:
    zone=sys.argv[1]
    origin = (str(input("What is the origin domain?\n")))
    originDot = (origin+".")
    dotOrigindot = ("."+origin+".")
    print("Here is your fixed zone:\n\n")
    if "ORIGIN" not in zone:
        print ("$ORIGIN "+origin)
    fh = open(zone)
    for line in fh:
        if ";" in line:
            continue
        if "ORIGIN" not in line:
            removeDomain1 = line.replace(dotOrigindot, "")
            removeDomain2 = removeDomain1.replace(originDot, "@")
            removeDomain3 = removeDomain2.replace(origin, "@")
        else:
            output = line
        if "SOA" in line:
            continue
        elif "CNAME" in line:
            RECORDTYPE="CNAME"
        elif "A" in line:
            RECORDTYPE="A"
        elif "TXT" in line:
            RECORDTYPE="TXT"
        elif "SPF" in line:
            RECORDTYPE="SPF"
        elif "MX" in line:
            RECORDTYPE="MX"
        elif "CAA" in line:
            RECORDTYPE="CAA"
        elif "PTR" in line:
            RECORDTYPE="PTR"
        elif "SRV" in line:
            RECORDTYPE="SRV"
        elif "NS" in line:
            RECORDTYPE="NS"
        else:
            RECORDTYPE="none"
        if (RECORDTYPE != "none"):
            if "IN" not in line:
                withIn = ("IN\t"+RECORDTYPE)
                output = removeDomain3.replace(RECORDTYPE, withIn)
            else:
                output = removeDomain3
        else:
            output = removeDomain3 
        if (RECORDTYPE == "NS"):
            if "@" in output:
                continue
        if (RECORDTYPE == "CNAME"):
            if "@" in output:
                print("\033[1;31;40m ERROR: CANNOT HAVE CNAME FOR THE ROOT DOMAIN  \n")
                break
        if (RECORDTYPE == "SRV"):
            if "@" in output:
                print("\033[1;31;40m ERROR: CANNOT HAVE SRV FOR THE ROOT DOMAIN  \n")
                break
        print(output)
    fh.close()
