# Naive Bayes and PCA/LDA

This repo contains code which implements the Naive Bayes classifier and the PCA and LDA methods of dimensionality reduction.  

### Naive Bayes Classifier  

This directory contains two files and the `census` directory.  
The `census` directory contains:  
- `census-income.data`  
- `census-income.names`  
- `census-income.test`  
The full versions of these files can be downloaded from <https://archive.ics.uci.edu/ml/datasets/Census-Income+%28KDD%29> and put in this directory.  

To run:`python databinning.py` and `python naivebayes.py`  

1. `databinning.py` - For binning, all the features that were continuous were initially considered. Then the ‘min’ value, ‘max’ value, ‘mean’ were observed for each of the features considered. For each feature a plot was drawn - sampleindex vs valueoffeature - the points were color coded - red for one class and blue for the other. Seeing the above graph and observing the variance, those features were selected which could better distinguish between the two classes. Features which gave overlapping class regions were ignored. The next step was to select proper values to bin each feature. This was done with the help of the above plot. Finally, the real features that have been binned are: `age`,  `wage per hour`, `capital gains`, `capital losses`, `dividends from stocks`, `weeks worked in year`, `num persons worked for employer`  
2. `naivebayes.py` - This implements the classifier. The `endindex` in `lines 94 and 136` are a multiple of len(data). The `1 can be replaced` by any number in the range `(0, 1]`. Please ensure that atleast one sample of both the classes exist to avoid a divide by 0 error. Here, in line 132, the `census-income.test` file can also be used. What has been done is to test on the train data itself.  
`Log probabilities` were used to avoid calculation errors due to very small numbers. A small logconst was added to the probabilities and then the log was taken. These log probabilities were then summed up.  
While training, if a missing entry occurs, we can do two things, either ignore the sample or take only the values of the features which aren’t missing. In this case I chose to take the values and not ignore the sample per se.  
While testing, we just use the features which have no missing values and ignore the ones with a missing value.  

### PCA-LDA

This work was done on the Dorothea dataset <https://archive.ics.uci.edu/ml/datasets/Dorothea>  
Training was done on the `train` file and testing on the `valid` file.

To run:`python PCA.py` and `python LDA.py`  

1. `PCA.py` - This implements the PCA technique. `numoffeatures` is the subset of the 100000 features. `newnumoffeatures` is the number of features in the new PCA reduced dimensions space.
`numofdata` is the number of datapoints to be used for training. `numoftestdata` is the number of datapoints to be used for testing - valid file.  
Since the original dataset consists of a really large number of features - 100000 features, there are two ways one can go about the task - use the so called ‘kernel trick’ for calculating the eigen vectors of ATA matrix or to select a random subsample of the 100000 features and then implement a PCA on that feature set. I chose to go with the latter approach.  
More info on the former approach can be found here:  
<http://stats.stackexchange.com/questions/7111/how-to-perform-pca-for-data-of-very-high-dimensionality>  
<http://stats.stackexchange.com/questions/134282/relationship-between-svd-and-pca-how-to-use-svd-to-perform-pca>  
Here we have separate train and test data. For training, all the 600 samples were used. For testing, 200 of the 350 samples were used.  
Since we take a random sample of the 100000 features, we assume that the 50000 features selected has a uniform distribution of the real and probe features.  

2. `LDA.py` - This implements the LDA technique. `numoffeatures`, `newnumoffeatures`, `numofdata` and `numoftestdata` all carry the same meaning as above. But let `newnumoffeatures` be `1` for the 1D LDA Space.
