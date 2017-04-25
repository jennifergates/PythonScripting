#!/usr/bin/python
######
# script to bulk add Windows OSSEC agents to the server and then pull the keys
# decode them from base64 and save them each to a separate file called client.keys.
#####

### run on OSSEC server, like Security Onion

### OSSEC runs chrooted so must place the bulk file in /var/ossec/tmp/ but reference it with just /tmp/.
###  so this script takes the input file and copies it to /var/ossec/tmp.

import os
import argparse
import subprocess
import sys

# Must run as root
if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

# command line arguments
parser = argparse.ArgumentParser(description='Bulk add and create client.keys files from a list of Windows machines getting OSSEC agents installed.')
parser.add_argument('path', metavar='path', type=str, 
                    help='path to file of windows computers. List IP, subnet, or any then a comma, then the hostname. Example: \n 192.168.25.0/24,mycomputer.net or 10.10.10.1,my.computer.net')

args = parser.parse_args()

# main program
if __name__ == '__main__':

    agentIDs = []

    print "\n"
    print "Script to add multiple computers as OSSEC agents"
    if not os.path.exists(args.path):
        print "No such path"
    else:
    	subprocess.check_output(['cp', args.path, '/var/ossec/tmp/bulk_clients'])
    	print "[ ] Verified file " + args.path + " exists. Continuing."
	
	#OSSEC command to add multiple agents to the database. Returns info including agent ID.
	print "[ ] Adding agents for hosts in " + args.path
	text = subprocess.check_output(["/var/ossec/bin/manage_agents", "-f", "/tmp/bulk_clients"]);
	#print text

	# Example output data for testing #
	#text = "Bulk load file: /tmp/bulk_clients\nOpening: [/tmp/bulk_clients]\nAgent information:\n   ID:003\n   Name:host3\n   IP Address:any\n\nAgent added.\nAgent information:\n   ID:004\n   Name:host4\n   IP Address:any\n\nAgent added.\nAgent information:\n   ID:005\n   Name:host5\n   IP Address:any\n\nAgent added.\n0"

	# Parse output of add multiple agents command to collect ID assigned to hostname
	agentblock=text.split("\n\n")
	#print agentblock[1]
	for data in agentblock:
		if "already present" in data:
			print "\t" + data.split("'")[1] + " already present. Skipping."
			continue
		line = str(data).split("\n")
		#print "line:"		
		#print line
		name = []
		id = []
		for item in line:
			if "ID:" in item:
				id = item.split(":")
				#print id[1]
			elif "Name:" in item:
				name = item.split(":")
				#print name[1]
		
		if len(name) <> 0:
			print "\tAdded "+ name[1] + " ID: "+ id[1]			
			agentIDs.append([id[1],name[1]])

	#print agentIDs

	print "[ ] Creating subfolder ./ossec_keys"
	if not os.path.exists("./ossec_keys"):		
		subprocess.check_call(['mkdir', "ossec_keys"])

	# Parses and decodes the base64 key returned for each agent ID entered in the OSSEC command
	print "[ ] Creating hostname_client.keys file for each new agent"
	for agentID in agentIDs:
		print "\tExtracting key for " + agentID[1] + " ID: "+ agentID[0]
		resp = subprocess.check_output(["/var/ossec/bin/manage_agents", "-e", agentID[0]]);
		key64 = resp.split(":")
		key = key64[1].decode('base64')
	
		# writes the decoded key data to a separate file for each agent added. file named hostname_client.keys
		# and saved to ./ossec_keys/
		
		
		filename = "./ossec_keys/" + agentID[1] + "_client.keys"
		f = open(filename, 'w')
		f.write(key + "\n")
		f.close()

	# Writes all agents in the DB to a file
	print "[ ] Writing all agents to file ./ossec_keys/all_agents.txt"	
	allAgents = subprocess.check_output(["/var/ossec/bin/manage_agents", "-l"]);
	f = open("./ossec_keys/all_agents.txt", "w")
	f.write(allAgents)
	f.close()


	#Cleanup
	subprocess.check_output(['rm', '/var/ossec/tmp/bulk_clients'])

	print "[ ] Script complete. Files located in ./ossec_keys"
		
	

	
