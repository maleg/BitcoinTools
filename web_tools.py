#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import urllib.request
import json
import smtplib
from email.mime.text import MIMEText

def get_UTXO_from_web():
	thefile = open('UTXO_addresses_with_balance.txt', 'w')
	utxo = []
	nexturl = 'https://api.smartbit.com.au/v1/blockchain/addresses?limit=1000'
	while(nexturl is not None):
		print(nexturl)
		response = urllib.request.urlopen(nexturl)
		data = response.read()      # a `bytes` object
		text = data.decode('utf-8') # a `str`; this step can't be used if data is binary
		textjson = json.loads(text)
		for entry in textjson["addresses"]:
			#utxo.append((entry["address"], entry["total"]["balance"]))
			thefile.write("%s %s\n" % (entry["address"], entry["total"]["balance"]))
			#print("%s %s" % (entry["address"], entry["total"]["balance"]))
			#b58decode_check(entry["address"])
		nexturl = textjson["paging"]["next_link"]

def parse_UTXO_from_web():
	print("Verifying Base58->hash160 Capability")
	verify_base58_to_hash160()

	file_source = open("UTXO_addresses_with_balance.txt", "r")
	file_dest = open("UTXO_hash160_with_balance_sorted.txt", "w")
	print("Getting dict of Bitcoin address stating by 1\n")
	addr_bal_sorted_dict = {bitcoin_address_To_hash160(x.split()[0]):x.split()[1] for x in file_source.readlines() if x.split()[0][0] == "1"}
	print("Getting list of Bitcoin address stating by 1\n")
	addr_bal = [x.split() for x in file_source.readlines()]
	file_source.close()


	#print("Getting only Bitcoin address stating with 1\n")
	#addresses = [x for (x,y) in addr_bal if x[0] == "1"]

	print("Finding duplicates")
	addresses_unique, addresses_duplicate = find_duplicate(addr_bal, False, True)
	print("Total of {} address".format(len(addresses_unique.keys())))
	print("Total of {} duplicates".format(len(addresses_duplicate.keys())))

	print("Converting list to hash160")
	addresses_unique_hash = map(lambda x: bitcoin_address_To_hash160(x), addresses_unique)

	print("Sorting List")
	addresses_unique_sorted = sorted(addresses_unique)

	file_dest.write("\n".join(addresses_unique_sorted))

def Send_email(body):
	# Create a text/plain message
	msg = MIMEText(body)

	# me == the sender's email address
	# you == the recipient's email address
	msg['Subject'] = 'Bitcoin found!!!' % textfile
	msg['From'] = "misteribm@gmail.com"
	msg['To'] = "misteribm@gmail.com"

	# Send the message via our own SMTP server.
	s = smtplib.SMTP('smtp.gmail.com:465')
	s.login("misteribm@gmail.com",'gma01gma')
	s.send_message(msg)
	s.quit()
