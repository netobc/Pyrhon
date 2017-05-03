import re, os, sys

ScriptName = sys.argv[0]
if len(sys.argv) > 1:
	UnaFileName = sys.argv[1]

if not ".una" in UnaFileName:
	print "Not .una file, exiting."
	exit(0)

# VARS
NewFile = []
FirstRun = False
GuCorr = False
GuSpecPath = False
GuCfPath = False
OpVar = "OperatorVariable".upper()
First = "First".upper()
Run = "run".upper() 
GU = "GU"
Correlation = "Correlation".upper()
Spec = "spec".upper()
transform = "transform".upper()
filepath = "filepath".upper()

# Open file
f = open(UnaFileName, 'rb')
UnaFile = f.readlines()
f.close()


for line in UnaFile:
	LINE = line.upper()
	if OpVar in LINE and First in LINE and Run in LINE: # First RUn
		GuCorr = False
		GuSpecPath = False
		GuCfPath = False
		# print "True first run: |", line
		FirstRun = True
	elif OpVar in LINE and Run in LINE and GU in LINE and Correlation in LINE:
		FirstRun = False
		GuSpecPath = False
		GuCfPath = False
		GuCorr = True
	elif OpVar in LINE and GU in LINE and Spec in LINE and filepath in LINE:
		FirstRun = False
		GuCorr = False
		GuCfPath = False
		GuSpecPath = True
	elif OpVar in LINE and GU in LINE and transform in LINE and filepath in LINE:
		FirstRun = False
		GuCorr = False
		GuSpecPath = False
		GuCfPath = True
	elif "}" in LINE and not "{" in LINE:
		FirstRun = False
		GuCorr = False
		GuSpecPath = False
		GuCfPath = False
	# if FirstRun == True:
	# 	print line
	if FirstRun and "__UserMode" in line:
		print "First Run: |", line[:len(line)-1]
		line = re.sub("Engineering", "Production", line)
		print "First Run after: |", line[:len(line)-1]
	elif GuCorr and "__UserMode" in line:
		print "RunGUcorrelation: |", line[:len(line)-1]
		line = re.sub("Engineering", "Production", line)
		print "RunGUcorrelation after: |", line[:len(line)-1]
	elif GuSpecPath and "__UserMode" in line:
		print "GUSpecFilePath: |", line[:len(line)-1]
		line = re.sub("Production", "Engineering", line)
		print "GUSpecFilePath after: |", line[:len(line)-1]
	elif GuCfPath and "__UserMode" in line:
		print "GUTransformFilePath: |", line[:len(line)-1]
		line = re.sub("Production", "Engineering", line)
		print "GUTransformFilePath after: |", line[:len(line)-1]
	NewFile.append(line)

with open(UnaFileName, 'wb') as f:
	for line in NewFile:
		f.writelines(line)

# with open(re.sub(".una","",UnaFileName) + "mod.una", 'wb') as f:
# 	for line in NewFile:
# 		f.writelines(line)

# NewUna = open(re.sub(".una","",UnaFileName) + "mod.una", 'rb')
# NewUnaLines = NewUna.readlines()
# NewUna.close()

# print "################ Verification ################"

# for index, line in enumerate(NewUnaLines):
# 	if UnaFile[index] != line:
# 		print line[:len(line)-1]


