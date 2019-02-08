#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import sys
zone=sys.argv[1] #set file to first argument
origin=sys.argv[2] #set origin to second argument
originDot = (origin+".")
dotOrigindot = ("."+origin+".") #all variations found
if "ORIGIN" not in zone:
    f = open('zone.json','w')
    f.write("$ORIGIN "+origin) #add the origin
    f.close()
fh = open(zone)
for line in fh: #run file line by line
    if ";" in line: #remove comments
        continue
    if "ORIGIN" not in line: #remove the origin domain from the FQDN
        removeDomain1 = line.replace(dotOrigindot, "")
        removeDomain2 = removeDomain1.replace(originDot, "@")
        removeDomain3 = removeDomain2.replace(origin, "@")
    else:
        continue #don't output if $ORIGIN is in the line
    if "SOA" in line:
        continue #get rid of the SOA
    elif "CNAME" in line:  #all of these grab the record type or lack thereof
        recordType="CNAME"
    elif "A" in line:
        recordType="A"
    elif "TXT" in line:
        recordType="TXT"
    elif "SPF" in line:
        recordType="SPF"
    elif "MX" in line:
        recordType="MX"
    elif "CAA" in line:
        recordType="CAA"
    elif "PTR" in line:
        recordType="PTR"
    elif "SRV" in line:
        recordType="SRV"
    elif "NS" in line:
        recordType="NS"
    else:
        recordType="none"
    if (recordType != "none"):
        if "IN" not in line:
            withIn = ("IN\t"+recordType) 
            output = removeDomain3.replace(recordType, withIn) #add the IN
        else:
            output = removeDomain3 #IN is already there
    else:
        continue
    if (recordType == "NS"):
        if "@" in output: #get rid of the root NS Records
            continue
    if (recordType == "CNAME"): #no root CNAME Records
        if "@" in output:
            f = open('zone.json','w')
            f.write("\033[1;31;40m ERROR: CANNOT HAVE CNAME FOR THE ROOT DOMAIN  \n")
            f.close()
            break
    if (recordType == "SRV"): #no root SRV Records
        if "@" in output:
            f = open('zone.json','w')
            f.write("\033[1;31;40m ERROR: CANNOT HAVE SRV FOR THE ROOT DOMAIN  \n")
            f.close()
            break
    if line.strip(): #no blank lines
        f = open('zone.json','a')
        f.write(output) #write output to file
        f.close()
fh.close()
