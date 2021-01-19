# Welcome! The purpose of this script is to verify if the nameservers set at the domain registry match those of your 'Ideal Name Servers'. 
#
# 1) Populate your list of domains on your desktop in a file called domains.txt
# 2) Set your array of Ideal Name Servers (The authorative list you want all your domains to have)
# 3) Run!
#
#


$DomainFile = "$env:USERPROFILE\Desktop\domains.txt"
$DomainArray = Get-Content -Path $DomainFile
$LoopIncrement = 1
$IdealNameServers = ('ns0.dnsmadeeasy.com','ns1.dnsmadeeasy.com','uz5c0c3s8l2rl9wzv47ju3fxnk8l4ly0r56j888sg6nqrmy0db4mn2.b.ast.ns.buddyns.com','uz5c0c3s8l2rl9wzv47ju3fxnk8l4ly0r56j888sg6nqrmy0db4mn2.c.ast.ns.buddyns.com')


Clear #I like a clear at the beginning, especially while debugging but this can be commented out.

foreach ($Domain in $DomainArray) {

$BodgeLineValue = $DomainArray.Count #This is here because I couldn't work out why in the Write-Progress if I referenced $DomainArray.Count it would give me the list of domains rather than the index of the current domain!?
Write-Progress -Activity "Checking Domain $Domain [$LoopIncrement of $BodgeLineValue]" -PercentComplete (($LoopIncrement*100)/$DomainArray.Count) -CurrentOperation $LoopIncrement #Needed to get the progress divided by domain count to have it as a percentage.
$LoopIncrement ++ 
$QueriedNameservers = Resolve-DnsName $Domain -Type NS -DnsOnly

if($Results = @(Compare-Object -ReferenceObject $IdealNameServers -DifferenceObject $QueriedNameservers.NameHost -PassThru)){
    write-host $Domain "Not OK - DNS is returning:" $QueriedNameservers.NameHost -ForegroundColor Red
    #pause
    }
    else {write-host $Domain "is OK"
    }

}