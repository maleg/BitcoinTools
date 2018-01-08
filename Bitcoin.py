#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import web_tools
import bitcoin_tools
import genereal_tools
import json
from time import time






	
# Adds a test value to database so it is found and decoded
# Can be : Base58 address, Hash160
def add_test_values_to_UTXO(D, str="1Ca1Rif6i9zsnZjtcgLeczJSskYDAqkrgv"):
	value = ""
	if len(str) == 40:
		#Assume its a hash160 of public address
		value = str
	elif str.startswith("1"):
		#Assume standard base58 bitcoin address
		value = bitcoin_address_to_hash160(str)

	#replace balance with "test"
	D[value] = "test"
	print("Adding test addresses {} to Dict".format(value))

	
def display_progress(byte_offset, old_byte_offset, newtime, prevtime, privkey, pubkey_u, pubkey_c):
	MB_read = byte_offset/1048576
	khash_per_sec = (byte_offset-old_byte_offset)/72/(newtime-prevtime)/1000
	print(",{:X}u {}MB {:.1f}kH/s".format(entryQty, MB_read, khash_per_sec))
	print("DEBUG Priv{}={}".format(len(privkey), privkey))
	print("DEBUG Pubkey Hash160 Uncomp.{}={}".format(len(pubkey_u), pubkey_u))
	print("DEBUG Pubkey Hash160 Comp.{}={}".format(len(pubkey_c), pubkey_c))
	addr_c = bitcoin_hash160Hex_to_address(pubkey_c)
	addr_u = bitcoin_hash160Hex_to_address(pubkey_u)
	print("DEBUG Address Uncomp.{}={}".format(len(addr_u), addr_u))
	print("DEBUG Address Comp.{}={}".format(len(addr_c), addr_c))

def found_database_match(database_filename, byte_offset, privkey, pubkey, balance):
	msg = "File:{} Byte:{} Priv={} Balance={} PubUnc={} ".format(database_filename, byte_offset, privkey, balance, pubkey)
	print(msg)
	Send_email(msg)
	return 1

def scan_database(database_c, database_utxo, start_offset = 0, stop_offset = 0xFFFFFFFFFFFFFFFF):
	addr_bal_sorted_dict = load_dict_from_hash160_file(database_utxo)
	#addr_bal_sorted_dict = load_dict_from_address_file(database_utxo)
	#save_dict_to_file("UTXO_hash160_filtered.txt", addr_bal_sorted_dict)
	add_test_values_to_UTXO(addr_bal_sorted_dict, "1Ca1Rif6i9zsnZjtcgLeczJSskYDAqkrgv")

	prevtime = time()
	old_byte_offset = 0
	byte_offset = 0
	print("Scanning Database for match")
	byte_offset = file_decode_start_offset(start_offset, infile)
	for chunk in file_read_in_chunks(infile, 72, byte_offset):
		byte_offset += 72
		if byte_offset > stop_offset:
			print("Stop offset reached. done.")
			return 0
		#line_hex = ''.join( [ "%02X"%x for x in chunk ] )
		line_hex = binascii.hexlify(chunk).decode("ascii")
		pubkey_c = line_hex[0:40].upper()
		pubkey_u = line_hex[40:80].upper()
		privkey = line_hex[80:144].upper()
		#print("DEBUG Priv{}={} PubU{}={} PubC{}={}".format(len(privkey), privkey, len(pubkey_u), pubkey_u, len(pubkey_c), pubkey_c))
		if pubkey_u in addr_bal_sorted_dict:
			return found_database_match(database_c, byte_offset, privkey, pubkey_u, addr_bal_sorted_dict[pubkey_u])
		if pubkey_c in addr_bal_sorted_dict:
			return found_database_match(database_c, byte_offset, privkey, pubkey_c, addr_bal_sorted_dict[pubkey_c])
		if byte_offset % (1048576) == 0:
			newtime = time()
			display_progress(byte_offset, old_byte_offset, newtime, prevtime, privkey, pubkey_u, pubkey_c)
			prevtime = newtime
			old_byte_offset = byte_offset
	print("done")
	return 0

generate_value(8,0,0)

#verify_base58_to_hash160()
#ret = scan_database("/media/malego/Data2TB/Keys_PubC20PubU20Priv32_00004cac6a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321726.txt", "UTXO_hash160_filtered.txt", 0, 72000000000)
#if ret == 0:
	#ret = scan_database("/media/malego/Data2TB/Keys_PubC20PubU20Priv32_000000006a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321727.txt", "UTXO_hash160_filtered.txt", 0, 72000000000)
#ret = scan_database("/media/malego/Data2TB/Keys_PubC20PubU20Priv32_000000006a307f426a94f8114701e7c8e774e7f9a47e2c2035db29a206321729.txt", "UTXO_hash160_filtered.txt", 0, 60000000000)




