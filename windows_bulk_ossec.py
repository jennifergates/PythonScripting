######
# script to bulk add Windows OSSEC agents to the server and then pull the keys
# decode them from base64 and save them each to a separate file called client.keys.
#####

### run on OSSEC server, like Security Onion

### Place the bulk file in /var/ossec/tmp/
import os
import argparse
import subprocess
import sys

if not os.geteuid() == 0:
    sys.exit('Script must be run as root')

parser = argparse.ArgumentParser(description='Bulk add and create client.keys files from a list of Windows machines getting OSSEC agents installed.')
parser.add_argument('path', metavar='path', type=str, 
                    help='path to file of windows computers')

args = parser.parse_args()

if __name__ == '__main__':

    if not os.path.exists(args.path):
        print "no such path"
    else:
    	subprocess.check_output(['cp', 'args.path', '/var/ossec/tmp/bulk_clients'])
    	print "found file"

	#/var/ossec/bin/manage_agents -f /tmp/bulk_clients > /tmp/bulk_output


#	from subprocess import call
#call("cp -p <file> <file>", shell=True)