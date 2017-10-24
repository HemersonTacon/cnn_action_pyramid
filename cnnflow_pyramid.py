import argparse
import math

encode = "utf-8"

def get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Input file")
	parser.add_argument("level", type=int, help="Number of pyramid levels", choices=[1, 2, 3, 4])
	parser.add_argument("-o", "--outdir", help="Output directory")
	#parser.add_argument("-s", "--seed", help="Seed of the random function", type=int)
	return parser.parse_args()
	
def generate_cnn_flows_of_snippet(first_frame, last_frame, frames, level):
	#global frames
	cnn_flows = []
	
	first_frame_features = frames[first_frame - 1].split()
	last_frame_features = frames[last_frame - 1].split()
	
	cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
	cnn_flows.append(cnn_flow)
	
	if level > 1:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/2)
		rest = (last_frame - first_frame + 1) - (2*sub_snippet_size)
		x = first_frame
		for i in range(2):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			
			first_frame_features = frames[x - 1].split()
			last_frame_features = frames[y - 1].split()
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows.append(cnn_flow)
			
			x = y + 1
		
	if level > 2:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/4)
		rest = (last_frame - first_frame + 1) - (4*sub_snippet_size)
		x = first_frame
		for i in range(4):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			
			first_frame_features = frames[x - 1].split()
			last_frame_features = frames[y - 1].split()
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows.append(cnn_flow)
			
			x = y + 1
			
	if level > 3:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/10)
		rest = (last_frame - first_frame + 1) - (10*sub_snippet_size)
		
		x = first_frame
		for i in range(10):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			first_frame_features = frames[x - 1].split()
			last_frame_features = frames[y - 1].split()
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows.append(cnn_flow)
			
			x = y + 1
	
	
	return cnn_flows

def read_keyframes_and_fc7(kf_name, fc7_name):

	try:
		bkf_file = kf_name + ".bkf"
		bkf = open(bkf_file, "r", encoding=encode)
		# list with key-frame numbers
		key_frames = [int(line) for line in bkf.readlines()]
		bkf.close()
		
		fc7_file = fc7_name + ".fc7"
		fc7 = open(fc7_file, "r", encoding=encode)
		# frames with 4096 features each
		frames = fc7.readlines()
		fc7.close()
		
		return key_frames, frames
	except Exception as e:
		print("A problem occurred trying to open keyframe or fc7 file: ", e)
		print("With parameters: \n", vars(args))
		return 0
	
def create_pyramid(key_frames, frames, level):
	
	first_frame = 1
	cnn_flow_snippets = []
	for i in range(len(key_frames)):
		last_frame = key_frames[i]
		# Generates cnn flows to the snippet formed of the closed interval between first_frame and last_frame
		cnn_flow_snippets.append(generate_cnn_flows_of_snippet(first_frame, last_frame, frames, level))
		# Update begin of interval
		first_frame = last_frame + 1

	return cnn_flow_snippets
	
def write_cnn_flow(name, outdir, cnn_flow_snippets):

	name = os.path.split(name)[1]
	
	try:	
		# Verify if is not absolute path and join the path with the current working directory
		if not os.path.isabs(outdir):
			outdir = os.path.join(os.getcwd(), args.outdir)
		# If path doesn't exists, make it
		if not os.path.isdir(outdir):
			os.makedirs(outdir)

		out_file = os.path.join(outdir, name) + ".cnnf"
	
		# With automatically closes output
		with open(out_file, "w", encoding=encode) as output:
			# Joining cnn flows elements with space and then joining cnn flows with \n and finally joining snippets with \n\n
			output.write("\n\n".join(["\n".join([" ".join(list(map(str, j))) for j in i]) for i in cnn_flow_snippets]))
			
		return 0
		
	except Exception as e:
		print("Some error occurred while writing cnnflow pyramid into file: ", e)
		return 1
	
def main(args):
	
	key_frames, frames = read_keyframes_and_fc7(args.name, args.name)
	cnn_flow_snippets = create_pyramid(key_frames, frames, args.level)
	if not args.outdir:
		args.outdir = ''
	write_cnn_flow(args.name, args.outdir, cnn_flow_snippets)
	
	
if __name__ == '__main__':
	# parse arguments
	args = get_Args()
	main(args)
