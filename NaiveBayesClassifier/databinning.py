import matplotlib.pyplot as plt

if __name__ == '__main__':
	fp = open('./census/census-income.data', 'r')
	data = fp.readlines()

	#index, class A - - 50000, class B - 50000+ and within each - sum, min, max, class A values, class B values
	age = [0, set(), set(), [], []]
	wageperhour = [5, set(), set(), [], []]
	capitalgain = [16, set(), set(), [], []]
	capitalloss = [17, set(), set(), [], []]
	stockdividend = [18, set(), set(), [], []]
	numpersonsemployer = [30, set(), set(), [], []] #index + 1
	weeksperyear = [39, set(), set(), [], []] #index + 1
	classcount = [0, 0] #class A, class B

	print len(data), " data items"

	for i in range(len(data)):
		line = data[i].split(", ")
		
		dlabel = line[len(line) - 1].strip(".\n")
		dage = int(line[age[0]]) if line[age[0]] != '?' else '?'
		dwageperhour = int(line[wageperhour[0]]) if line[wageperhour[0]] != '?' else '?'
		dcapitalgain = int(line[capitalgain[0]]) if line[capitalgain[0]] != '?' else '?'
		dcapitalloss = int(line[capitalloss[0]]) if line[capitalloss[0]] != '?' else '?'
		dstockdividend = int(line[stockdividend[0]]) if line[stockdividend[0]] != '?' else '?'
		dnumpersonsemployer = int(line[numpersonsemployer[0]]) if line[numpersonsemployer[0]] != '?' else '?'
		dweeksperyear = int(line[weeksperyear[0]]) if line[weeksperyear[0]] != '?' else '?'
		
		if dlabel == '- 50000':
			classcount[0] += 1
			age[1].add(dage)
			wageperhour[1].add(dwageperhour)
			capitalgain[1].add(dcapitalgain)
			capitalloss[1].add(dcapitalloss)
			stockdividend[1].add(dstockdividend)
			numpersonsemployer[1].add(dnumpersonsemployer)
			weeksperyear[1].add(dweeksperyear)

			age[3].append(dage)
			wageperhour[3].append(dwageperhour)
			capitalgain[3].append(dcapitalgain)
			capitalloss[3].append(dcapitalloss)
			stockdividend[3].append(dstockdividend)
			numpersonsemployer[3].append(dnumpersonsemployer)
			weeksperyear[3].append(dweeksperyear)
		else:
			classcount[1] += 1
			age[2].add(dage)
			wageperhour[2].add(dwageperhour)
			capitalgain[2].add(dcapitalgain)
			capitalloss[2].add(dcapitalloss)
			stockdividend[2].add(dstockdividend)
			numpersonsemployer[2].add(dnumpersonsemployer)
			weeksperyear[2].add(dweeksperyear)

			age[4].append(dage)
			wageperhour[4].append(dwageperhour)
			capitalgain[4].append(dcapitalgain)
			capitalloss[4].append(dcapitalloss)
			stockdividend[4].append(dstockdividend)
			numpersonsemployer[4].append(dnumpersonsemployer)
			weeksperyear[4].append(dweeksperyear)
	
	ageset = age[1] | age[2]
	wageperhourset = wageperhour[1] | wageperhour[2]
	capitalgainset = capitalgain[1] | capitalgain[2]
	capitallossset = capitalloss[1] | capitalloss[2]
	stockdividendset = stockdividend[1] | stockdividend[2]
	numpersonsemployerset = numpersonsemployer[1] | numpersonsemployer[2]
	weeksperyearset = weeksperyear[1] | weeksperyear[2]

	print classcount[0], " - 50000 and", classcount[1], " 50000+"

	print "Class1 age", sum(age[3])/len(age[3]), " mean", min(list(age[1])), " min", max(list(age[1])), " max"
	print "Class2 age", sum(age[4])/len(age[4]), " mean", min(list(age[2])), " min", max(list(age[2])), " max"

	print "Class1 wageperhour", sum(wageperhour[3])/len(wageperhour[3]), " mean", min(list(wageperhour[1])), " min", max(list(wageperhour[1])), " max"
	print "Class2 wageperhour", sum(wageperhour[4])/len(wageperhour[4]), " mean", min(list(wageperhour[2])), " min", max(list(wageperhour[2])), " max"

	print "Class1 capitalgain", sum(capitalgain[3])/len(capitalgain[3]), " mean", min(list(capitalgain[1])), " min", max(list(capitalgain[1])), " max"
	print "Class2 capitalgain", sum(capitalgain[4])/len(capitalgain[4]), " mean", min(list(capitalgain[2])), " min", max(list(capitalgain[2])), " max"

	print "Class1 capitalloss", sum(capitalloss[3])/len(capitalloss[3]), " mean", min(list(capitalloss[1])), " min", max(list(capitalloss[1])), " max"
	print "Class2 capitalloss", sum(capitalloss[4])/len(capitalloss[4]), " mean", min(list(capitalloss[2])), " min", max(list(capitalloss[2])), " max"

	print "Class1 stockdividend", sum(stockdividend[3])/len(stockdividend[3]), " mean", min(list(stockdividend[1])), " min", max(list(stockdividend[1])), " max"
	print "Class2 stockdividend", sum(stockdividend[4])/len(stockdividend[4]), " mean", min(list(stockdividend[2])), " min", max(list(stockdividend[2])), " max"

	print "Class1 numpersonsemployer", sum(numpersonsemployer[3])/len(numpersonsemployer[3]), " mean", min(list(numpersonsemployer[1])), " min", max(list(numpersonsemployer[1])), " max"
	print "Class2 numpersonsemployer", sum(numpersonsemployer[4])/len(numpersonsemployer[4]), " mean", min(list(numpersonsemployer[2])), " min", max(list(numpersonsemployer[2])), " max"

	print "Class1 weeksperyear", sum(weeksperyear[3])/len(weeksperyear[3]), " mean", min(list(weeksperyear[1])), " min", max(list(weeksperyear[1])), " max"
	print "Class2 weeksperyear", sum(weeksperyear[4])/len(weeksperyear[4]), " mean", min(list(weeksperyear[2])), " min", max(list(weeksperyear[2])), " max"	

	plt.plot(age[3], 'ro')
	plt.plot(age[4], 'bo')
	plt.show()

	plt.plot(wageperhour[3], 'ro')
	plt.plot(wageperhour[4], 'bo')
	plt.show()

	plt.plot(capitalgain[3], 'ro')
	plt.plot(capitalgain[4], 'bo')
	plt.show()

	plt.plot(capitalloss[3], 'ro')
	plt.plot(capitalloss[4], 'bo')
	plt.show()

	plt.plot(stockdividend[3], 'ro')
	plt.plot(stockdividend[4], 'bo')
	plt.show()

	plt.plot(numpersonsemployer[3], 'ro')
	plt.plot(numpersonsemployer[4], 'bo')
	plt.show()

	plt.plot(weeksperyear[3], 'ro')
	plt.plot(weeksperyear[4], 'bo')
	plt.show()
	