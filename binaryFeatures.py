from lshash import LSHash
import bitarray
import random

encode = "utf-8"
nFrames = 100;
codeLength = 16
numberOfFeatures = 4096


frameList = []
fc7_file = "fc7" + ".fc7"
fc7 = open(fc7_file, "r")
frames = fc7.readlines()	
output = open("codigoBinarios.lsh", "w")

for i in range (len(frames)):
	print("\n"+ str(i))
	#frameList.append(frames[i])				
	fc7Features = frames[i].split()

	#for i in range (len(fc7Features)):
		#fc7Features[i] = float(fc7Features[i])
	fc7Features = map(float, fc7Features)
		

	################################################################
	# 		Gerando features aleatorias		


	#	fc7Features = random.sample(range(1000000), numberOfFeatures)
	#	fc7FeaturesCompare = random.sample(range(1000000), numberOfFeatures)

	################################################################


	lsh = LSHash(codeLength ,numberOfFeatures)
	lsh._init_uniform_planes()
	planes = lsh._generate_uniform_planes()
	fc7BinaryCode = lsh._hash(planes,fc7Features)
	#	fc7BinaryCode2 = lsh._hash(planes,fc7FeaturesCompare)



	###############################################################
	#		Printando os valores dos codigos

	#	print(fc7BinaryCode1)
	#	print(fc7BinaryCode2)

	###############################################################

	#	hammingDistance = lsh.hamming_dist( fc7BinaryCode1, fc7BinaryCode2)
	#	print("A distancia de hamming e: " + str(hammingDistance))
	frameList.append(fc7BinaryCode)
	print(frameList)
	output.write(fc7BinaryCode + "\n")

output.close()







	
