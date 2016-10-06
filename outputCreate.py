import puzzleSolver
import os
import random

in_file = ''
out_file = ''

out_file = open('calc.txt','w')
out_file.write('\t   PATH  \tEXPLORED  \t    time in ms  \t  DEPTH   \n')
for i in range(20):
	randNum = random.randrange(80)

	os.system('py puzzleGenerator.py 4 '+str(randNum)+' 4.txt')
	os.system('py puzzleSolver.py 1 4 4.txt out.txt')
	in_file = open('out.txt','r')	
	output = in_file.readline()
	#print("out=")
	output = output.split('$')
	path=output[0]
	states = output[1]
	time = output[2]
	depth = output[3]


	out_file.write("\n"+str(randNum)+"\t"+path+"\t"+states+"\t"+time+"\t"+depth)

	output = in_file.readline()
	output = output.split('$')
	#print("out=")
	path=output[0]
	states = output[1]
	time = output[2]
	depth = output[3]


	out_file.write("\n"+str(randNum)+"\t\t"+path+"\t\t"+states+"\t\t"+time+"\t\t"+depth)
	
	#print('\n\t'+path+'\t'+states+'\t'+time+'\t'+depth)
	in_file.close()




out_file.close()