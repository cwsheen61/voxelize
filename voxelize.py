import heapq
import sys
import numpy

#a = [(1,2,3),(1,3,2),(2,3,1),(4,1,2),(2,3,3),(5,3,2)]

a = []
b = []
c = []
d = []


xMin = 0.0
xMax = 0.0
yMin = 0.0
yMax = 0.0
zMin = 0.0
zMax = 0.0


fname = raw_input('Input the point cloud: ')
fname = fname.strip()
fname = fname.replace('\'','')
print fname
basename = fname

voxel = input('Voxel size: ')
print voxel
highpass = input('Minimum points per voxel: ')
print highpass

loopCount = 0

# while loopCount <= 3000:


print 'Input file name: ', fname

#basename = basename.replace(('%d' % loopCount), ('%d' % (loopCount+100)), 1)

#fname = basename

oName = fname.replace('pointcloud', 'pointcloud_vox', 1)

print 'Output file name: ', oName

f=open(fname,'r')

hCount =0
for line in f:
	hCount += 1
	if line == 'end_header\n':
		break
	tempStr = line.split(' ')
	if tempStr[0] == 'element':
		numPts = int(tempStr[2])
		print 'Number of points: ', numPts

i = 0

f.close()

print 'Reading in large array from: ', fname

a = numpy.loadtxt(fname,skiprows = hCount)

print (a.shape)
min = numpy.arange(a.shape[1], dtype=float)
max = numpy.arange(a.shape[1], dtype=float)
print (a.min(axis=0, out=min))
print (a.max(axis=0, out=max))


xMin = min[0]
yMin = min[1]
zMin = min[2]
xMax = max[0]
yMax = max[1]
zMax = max[2]


#print '\n',xMin, xMax, yMin, yMax, zMin, zMax

xVoxels = int((xMax - xMin)/voxel)
yVoxels = int((yMax - yMin)/voxel)
zVoxels = int((zMax - zMin)/voxel)

print xVoxels, yVoxels, zVoxels		

b = []

for i in range(0,numPts):
	xVox = int(xVoxels * (((a[i][0])-xMin)/(xMax - xMin)))
	yVox = int(yVoxels * (((a[i][1])-yMin)/(yMax - yMin)))
	zVox = int(zVoxels * (((a[i][2])-zMin)/(zMax - zMin)))
	b.append((xVox, yVox, zVox, a[i][0], a[i][1], a[i][2], a[i][3], a[i][4], a[i][5]))
	if float(i/1000000) == float(i)/1000000.0:
		sys.stdout.write('\rBuilding b-matrix: %d' % i)
		sys.stdout.flush()


a = []

print '\nstarting heapify: '

heapq.heapify(b)

print 'heapify complete: '

xSum = 0.0
ySum = 0.0
zSum = 0.0
iSum = 0.0

i = 0
j = 0
k = 0
l = 0
m = 1
dCount = 0 

c = []

for i in range (0, numPts):
	c.append(heapq.heappop(b))
	if float(i/1000000) == float(i)/1000000.0:
		sys.stdout.write('\rBuilding c-matrix: %d' % i)
		sys.stdout.flush()

b = []

print '\nStarting voxelization: '

i = 0

d = []

dString = fname.replace('.ply', '_dMatrix.txt', 1)

dFile = open(dString,'w')


while i < numPts:
	xSum = c[i][3]
	ySum = c[i][4]
	zSum = c[i][5]
	iSum = c[i][7]
	cSum = c[i][8]
	cXbin = c[i][0]
	cYbin = c[i][1]
	cZbin = c[i][2]
	while j < xVoxels:
		while k < yVoxels:
			while l < zVoxels:
				i += 1
				if i > numPts-1:
					break
				jump = 1
				if c[i][0] == cXbin:
					if c[i][1] == cYbin:
						if c[i][2] == cZbin:
							if float(i/1000000) == float(i)/1000000.0:
								sys.stdout.write('\ri: %7d Summing: %3d' % (i, m))
								sys.stdout.flush()
							xSum += c[i][3]
							ySum += c[i][4]
							zSum += c[i][5]
							iSum += c[i][7]
							cSum += c[i][8]
							m += 1
#							print 'm: ', m
							jump = 0
				if jump == 1:
					xAve = xSum/float(m)
					yAve = ySum/float(m)
					zAve = zSum/float(m)
					iAve = iSum/float(m)
					d.append((xAve, yAve, zAve, iAve, m))
					if m > 1:
						dFile.write('%f %f %f %f %f %f %f %d\n' % (j, k, l, xAve, yAve, zAve, iAve, m))
					dCount += 1
#					print 'dCount: ', dCount, '  m: ', m
					m = 1
					l += 1
					i += 1
					if i > numPts-1:
						break
					xSum = c[i][3]
					ySum = c[i][4]
					zSum = c[i][5]
					iSum = c[i][7]
					cSum = c[i][8]
					cXbin = c[i][0]
					cYbin = c[i][1]
					cZbin = c[i][2]
#					print 'l: ', l
			k += 1
#			print 'k: ', k
			l = 0
			if i > numPts-1:
				break
		j += 1
#		print 'j: ', j
		l = 0
		k = 0
		if i> numPts-1:
			break

		
dFile.close()		
			
print '\nFinal dCount: ', dCount	
fCount = 0			

for i in range (0, dCount):
#	print i
	if d[i][4] >= highpass:
		fCount += 1

print '\nFinal fCount (number of points above highpass filter value): ', fCount


f2 = open(oName, 'w')

f2.write('ply\n')
f2.write('format ascii 1.0\n')
f2.write('element vertex %d\n' % (fCount-1))
f2.write('property float x\n')
f2.write('property float y\n')
f2.write('property float z\n')
f2.write('property float intensity\n')
f2.write('property float count\n')
f2.write('end_header\n')


for i in range (0, dCount):
#	print i
	if d[i][4] >= highpass:
		f2.write('%f %f %f %f %d\n' % (d[i][0], d[i][1], d[i][2], d[i][3], d[i][4]))
loopCount += 100
f2.close()
