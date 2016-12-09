#Jake Felzien
#this will be a test at using sci-kit learn's neural network, to see if we can enhance our speed
from sklearn.neural_network import MLPClassifier
import time
import cv2
import random

accountName = 'loki_the_wolfdog_SMALL'
accountName = 'destination_wild'

#this will be a directory variable in which i plan to put the directory to the images, as well as the log file, i wish to access
imgdirectory = '/home/jfelzien/Desktop/cs5660/neuralNetFeed/images/'+accountName+'/'
logdirectory = '/home/jfelzien/Desktop/cs5660/neuralNetFeed/logFile.txt'

def loadHash(logFile, account):
	imageHash = {}
	hashFile = open(logFile, 'r')
	for line in hashFile:
		#print line.split()
		if line.split()[0] == account:
			imageHash[line.split()[1]] = line.split()[2]
	return imageHash

def loadImage(path):
	im = cv2.imread(path)
	return flatten(im)
 
def flatten(x):
	result = []
	for el in x:
		if hasattr(el, "__iter__") and not isinstance(el, basestring):
			result.extend(flatten(el))
		else:
			result.append(el)
	return result

def avgErrorCalc(actualAr, expAr):
	resultarray = []
	for index, i in enumerate(actualAr):
		resultarray.append(float((abs(actualAr[index] - expAr[index]) / actualAr[index]) * 100 ))
	total = 0.0
	for i in resultarray:
		total += i 
	return total/len(resultarray)




if __name__ == "__main__":
	startTime = time.time()
	X = []
	y = []
	imgHash = loadHash(logdirectory, accountName)
	#this is an inital tester, make sure to comment this out later
	#t = loadImage(imgdirectory+'img_0.png')
	#print t
	#print "length of t:", len(t)

	#now lets load all of the images into our massive array
	#don't forget to add an outlier check. load all of the total like counts into a list and do a similar technique to the plotting file
	#also, I need to implement a random selection and keep track of it, where i select 50 random images or so for training
		#and then test on a huge amount of random ones, but always make sure to not add stuff that has already been used
	#for i in range(0,100):
	countList = []

	while len(countList) < 80:
		i = random.randint(0, 1000)
		if i not in countList:
			try:
				print "Loading image: ", i
				X.append(loadImage(imgdirectory+'img_'+str(i)+'.png'))
				y.append(imgHash['img_'+str(i)+'.png'])
				countList.append(i)
			except:
				print "Image does not exist, cannot be added to training data"

	print "Training the classifier"
	clf = MLPClassifier(activation='logistic', solver='lbfgs', alpha=0.001, hidden_layer_sizes=(35, 20), random_state=1, max_iter=1000)
	clf.fit(X, y)

	#this was a single test to see if we had a complete model, good to go
	#print "Printing results of image 0"
	#print clf.predict([t])
	#print imgHash['img_0.png']
	#print imgHash['img_'+str(i)+'.png']
	actual = []
	experimental = []
	#for i in range(100, 200):
	while len(countList) < 150:
		i = random.randint(0, 1000)
		if i not in countList:
			try:
				t = loadImage(imgdirectory+'img_'+str(i)+'.png')
				print "Experimental:", clf.predict([t]) , "     Actual:" , imgHash['img_'+str(i)+'.png']
				actual.append(float(imgHash['img_'+str(i)+'.png']))
				experimental.append(float(clf.predict([t])[0]))
				countList.append(i)
			except:
				print 'image does not exist, unable to test'
	print "\n\nError Analysis:"
	print "Average Error:", avgErrorCalc(actual, experimental)
	print "Done Executing"
	print "Time to execute: ", time.time() - startTime , " seconds"
	print "Time to execute: ", (time.time() - startTime)/60 , " minutes"
	print "Time to execute: ", ((time.time() - startTime)/60)/60 ,  " hours"
