#!/usr/bin/python
import os
import sys

uports = {'53':'dns','67':'dhcp','69':'tftp','123':'ntp','161':'snmp','164':'radius','165':'radius','166':'radius'};
tports = {'20':'ftp','21':'ftp','22':'ssh','23':'telnet','25':'smtp','49':'tacacs','1741':'ciscoWorks','8787':'solarwinds','1433':'mssql','1521':'oracle','3306':'mysql','5432':'postgres','80':'web80','443':'web443','8080':'web8080','8334':'web8334','8443':'web8443','137':'windows','139':'windows','445':'windows'};

targets = "";

while targets == "":
	if len(sys.argv) < 2:
		targets = raw_input('Enter range to scan. Example: 192.168.1.0/24  ');
	else: 
		targets = sys.argv[1];

nmapUstring = 'U:'
nmapTstring = 'T:'
nmapstring = 'nmap -T4 -O -sV -sU -sT -p '

for port in uports:
	nmapUstring = nmapUstring + port +',';

for port in tports:
	nmapTstring = nmapTstring + port +',';

nmapcommand = 'nmap -T4 -O -sV -sU -sT -p '+nmapUstring +nmapTstring[:-1] +' '+ targets +' -oA discoveryServiceScan';
#print nmapcommand;

os.system(nmapcommand);

alivecommand = "grep 'Up' discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> aliveIPs.txt";	
os.system(alivecommand);

for port in uports:
	command = "grep ' " + port +"/open/udp/' discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> " + uports[port] +".txt";
	os.system(command);

for port in tports:
	command = "grep ' " + port +"/open/tcp/' discoveryServiceScan.gnmap | cut -d \" \" -f 2 >> " + tports[port] +".txt";
	os.system(command);