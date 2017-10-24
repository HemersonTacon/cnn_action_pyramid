import argparse
import math

encode = "utf-8"

def get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Input file")
	parser.add_argument("-o", "--outdir", help="Output directory")
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
	
def write_key_frames(name, outdir, key_frames):

	name = os.path.split(name)[1]
	
	try:
		# Verify if is a absolute path and join the path with the current working directory otherwise
		if not os.path.isabs(outdir):
			outdir = os.path.join(os.getcwd(), args.outdir)
		# If path doesn't exists, make it
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
		
		out_file = os.path.join(outdir, name) + ".bkf"
		
		# 'with' automatically closes output
		with open(out_file, "w", encoding=encode) as output:
			# Joining frames binary coded with \n
			output.write("\n".join(key_frames))
		
		return 0
	except Exception as e:
		print("Some error occurred while writing keyframes into file: ", e)
		return 1
	
def main(args):
	
	frames = read_lsh_file(args.name)
	key_frames = calculate_key_frames(frames, 1)
	if not args.outdir:
		args.outdir = ''
	write_key_frames(args.name, args.outdir, key_frames)	
	
if __name__ == '__main__':
	# parse arguments
	args = get_Args()
	main(args)
