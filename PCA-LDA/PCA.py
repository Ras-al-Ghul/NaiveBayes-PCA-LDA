import numpy as np
from copy import deepcopy
import random, math, sys

numoffeatures = 1000
newnumoffeatures = 100
numofdata = 600

numoftestdata = 200

def populatedata(values):
	fp = open('dorothea_train.data')
	data = fp.readlines()

	#selectedfeatures = [1,2,3,4,5,6,7,8,9,10]
	selectedfeatures = []
	for i in range(numoffeatures):
		num = random.randint(1, 100001)
		if num not in selectedfeatures:
			selectedfeatures.append(num)

	for i in range(numofdata):
		line = data[i].split(' ')
		line = line[:len(line) - 1]
		if line == ['']:
			continue
		line = [int(x) for x in line]
		
		for j in range(len(line)):
			if line[j] in selectedfeatures:
				values[i][selectedfeatures.index(line[j])] = 1

	return selectedfeatures

def calccovmatrix(data):
	listoffeatures = []
	for i in range(numoffeatures):
		listoffeatures.append(data[i,:])
	covmatrix = np.cov(listoffeatures)
	return covmatrix

def sorteigen(eigval, eigvec):
	idx = eigval.argsort()[::-1]
	eigval = eigval[idx]
	eigvec = eigvec[:,idx]

	return eigval, eigvec

def deletecolumns(eigvecsc):
	for i in range(numoffeatures - newnumoffeatures):
		eigvecsc = np.delete(eigvecsc, len(eigvecsc[0]) - 1, axis=1)

	return eigvecsc

def gaussian(mean, variance, value):
	try:
		return ((1/math.sqrt(2 * math.pi * variance)) * (math.exp((-((value - mean) * (value - mean))) / (2 * variance))))
	except:
		print "exception"
		return 0.0000000000001    	

def calcclassmean(data, meanA, meanB, labels):
	for j in range(newnumoffeatures):
		sumA = 0
		numA = 0
		sumB = 0
		numB = 0
		for i in range(numofdata):
			if labels[i] == 1:
				sumA += data[j][i]
				numA += 1
			else:
				sumB += data[j][i]
				numB += 1
		if numA != 0:
			meanA[j] = float(sumA)/numA
		if numB != 0:
			meanB[j] = float(sumB)/numB

def calcvariance(data, varianceA, varianceB, labels, meanA, meanB):
	for j in range(newnumoffeatures):
		sumA = 0
		numA = 0
		sumB = 0
		numB = 0
		for i in range(numofdata):
			if labels[i] == 1:
				sumA += (data[j][i] - meanA[j]) ** 2
				numA += 1
			else:
				sumB += (data[j][i] - meanB[j]) ** 2
				numB += 1 
		if numA - 1 != 0:
			varianceA[j] = float(sumA)/(numA - 1)
		if numB - 1 != 0:
			varianceB[j] = float(sumB)/(numB - 1)

def getPrior():
	fp = open('dorothea_train.labels')
	data = fp.readlines()

	A = 0
	B = 0

	for i in range(numofdata):
		label = int(data[i])
		if label == 1:
			A += 1
		else:
			B += 1

	return float(A)/(A + B), float(B)/(A + B)

def populatetestdata(values, selectedfeatures):
	fp = open('dorothea_valid.data')
	data = fp.readlines()

	for i in range(numoftestdata):
		line = data[i].split(' ')
		line = line[:len(line) - 1]
		if line == ['']:
			continue
		line = [int(x) for x in line]
		
		for j in range(len(line)):
			if line[j] in selectedfeatures:
				values[i][selectedfeatures.index(line[j])] = 1

def getlabels(filename, ranges):
	fp = open(filename)
	data = fp.readlines()

	labels = []
	for i in range(ranges):
		label = int(data[i])
		labels.append(label)

	return labels

def predict(data, labels, meanA, meanB, varianceA, varianceB, priorA):
	correct = 0
	logconst = 1.000000001
	for i in range(numoftestdata):
		pA = math.log(priorA + logconst)
		pB = math.log(1 - pA + logconst)
		for j in range(newnumoffeatures):
			value = data[j][i]
			pA += math.log(gaussian(meanA[j], varianceA[j], value) + logconst)
			pB += math.log(gaussian(meanB[j], varianceB[j], value) + logconst)
		if (pA > pB and labels[i] == 1) or (pA < pB and labels[i] != 1):
			correct += 1
	print (float(correct)/numoftestdata) * 100, "%"

if __name__ == '__main__':
	random.seed()

	data = np.zeros((numofdata, numoffeatures))

	selectedfeatures = populatedata(data)
	data = data.T
	
	covmatrix = calccovmatrix(data)

	eigvalsc, eigvecsc = np.linalg.eig(covmatrix)
	eigvalsc, eigvecsc = sorteigen(eigvalsc, eigvecsc)

	eigvecsc = eigvecsc.astype(float)
	eigvecsc = deletecolumns(eigvecsc)

	newdata = eigvecsc.T.dot(data)

	NmeanvecA = np.zeros((newnumoffeatures, 1))
	NmeanvecB = np.zeros((newnumoffeatures, 1))
	labelles = getlabels('dorothea_train.labels', numofdata)
	calcclassmean(newdata, NmeanvecA, NmeanvecB, labelles)

	NvariancevecA = np.zeros((newnumoffeatures, 1))
	NvariancevecB = np.zeros((newnumoffeatures, 1))
	calcvariance(newdata, NvariancevecA, NvariancevecB, labelles, NmeanvecA, NmeanvecB)

	#classA +1 classB -1
	classA, classB = getPrior()

	testdata = np.zeros((numoftestdata, numoffeatures))
	populatetestdata(testdata, selectedfeatures)
	testdata = testdata.T

	newtestdata = eigvecsc.T.dot(testdata)
	testlabels = getlabels('dorothea_valid.labels', numoftestdata)

	predict(newtestdata, testlabels, NmeanvecA, NmeanvecB, NvariancevecA, NvariancevecB, classA)
