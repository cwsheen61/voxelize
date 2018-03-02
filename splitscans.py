import sys
import math
import datetime
import time

trHeader = []
points = []
pcHeader = []
pcPoints = []
tPoints = []
kpT = []

lowPass = 3.0


pointCloudFileName = 'pointcloud_r.ply'

	
line = ''
count = 0

lineCount = 0
count = 0
index = 0


sumPts = 0

pc = open(pointCloudFileName,'r')

while line <> 'end_header\n':
	line = pc.readline()
	pcHeader.append(line.strip())
	print ('line: %d, value: %s' % (count, pcHeader[count]))
	count += 1
	
line = ''

headerStr = pcHeader[2].split(' ')
totalPoints = int(headerStr[2])
print 'Points: ', totalPoints

currentTime = 0.0
lastTime = -1.0
index = 0
tp = 0

for j in range (0, totalPoints):
	if tp >= totalPoints:
		break
	trTime = lastTime
	print 'trTime: ', trTime
	pcTime = -1
	pcCount = 0
	totalCount = 0
	while pcTime <= trTime:
		pcLine = pc.readline()
		if pcLine == '':
			break
		parsePcLine = pcLine.split()
		pcTime = float(parsePcLine[5])
		rVal = float(parsePcLine[4])
		if rVal <= lowPass:
			pcCount += 1
		totalCount += 1
		tp += 1
#	print 'index: ', j, pcCount
	pcPoints.append(pcCount)
	tPoints.append(totalCount)
	lastTime = pcTime
	index += 1

sumPcPoints = 0

for i in range(0,index):
	print pcPoints[i]
	sumPcPoints += pcPoints[i]

print sumPcPoints


line = ''

	
pc.close()
pc = open(pointCloudFileName,'r')
line = ''
while line <> 'end_header\n':
	line = pc.readline()


	
for i in range(0, index):

	pcName = ('pointcloud_%d.ply' % i)

	print pcName

	pcOut = open(pcName,'w')
	for j in range (0, count):
		if j <> 2:
			pcOut.write('%s\n' % pcHeader[j])
		else:
			pcOut.write('element vertex %d\n' % pcPoints[i])
	pCount = 0
	while pCount < tPoints[i]:
		line = pc.readline()
		if line == '':
			break
		parsePcLine = line.split(' ')
		rVal = float(parsePcLine[4])
		if rVal <= lowPass:
			pcOut.write(line)
		pCount+=1
	pcOut.close()

