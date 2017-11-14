import argparse
import math
import pandas as pd
import os
from binary_features import read_fc7_file
import numpy as np

encode = "utf-8"

def _get_Args():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("-k", "--key_name", help="Input keyframe file")
	parser.add_argument("fc7_name", help="Input fc7 file")
	parser.add_argument("level", type=int, help="Number of pyramid levels", choices=[1, 2, 3, 4])
	parser.add_argument("-o", "--outdir", help="Output directory")
	group.add_argument("-r", "--regular", help="Regular size of snippets", type=int)
	#parser.add_argument("-s", "--seed", help="Seed of the random function", type=int)
	return parser.parse_args()
	
def generate_cnn_flows_of_snippet(first_frame, last_frame, frames, level):
	#global frames
	cnn_flows = [[] for i in range(4)]
	
	first_frame_features = frames[first_frame - 1]
	last_frame_features = frames[last_frame - 1]
	
	cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
	cnn_flows[0].append(cnn_flow)
	
	if level > 1:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/2)
		if sub_snippet_size < 2:
			return cnn_flows
		rest = (last_frame - first_frame + 1) - (2*sub_snippet_size)
		x = first_frame
		for i in range(2):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			
			first_frame_features = frames[x - 1]
			last_frame_features = frames[y - 1]
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows[1].append(cnn_flow)
			
			x = y + 1
		
	if level > 2:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/4)
		if sub_snippet_size < 2:
			return cnn_flows
		rest = (last_frame - first_frame + 1) - (4*sub_snippet_size)
		x = first_frame
		for i in range(4):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			
			first_frame_features = frames[x - 1]
			last_frame_features = frames[y - 1]
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows[2].append(cnn_flow)
			
			x = y + 1
			
	if level > 3:
		sub_snippet_size = math.floor((last_frame - first_frame + 1)/10)
		if sub_snippet_size < 2:
			return cnn_flows
		rest = (last_frame - first_frame + 1) - (10*sub_snippet_size)
		
		x = first_frame
		for i in range(10):
			y = x + sub_snippet_size - 1
			
			if(i < rest):
				y = y + 1
			
			first_frame_features = frames[x - 1]
			last_frame_features = frames[y - 1]
		
			cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
			cnn_flows[3].append(cnn_flow)
			
			x = y + 1
	
	
	return cnn_flows
	
def read_keyframes(name):

	key_frames = pd.read_csv(name, header=None)
	
	return key_frames.values

	
def create_pyramid(key_frames, frames, level):

	# Se for os keyframes foram lidos de arquivo preciso fazer essa conversao
	if type(key_frames[0]) == type([]):
		key_frames = [i for item in key_frames for i in item]
	
	first_frame = 1
	cnn_flow_snippets = [[] for i in range(4)]
	for i in range(len(key_frames)):
		last_frame = key_frames[i]
		# Generates cnn flows to the snippet formed of the closed interval between first_frame and last_frame
		cnn_flows = generate_cnn_flows_of_snippet(first_frame, last_frame, frames, level)
		for k in range(4):
			cnn_flow_snippets[k].append(cnn_flows[k])
		# Update begin of interval
		first_frame = last_frame + 1

	return cnn_flow_snippets
	
def write_cnn_flow(name, outdir, cnn_flow_snippets):

	name = os.path.basename(name)
	# Removing file extension
	name = ".".join(name.split('.')[:-1])
	
	#cnnflow_dataframe = pd.DataFrame(cnn_flow_snippets)
	
	try:	
		# If path doesn't exists, make it
		if not os.path.isdir(outdir) and outdir != '':
			os.makedirs(outdir)

		for k in range(4):
			out_file = os.path.join(outdir, name) + str(k) + ".cnnf"
		
			# With automatically closes output
			with open(out_file, "w", encoding=encode) as output:
				# Joining cnn flows elements with space and then joining cnn flows with \n and finally joining snippets with \n\n
				output.write("\n\n".join(["\n".join([" ".join(list(map(str, j))) for j in i]) for i in cnn_flow_snippets[k]]))
			
		return 0
		
	except Exception as e:
		print("Some error occurred while writing cnnflow pyramid into file: ", e)
		return 1
	
def _main(args):
	
	frames = read_fc7_file(args.fc7_name)
	
	if args.regular:
		size = frames.shape[0]
		key_frames = np.arange(0, size, args.regular).tolist()
		del key_frames[0]
		key_frames.append(size)
	else:
		key_frames = read_keyframes(args.key_name).tolist()
		
	cnn_flow_snippets = create_pyramid(key_frames, frames.tolist(), args.level)
	if not args.outdir:
		args.outdir = ''
	write_cnn_flow(args.fc7_name, args.outdir, cnn_flow_snippets)
	
	
if __name__ == '__main__':
	# parse arguments
	args = _get_Args()
	_main(args)
