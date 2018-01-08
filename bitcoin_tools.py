#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import hashlib
import binascii

def decode_base58(s):
	""" Decodes the base58-encoded string s into an integer """
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	base_count = len(alphabet)
	decoded = 0
	multi = 1
	for char in s:
		decoded += multi * alphabet.index(char)
		multi = multi * base_count
	
	return decoded
	
def encode_base58(num):
	""" Returns num in a base58-encoded string """
	alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
	base_count = len(alphabet)
	encode_be = ''

	if (num < 0):
		return ''

	while (num >= base_count):    
		mod = num % base_count
		
		encode_be = alphabet[mod] + encode_be
		num = num // base_count

	if (num):
		encode_be = alphabet[num] + encode_be

	return encode_be

def bitcoin_address_to_hash160(bitcoin_address_b58):
	is_multi_sig = False
	if bitcoin_address_b58[0] == "3":
		is_multi_sig = True
	value_temp = bitcoin_address_b58[:0:-1]
	value_int = decode_base58(value_temp)
	value_hex = format(value_int, '048X')
	address_check = value_hex[-8:]
	address_hex = value_hex[0:-8]
	#print("b58:{} value_temp:{} value_hex:{} address_hex:{} address_check:{}".format(bitcoin_address_b58, value_temp, value_hex, address_hex, address_check))
	#print("value_int type={} value={}".format(type(value_int), value_int))
	return address_hex

def bitcoin_hash160Hex_to_address(hash160_hex):
	hash160_hex = "00" + hash160_hex
	m = hashlib.sha256()
	m2 = hashlib.sha256()
	m.update(bytes.fromhex(hash160_hex))
	m2.update(m.digest())
	checkHex = m2.hexdigest()
	#checkHex = binascii.hexlify(check).decode("ascii")
	#print("DEBUG before decode " + hash160_hex + checkHex[:8])
	num = int(hash160_hex + checkHex[:8], 16)
	return "1" + encode_base58(num)

def verify_base58_to_hash160():
	test = [ 
	{"address":"16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM", "hash160":"010966776006953D5567439E5E39F86A0D273BEE"},
	{"address":"34y4eyYK3mUPoys9xz9QSEHKh2RG5iLDuZ", "hash160":"23f1501d99f54be7971b1112eb45df3042f7691c"},
	{"address":"1KKiEAkpnQR2FH5kpkGP6442ZDkd6ZdrRS", "hash160":"c8fc2a802dd8e7cb94621c3a449b27d3abd2db51"},
	{"address":"1JCe8z4jJVNXSjohjM4i9Hh813dLCNx2Sy", "hash160":"bcadb700c24da04b17feb9aa9bd71e368a4b623c"},
	{"address":"1Q5YT4TU6skrLs2LdqDmRNpvFaQYT4iAis", "hash160":"fd26cf36d43e96f13090e48b43b1ab08742631d7"},
	{"address":"15NQthxeLSwMtEaXJFM7YUCf59LzmFjkeH", "hash160":"2fed2e93aecfcdadd0795d62a85c0100253835bc"},
	{"address":"3FXFshYr97aQUizVEGwdCLNdDihWtqHsT9", "hash160":"97b93f3dd47585e9e198e08572f9f6c07bdb926d"}
	]

	for entry in test:
		entry["hash160"] = entry["hash160"].upper()

	for entry in test:
		entry["decode"] = bitcoin_address_to_hash160(entry["address"])
		if entry["decode"] == entry["hash160"]:
			print("DECODE SUCCESS : {} {} {}\n".format(entry["address"], entry["decode"], entry["hash160"]))
		else:
			print("DECODE FAILED : {} {} {}\n".format(entry["address"], entry["decode"], entry["hash160"]))

	for entry in test:
		entry["encode"] = bitcoin_hash160Hex_to_address(entry["hash160"])
		if entry["encode"] == entry["address"]:
			print("ENCODE SUCCESS : {} {} {}\n".format(entry["hash160"], entry["encode"], entry["address"]))
		else:
			print("ENCODE FAILED : {} {} {}\n".format(entry["hash160"], entry["encode"], entry["address"]))
