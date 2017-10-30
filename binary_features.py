from lshash import lshash
import argparse

encode = "utf-8"

def _get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Input file")
	parser.add_argument("bits", type=int, help="Number of bits of codification")
	parser.add_argument("-o", "--outdir", help="Output directory")
	return parser.parse_args()
	
def read_fc7_file(name):

	fc7_file = name + ".fc7"
	fc7 = open(fc7_file, "r", encoding=encode)
	# list with frame features
	frames = fc7.readlines()
	fc7.close()
	return frames
	
def codify_frames(frames, num_bits):
	
	temp = frames[0].split()
	num_features = len(temp)
	# Initializing hash
	lsh = lshash.LSHash(num_bits, num_features)
	# Getting plane of first and unique hash table
	plane = lsh.uniform_planes[0]
	bin_frames = []
	
	for i in frames:
		# Extracting features as float list
		features = list(map(float, i.split()))
		bin_frames.append(lsh._hash(plane, features))
	
	return bin_frames
	
def write_binary_frames(name, outdir, bin_frames):

	name = os.path.split(name)[1]
	
	try:
		# Verify if is not absolute path and join the path with the current working directory
		if not os.path.isabs(outdir):
			outdir = os.path.join(os.getcwd(), args.outdir)
		# If path doesn't exists, make it
		if not os.path.isdir(outdir):
			os.makedirs(outdir)
				
		out_file = os.path.join(outdir, name) + ".lsh"
		
		# 'with' automatically closes output
		with open(out_file, "w", encoding=encode) as output:
			# Joining frames binary coded with \n
			output.write("\n".join(bin_frames))
			
		return 0
		
	except Exception as e:
		print("Some error occurred while writing binary frames into file: ", e)
		return 1
	
def _main(args):
	
	frames = read_fc7_file(args.name)
	binary_frames = codify_frames(frames, args.bits)
	if not args.outdir:
		args.outdir = ''
	write_binary_frames(args.name, args.outdir, binary_frames)
	
if __name__ == '__main__':
	# parse arguments
	args = get_Args()
	main(args)


	
