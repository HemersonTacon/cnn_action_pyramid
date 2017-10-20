import argparse
import math

encode = "utf-8"

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Input file")
	return parser.parse_args()

def read_lsh_file(name):

	lsh_file = name + ".lsh"
	lsh = open(lsh_file, "r", encoding=encode)
	# list with binary codified frames
	frames = lsh.readlines()
	lsh.close()
	return frames
	
def hamming_distance(a, b):
	c = 0
	for x, y in zip(a, b):
		# Bitwise XOR
		c = c + (int(x) ^ int(y))
	return c
	
# Receives a list of binary codified frames (each element is a string with 0's and 1's) and the hamming distance value not allowed inside snippet
def calculate_key_frames(frames, h_dist):
	
	# Creating a list of bits from first frame
	last_frame = list(frames[0])
	# Removing '\n' from the end of list
	last_frame.pop()
	key_frames = []
	
	# Putting this just to ease the merge logic
	key_frames.append(0)
	
	for i in range(len(frames) - 1):
		
		# Creating other list of bits from actual frame
		actual_frame = list(frames[i+1])
		# Removing '\n' from the end of list
		actual_frame.pop()
		# Hamming distance between those two "bitstring"
		dist = hamming_distance(last_frame, actual_frame)
		# If it's bigger than established distance
		if dist >= h_dist :
			key_frames.append(i+1)
			last_frame = actual_frame
	
	key_frames.append(len(frames))
	
	i = 0
	while i < (len(key_frames) - 1):
		# If snippet size is less than 20, need to merge
		if key_frames[i+1] - key_frames[i] < 20:
			# Borders
			# Begin
			if i == 0:
				del key_frames[i+1]
				# Need to verify if now is bigger than 20
				i = i - 1
			# End
			elif i == len(key_frames) - 2:
				del key_frames[i]
				i = i - 2
			# Inner
			elif (key_frames[i+2] - key_frames[i+1]) < (key_frames[i] - key_frames[i-1]):
				del key_frames[i+1]
				i = i - 1
			else:
				del key_frames[i]
				i = i - 2

		i = i + 1
		
	del key_frames[0]
	
		
	if len(frames) < 20:
		print("\n\n *** WARNING: less than 20 frames\n\n")
		
	return key_frames
	
def write_key_frames(name, key_frames):
	
	try:
		out_file = args.name + ".bkf"
		output = open(out_file, "w", encoding=encode)
		
		for i in key_frames:
			output.write(str(i)+"\n")
			
		output.close()
		
		return 0
	except Exception as e:
		print("Some error occurred while writing keyframes into file: ", e)
		return 1
	
def main(args):
	
	frames = read_lsh_file(args.name)
	key_frames = calculate_key_frames(frames, 1)
	write_key_frames(args.name, key_frames)	
	
if __name__ == '__main__':
	# parse arguments
	args = getArgs()
	main(args)
