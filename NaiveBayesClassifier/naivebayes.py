import random, sys, itertools
from math import log

logconst = 1

def constructdict(listofdicts):
	namefile = open('./census/census-income.names', 'r')
	namedata = namefile.readlines()

	namedata = namedata[142:]
	
	for i in range(len(namedata)):

		if i not in [24, 25]:

			line = namedata[i].split(', ')

			label = line[0].split(': ')
			line[0] = label[1]
			label = label[0]

			line[len(line) - 1] = line[len(line) - 1].strip(".\n")

			if line[0] != 'continuous':
				listofdicts[0].append(dict((key, 0) for key in line))
				listofdicts[1].append(dict((key, 0) for key in line))
			else:
				if label == 'age':
					listofdicts[0].append(dict((key, 0) for key in range(10)))
					listofdicts[1].append(dict((key, 0) for key in range(10)))
				elif label == 'wage per hour':
					listofdicts[0].append(dict((key, 0) for key in range(11)))
					listofdicts[1].append(dict((key, 0) for key in range(11)))
				elif label == 'capital gains':
					listofdicts[0].append(dict((key, 0) for key in range(5)))
					listofdicts[1].append(dict((key, 0) for key in range(5)))
				elif label == 'capital losses':
					listofdicts[0].append(dict((key, 0) for key in range(5)))
					listofdicts[1].append(dict((key, 0) for key in range(5)))
				elif label == 'dividends from stocks':
					listofdicts[0].append(dict((key, 0) for key in range(10)))
					listofdicts[1].append(dict((key, 0) for key in range(10)))
				elif label == 'weeks worked in year':
					listofdicts[0].append(dict((key, 0) for key in range(6)))
					listofdicts[1].append(dict((key, 0) for key in range(6)))
				elif label ==  'num persons worked for employer':
					listofdicts[0].append([])
					listofdicts[1].append([])	
		else:
			if i == 25:
				listofdicts[0].append([])
				listofdicts[1].append([])

def addtolist(line, listofdicts, i):
	for j in range(len(line)):
		if line[j] != '?':
			if j not in [0, 5, 16, 17, 18, 24, 30, 39]:
				listofdicts[i][j][line[j]] += 1
			else:
				if j == 0:
					listofdicts[i][j][int(line[j])/10] += 1	
				elif j == 5:
					wageperhour = int(line[j])
					if wageperhour < 400:
						listofdicts[i][j][0] += 1
					elif wageperhour < 1000:
						listofdicts[i][j][1] += 1
					else:
						listofdicts[i][j][(wageperhour/1000) + 1] += 1
				elif j == 16:
					capitalgain = int(line[j])
					if capitalgain <= 10000:
						listofdicts[i][j][0] += 1
					elif capitalgain <= 20000:
						listofdicts[i][j][1] += 1
					elif capitalgain <= 30000:
						listofdicts[i][j][2] += 1
					elif capitalgain <= 50000:
						listofdicts[i][j][3] += 1
					else:
						listofdicts[i][j][4] += 1
				elif j == 17:
					listofdicts[i][j][int(line[j])/1000] += 1
				elif j == 18:
					listofdicts[i][j][int(line[j])/10000] += 1
				elif j == 39:
					listofdicts[i][j][int(line[j])/10] += 1

def populatedict(listofdicts, counts):
	fp = open('./census/census-income.data', 'r')
	data = fp.readlines()

	startindex = 0
	endindex = int(len(data) * 1)

	data = data[startindex:endindex]

	for i in range(len(data)):
		line = data[i].split(", ")
		
		label = line[len(line) - 1].strip(".\n")
		line = line[:len(line) - 1]

		if label == '- 50000':
			counts[0] += 1
			addtolist(line, listofdicts, 0)
		else:
			counts[1] += 1
			addtolist(line, listofdicts, 1)

def calclikelihood(listofdicts):
	for i in range(len(listofdicts[0])):
		if i not in [24, 30]:
			dict1 = listofdicts[0][i]
			dict2 = listofdicts[1][i]
			tempsum = 0
			for keyA, valueA in dict1.iteritems():
				tempsum += valueA
			for keyA, valueA in dict1.iteritems():
				dict1[keyA] = log(float(valueA)/tempsum + logconst)
			tempsum = 0
			for keyB, valueB in dict2.iteritems():
				tempsum += valueB
			for keyB, valueB in dict2.iteritems():
				dict2[keyB] = log(float(valueB)/tempsum + logconst)

def predict(listofdicts, counts):

	correctcount = 0
	equalcount = 0
	
	fp = open('./census/census-income.data', 'r')
	data = fp.readlines()

	startindex = 0
	endindex = int(len(data) * 1)

	data = data[startindex:endindex]

	for i in range(len(data)):
		class1prob = log(float(counts[0])/sum(counts) + logconst)
		class2prob = log(float(counts[1])/sum(counts) + logconst)
		line = data[i].split(", ")
		
		label = line[len(line) - 1].strip(".\n")
		line = line[:len(line) - 1]

		for j in range(len(line)):
			if line[j] != '?':
				if j not in [0, 5, 16, 17, 18, 24, 30, 39]:
					class1prob += listofdicts[0][j][line[j]]
					class2prob += listofdicts[1][j][line[j]]
				else:
					if j == 0:
						class1prob += listofdicts[0][j][int(line[j])/10]
						class2prob += listofdicts[1][j][int(line[j])/10]
					elif j == 5:
						wageperhour = int(line[j])
						if wageperhour < 400:
							class1prob += listofdicts[0][j][0]
							class2prob += listofdicts[1][j][0]
						elif wageperhour < 1000:
							class1prob += listofdicts[0][j][1]
							class2prob += listofdicts[1][j][1]
						else:
							class1prob += listofdicts[0][j][(wageperhour/1000) + 1]
							class2prob += listofdicts[1][j][(wageperhour/1000) + 1]
					elif j == 16:
						capitalgain = int(line[j])
						if capitalgain <= 10000:
							class1prob += listofdicts[0][j][0]
							class2prob += listofdicts[1][j][0]
						elif capitalgain <= 20000:
							class1prob += listofdicts[0][j][1]
							class2prob += listofdicts[1][j][1]
						elif capitalgain <= 30000:
							class1prob += listofdicts[0][j][2]
							class2prob += listofdicts[1][j][2]
						elif capitalgain <= 50000:
							class1prob += listofdicts[0][j][3]
							class2prob += listofdicts[1][j][3]
						else:
							class1prob += listofdicts[0][j][4]
							class2prob += listofdicts[1][j][4]
					elif j == 17:
						class1prob += listofdicts[0][j][int(line[j])/1000]
						class2prob += listofdicts[1][j][int(line[j])/1000]
					elif j == 18:
						class1prob += listofdicts[0][j][int(line[j])/10000]
						class2prob += listofdicts[1][j][int(line[j])/10000]
					elif j == 39:
						class1prob += listofdicts[0][j][int(line[j])/10]
						class2prob += listofdicts[1][j][int(line[j])/10]

		if (class1prob >= class2prob and label == '- 50000') or (class2prob >= class1prob and label == '50000+'):
			correctcount += 1
			if class1prob == class2prob:
				equalcount += 1

	print float(correctcount)/(endindex - startindex) * 100, "%"
	print correctcount, endindex-startindex
	print equalcount

if __name__ == '__main__':
	random.seed()

	listofdicts = [[], []] #class 1 - - 50000 class 2 50000+
	constructdict(listofdicts)

	counts = [0, 0]
	populatedict(listofdicts, counts)

	calclikelihood(listofdicts)

	predict(listofdicts, counts)
	