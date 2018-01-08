#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#Opens a binary file and gives a generator that return chunks of data
def file_read_in_chunks(filename, chunk_size=1, start_offset=0):
	with open(filename, "rb") as infile:
		infile.seek(start_offset)
		chunk = infile.read(chunk_size)
		while chunk:
			yield chunk
			chunk = infile.read(chunk_size)

#Takes a string of various format and return a byte qty to use as start offset
def file_decode_start_offset(start_offset_string, verbose=True):
	start_offset = 0
	if start_offset_string is not None:
		if isinstance(start_offset_string, str):
			suffixes = ("MB", "KB", "GB", "B")
			suffixe = start_offset_string[-2:]
			if suffixe in suffixes:
				value = float(start_offset[:-2])
				if suffixe == "B": 
					start_offset = value
				value *= 1024
				if suffixe == "KB": 
					start_offset = value
				value *= 1024
				if suffixe == "MB": 
					start_offset = value
				value *= 1024
				if suffixe == "GB": 
					start_offset = value
			else:
				raise Exception("Start_offset_string has invalid suffix")
		elif isinstance(start_offset_string, int):
			start_offset = start_offset_string
		else:
			raise Exception("Start_offset_string is not a string or integer")
	start_offset = int(start_offset)			
	if verbose:
		print("Starting at offset {:X} = {}MB".format(start_offset, start_offset*72/1048576))
	return start_offset

def file_save_dict(filename, D):
	with open(filename, "w") as outfile:
		for key,value in D.items():
			outfile.write("{} {}\n".format(key, value))

def file_load_dict(database_utxo):
	print("Getting dict of Bitcoin address from filtered file : {}".format(database_utxo))
	file_source = open(database_utxo, "r")
	return {x.split()[0]:x.split()[1] for x in file_source.readlines()}

def create_mask(bit_qty, mask_offset=0, word_length=32, justify="right"):
	mask = 0
	for i in range(0, bit_qty):
		if justify == "right":
			mask |= 0x1<<i+mask_offset
		else:
			mask |= 0x1<<word_length-i-1-mask_offset
	return mask

def find_duplicate(L, print_unique = False, print_duplicate = False):
	seen = set()
	dup = set()
	for item in L:
		if item in seen:
			dup.add = item
			if print_duplicate:
				print("Duplicate Item:{}".format(item))
		else:
			seen.add(item)
			if print_unique:
				print("Unique Item:{}".format(item))
	return seen, dup

def generate_value(byte_length, start_offset, entropy):
	byte_array = bytearray(byte_length)
	counter = 0
	while(counter < 0xFFFFF):
		check_entropy(byte_array, 1, 1)
		print(byte_array)
		counter += 1
		incr_byte_array(byte_array)
	print("Counter={}".format(counter))
	
	
# Scan a byte_array from end to start looking for consecutive value
# if max_consecutive_Value is attained, we increment the LSB to break the chain
# Param: Order = number of bytes representing a single "value"
def check_entropy(byte_array, order, max_consecutive_value):
	for byte_idx in range(0, len(byte_array)-1):
		consecutive_value = 1
		if byte_array[byte_idx] == byte_array[byte_idx+1]:
			consecutive_value +=1
		if consecutive_value == max_consecutive_value:
			incr_byte_array(byte_array, byte_idx)

def check_word_entropy(byte_array, byte_offset, order=1, max_consecutive_value=2)
	for byte_idx in range(0, order):
		for word_idx in range(0, max_consecutive_value)
			(byte_offset, byte_offset+(order*max_consecutive_value), order):
			consecutive_value = 1
			if byte_array[byte_idx] == byte_array[byte_idx+1]:
				consecutive_value +=1
			if consecutive_value == max_consecutive_value:
				incr_byte_array(byte_array, byte_idx)

def incr_byte_array(b_arr, byte_idx=0):
	idx = byte_idx
	while(b_arr[idx] == 255):
		b_arr[idx] = 0
		idx += 1
	b_arr[idx] += 1
		

def scan_bits(mask_length, old_mask, word_length, startbit, endbit, level):
	for mask_offset in range(startbit, endbit+1):
		mask = old_mask | create_mask(mask_length, mask_offset, word_length, "left") 
		mask &= create_mask(word_length)	
		if level == 1:
			yield mask
		else:
			yield from flip(mask_length, mask, word_length, mask_offset+mask_length, endbit+mask_length, level-1)

def scan_test():
	start = 0x0000AAAA	
	flip = [start]
	flipcheck = []
	for mask_qty in range(1,8):
		prep = get_mask(2*mask_qty, 16)
		for i in range(0,16):		
			mask = (prep>>i) & 0xFFFF
			print("i={:02d} y={:02d} mask={:016b}".format(i, mask_qty, mask))
			flip.append(start^mask)
	
	for x in flip:
		if x in flipcheck:
			print("Double={}".format(x))
		else:
			print("{:04X} {:016b}".format(x, x))
			flipcheck.append(x)
