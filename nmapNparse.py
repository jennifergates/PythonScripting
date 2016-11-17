#! /usr/bin/python
import os
import sys

## ensure running as root so nmap scan will work
if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

##  Define Ports to scan for
uports = {'53':'dns','67':'dhcp','69':'tftp','123':'ntp','161':'snmp','164':'radius','165':'radius','166':'radius'};
tports = {'20':'ftp','21':'ftp','22':'ssh','23':'telnet','25':'smtp','49':'tacacs','1741':'ciscoWorks','8787':'solarwinds','1433':'mssql','1521':'oracle','3306':'mysql','5432':'postgres','80':'web80','443':'web443','8080':'web8080','8334':'web8334','8443':'web8443','137':'windows','139':'windows','445':'windows'};

if os.path.exists('./nmap_parsed_files') == 'False':
	mkdir = 'mkdir nmap_parsed_files';
	os.system(mkdir);

## get IP/subnet from command line
targets = "";

while targets == "":
	if len(sys.argv) < 2:
		targets = raw_input('\n\nEnter IP or range to scan in nmap acceptable syntax. \n Example: 192.168.1.0/24  ');
	else: 
		targets = sys.argv[1];

## convert target ip/range to string for filenames
filebase = targets.replace('.','_').replace('/','-');
filebase = 'nmap_parsed_files/'+filebase + "_";
print filebase;


## create nmap command
nmapUstring = 'U:'
nmapTstring = 'T:'
nmapStartstring = 'nmap -T4 -O -sV -sU -sT -p '
nmapEndstring = ' -oA ' + filebase +'discoveryServiceScan'

for port in uports:
	nmapUstring = nmapUstring + port +',';

for port in tports:
	nmapTstring = nmapTstring + port +',';

nmapcommand = nmapStartstring + nmapUstring +nmapTstring[:-1] +' '+ targets + nmapEndstring;
print "\nRunning nmap command:\n %s" % nmapcommand;

## Run nmap command
os.system(nmapcommand);

## Parse results file
alivecommand = "grep 'Up' "+ filebase +"discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> " + filebase +"aliveIPs.txt";
os.system(alivecommand);

for port in uports:
	command = "grep ' " + port +"/open/udp/' "+ filebase +"discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> "+ filebase  + uports[port] +".txt";
	os.system(command);

for port in tports:
	command = "grep ' " + port +"/open/tcp/' "+ filebase +"discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> "+ filebase + tports[port] +".txt";
	os.system(command);


