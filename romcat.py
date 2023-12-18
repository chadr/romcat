'''
romcat.py

Takes binary dumps of option ROMs and combines them into
one binary so that they can be burned onto a single
EPROM.

Automatically calculates and generates required padding.

romcat.py -h

or

romcat.py --help

for usage
'''

# imports
import os
import sys
import argparse
from functools import reduce

# main function
# this needs to be refactored
def main():
	print("romcat v0.2")
	print("https://github.com/chadr/romcat")
	print("released under MIT license, 2023")
	print("romcat WILL NOT modify original ROM dumps!")
	print("------------------------------------------")
	
	# concatenated list 
	combinedROMS = bytearray()

	# get command line arguments
	inputROMS, targetSize = getargs()

	# generate base-2 value of size
	realSize = getsize(targetSize)

	ROMS = readromfiles(inputROMS)

	# check for valie option ROMs
	# a valid option ROM starts with bytes 0x55 0xAA
	# as specified in the IBM PC standard
	print('checking for valid option ROMs...')
	for ROM, NAME in zip(ROMS, inputROMS):
		# check if first two bytes of option rom are 0x55 0xAA
		if ROM[0] == 0x55 and ROM[1] == 0xAA:
			print('  checking ' + NAME + '...VALID')
		else:
			print('  checking ' + NAME + '...INVALID (Bad signature)')
			sys.exit(2) 

	# combine the ROMs
	# probably a more pythonic way to do this
	for ROM in ROMS:
		combinedROMS = combinedROMS + ROM

	if len(combinedROMS) > realSize:
		print('ERROR: combined binary too large for E/EPROM size')
		sys.exit(2)
		
	paddingSize = realSize - len(combinedROMS)
	padding = bytes(paddingSize)

	print('padding binary file...DONE')
	outputROM = combinedROMS + padding

	with open("output.bin", "wb") as binary_file:
	    # Write text or bytes to the file
	    try:
	    	print('writing binary file...')
	    	num_bytes_written = binary_file.write(outputROM)
	    	print("  wrote %d bytes...DONE" % num_bytes_written)
	    except:
	    	print("ERROR: couldn't write binary file")
	    	sys.exit(2)

def readromfiles(inputROMS):
	ROMS = [] # list of ROM dumps

	# read in specified ROM files
	print('reading ROM files...')
	for ROM in inputROMS:
		# see if file actually exists
		if os.path.exists(ROM):
			# opening file via WITH ensures file is automatically closed after reading
			with open(ROM, "rb") as binary_file:
				# attempt to read it
				try:
					ROMS.append(binary_file.read())
					print('  reading ' + ROM + '...OK')
				except:
					print('  reading ' + ROM + '...FAILED')
					sys.exit(2)
		else:
			print("  reading " + ROM + "...FAILED (file doesn't exist!)")
			sys.exit(2)

	return(ROMS)

def getargs():
	parser = argparse.ArgumentParser(description = 'Combines option ROMs and generates correct padding size.')
	
	parser.add_argument('roms', metavar = 'roms', nargs = '+',
	                    help = 'option ROMs to be concatenated')
	
	parser.add_argument('size', metavar = 'size', help = 'output size (16K, 32K, 64K, etc)')

	args = parser.parse_args()

	return(args.roms, args.size)

def getsize(size):
	if size == "2K":
		return(2048)
	elif size == "4K":
		return(4096)
	elif size == "8K":
		return(8192)
	elif size == "16K":
		return(16384)
	elif size == "32K":
		return(32768)
	elif size == "64K":
		return(65536)
	elif size == "128K":
		return(131072)
	elif size == "256K":
		return(262144)
	elif size == "512K":
		return(524288)

if __name__ == "__main__":
	main()