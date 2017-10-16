import argparse
import math

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Input file")
	parser.add_argument("level", type=int, help="Number of pyramid levels", choices=[1, 2, 3, 4])
	#parser.add_argument("-s", "--seed", help="Seed of the random function", type=int)
	return parser.parse_args()
	
def generate_cnnflows_of_snippet(first_frame, last_frame):
	global frames
	cnn_flows = []
	
	first_frame_features = frames[first_frame - 1].split()
	last_frame_features = frames[last_frame - 1].split()
	
	cnn_flow = [float(b) - float(a) for a, b in zip(first_frame_features, last_frame_features)]
	cnn_flows.append(cnn_flow)
	
	if levels > 1:
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
		
	if levels > 2:
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
			
	if levels > 3:
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

def main(args):
	
	bkf_file = args.name + ".bkf"
	bkf = open(bkf_file, "r", encoding="utf-16")
	# list with key-frame numbers
	key_frames = [int(line) for line in bkf.readlines()]
	
	bkf.close()
	#print(key_frames)
	
	fc7_file = args.name + ".fc7"
	fc7 = open(fc7_file, "r", encoding="utf-16")
	
	# frames with 4096 features each
	global frames
	frames = fc7.readlines()
	global levels
	levels = args.level
	
	out_file = args.name + ".cnnf"
	output = open(out_file, "w", encoding="utf-16")
	
	first_frame = 1
	for i in range(len(key_frames)):
		last_frame = key_frames[i]
		snippet_cnn_flows = generate_cnnflows_of_snippet(first_frame, last_frame)
		first_frame = last_frame + 1

		for j in range(len(snippet_cnn_flows)):
			for k in range(len(snippet_cnn_flows[j])):
				output.write(str(snippet_cnn_flows[j][k])+" ")
			output.write("\n")
		output.write("\n")
		
	output.close()
	
	
	
if __name__ == '__main__':
	# parse arguments
	args = getArgs()
	main(args)