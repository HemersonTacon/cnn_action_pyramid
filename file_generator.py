import random
import argparse

def getArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--fc7", help="Creates a fc7 file", action='store_true')
	parser.add_argument("-k", "--keyframes", help="Creates a key frames file", action='store_true')
	parser.add_argument("-c", "--cnnflows", help="Creates a CNN flows file with the informed levels in the pyramid", type=int, choices=[1, 2, 3, 4])
	parser.add_argument("-p", "--pca", help="Creates a CNN flows reduced by PCA file with the informed levels in the pyramid", type=int, choices=[1, 2, 3, 4])
	parser.add_argument("-b", "--codebooks", help="Creates a codebooks file", action='store_true')
	parser.add_argument("-d", "--descriptors", help="Creates a video descriptors file with the informed levels in the pyramid", type=int, choices=[1, 2, 3, 4])
	parser.add_argument("-s", "--seed", help="Seed of the random function", type=int)
	return parser.parse_args()
	
	
def create_fc7_file(name="fc7"):
	minimum = 1
	maximum = 1000
	frames = 100
	
	output_file = name + ".fc7"
	output = open(output_file, "w", encoding="utf-16")
	
	for i in range(frames):
		for j in range(4096):
			feature = random.uniform(minimum, maximum)
			output.write(str(feature)+" ")
		output.write("\n")
		
	output.close()

	
def create_keyframes_file(name="keyframes"):
	# min and max size values of snippets
	minimum = 20
	maximum = 30
	frames = 100
	count = 0
	number = 0
	
	output_file = name + ".bkf"
	output = open(output_file, "w", encoding="utf-16")
	
	number = random.randint(minimum, maximum)

	while (frames - count) >= 2*minimum:
		# Logic to let at least minimun frames to the last snippet
		temp = min(maximum, (frames - count - minimum))
		
		count = count + number
		output.write(str(count)+"\n")
		
		number = random.randint(minimum, temp)
		
	output.write(str(frames)+"\n")
	output.close()

def create_cnnflows_file(name="cnnflows", level=4):
	minimum = 1
	maximum = 999
	flows = 1
	snipets = 4;
	
	if level < 4:
		flows = 2**level - 1
	else:
		flows = 2**3 - 1 + 10
		
	output_file = name + ".cnnf"
	output = open(output_file, "w", encoding="utf-16")
	
	for i in range(snipets):
		for j in range(flows):
			for k in range(4096):
				cnnf = random.uniform(minimum, maximum)
				output.write(str(cnnf)+" ")
			output.write("\n")
		output.write("\n")
		
	output.close()
	

def create_pca_file(name="pca", level=4):
	minimum = 1
	maximum = 999
	flows = 1
	snipets = 4;
	
	if level < 4:
		flows = 2**level - 1
	else:
		flows = 2**3 - 1 + 10
		
	output_file = name + ".pca"
	output = open(output_file, "w", encoding="utf-16")
	
	for i in range(snipets):
		for j in range(flows):
			for k in range(100):
				pca = random.uniform(minimum, maximum)
				output.write(str(pca)+" ")
			output.write("\n")
		output.write("\n")
		
	output.close()
	

def create_codebooks_file(name="codebooks"):
	minimum = 1
	maximum = 1000
	size = 4000
	
	output_file = name + ".dic"
	output = open(output_file, "w", encoding="utf-16")
	
	for i in range(size):
		for j in range(100):
			coord = random.uniform(minimum, maximum)
			output.write(str(coord)+" ")
		output.write("\n")
		
	output.close()
	

def create_descriptors_file(name="descriptors", level = 4):
	minimum = 0
	maximum = 5
	size = 4000
	
	output_file = name + ".desc"
	output = open(output_file, "w", encoding="utf-16")
	
	for i in range(level):
		for j in range(size):
			freq = random.randint(minimum, maximum)
			output.write(str(freq)+" ")
		output.write("\n")
		
	output.close()
	return
	
	
def main(args):
	no_args_flag = True
	
	# If ommited, args.seed gets None value and the seed uses randomness sources provided by the OS
	random.seed(args.seed)
	
	
	if args.fc7:
		create_fc7_file()
		no_args_flag = False
		
	
	if args.keyframes:
		create_keyframes_file()
		no_args_flag = False
	
	if args.cnnflows:
		create_cnnflows_file(level=args.cnnflows)
		no_args_flag = False
	
	if args.pca:
		create_pca_file(level=args.pca)
		no_args_flag = False
	
	if args.codebooks:
		create_codebooks_file()
		no_args_flag = False
	
	if args.descriptors:
		create_descriptors_file(level=args.descriptors)
		no_args_flag = False
	
	if no_args_flag:
		create_fc7_file()
		create_keyframes_file()
		create_cnnflows_file()
		create_pca_file()
		create_codebooks_file()
		create_descriptors_file()

		
if __name__ == '__main__':
	# parse arguments
	args = getArgs()
	main(args)
	
	


		




