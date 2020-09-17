###########Code for three histograms##########################################
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from apyori import apriori
from sklearn import model_selection 
from sklearn.preprocessing import normalize
# http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_
# recall_fscore_support.html#sklearn.metrics.precision_recall_fscore_support
# Link shows what each metric represents and how its calculated
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier 
from sklearn.svm import SVC
import numpy as np
from sklearn.cluster import KMeans,AgglomerativeClustering, DBSCAN
from sklearn import preprocessing
import pylab as pl
from sklearn import decomposition
from pprint import pprint
from sklearn.metrics import silhouette_samples, silhouette_score
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import dendrogram, linkage  
from pandas.plotting import scatter_matrix
import seaborn as sns
from scipy import stats
import urllib
import urllib.request
import requests
import json
from urllib.request import urlopen
from pandas import DataFrame
from pandas import merge
from sklearn.linear_model import LinearRegression
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go
import pandas as pd
import plotly
import numpy as np


# Have to specify dtype because FIPS State and FIPS County should be strings.
# If this is not done, then python thinks its integers, which removes leading 0's.
# Note, there might be bugs on an apple computer.  
air = pd.read_csv('cleanPollutionData.csv', dtype={
        'FIPS State':object, 'FIPS County':object})

water = pd.read_csv('water_clean.csv')
cancer = pd.read_csv('cleaned_cancer.csv')
# add leading 0's
cancer['FIPS'] = cancer['FIPS'].apply(lambda x: '{0:0>5}'.format(x))

# fix water fips - add leading 0's.
water['FIPS'] = water['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
water['FIPS'] = water['FIPS'].astype(object)

# Creating a single FIPS Column.
air['FIPS'] = air['FIPS State'] + air['FIPS County']
air = air.drop(['FIPS State', 'FIPS County'], axis=1)
air['FIPS'] = air['FIPS'].str.replace("=", "")
air['FIPS'] = air['FIPS'].str.replace("\"", "")

def cancerBin(cancer):
    #bin cancer incidence rate
    quants = [0, .25, .5, .75, 1.]
    labels = ['<25%', '25-50%', '50-75%', '75-100%']
    cancer['Incidence Quant'] = pd.qcut(pd.to_numeric(cancer[
           'Age-Adjusted Incidence Rate(†) - cases per 100,000'],
       errors = 'coerce'),quants, labels=labels)
    return cancer

cancer = cancerBin(cancer)
    
##This function creates a histogram showing the frequency of max AQI values for 2011-2015
def AirQualityHist(data):
    name= "Maximum AQI Values in the US by Year"
    data['Max AQI'].hist(by=data['Year'])
    plt.suptitle("Histograms by year for the Maximum AQI in each county of the US")
    plt.savefig(name)
    plt.close()

AirQualityHist(air)

##This function creates a histogram showing the frequency of water quality levels
def waterQualityHist(result):
    name = "Number of counties at different water quality levels"
    result['Value'].hist(by=result['Year'])
    plt.suptitle("Counties at different water quality levels")
    plt.savefig(name)
    plt.close()

waterQualityHist(water) 

##Code for 10 mean/med/mode/std####
#This function describes the mean, median and std for 5 attributes in the air quality dataset
def AirQualitymeans(data):
    
    
    Max_AQI_mean = data['Max AQI'].mean()
    Max_AQI_med = data['Max AQI'].median()
    Max_AQI_std = data['Max AQI'].std()
    
    Good_mean = data['Good Days_Norm'].mean()
    Good_med = data['Good Days_Norm'].median()
    Good_std = data['Good Days_Norm'].std()
    
    Mod_mean = data['Moderate Days_Norm'].mean()
    Mod_med = data['Moderate Days_Norm'].median()
    Mod_std = data['Moderate Days_Norm'].std()
    
    UHFSG_mean = data['Unhealthy for Sensitive Groups Days_Norm'].mean()
    UHFSG_med = data['Unhealthy for Sensitive Groups Days_Norm'].median()
    UHFSG_std = data['Unhealthy for Sensitive Groups Days_Norm'].std()
    
    Haz_mean =data['Hazardous Days_Norm'].mean()
    Haz_med = data['Hazardous Days_Norm'].median()
    Haz_std = data['Hazardous Days_Norm'].std()

    name= "Percentage of Good Days"
    data['Good Days_Norm'].hist()
    plt.suptitle(name)
    plt.savefig(name)
    plt.close()
    
    print("The average Max AQI Value across all counties for all years is: ",
          Max_AQI_mean, "with a standard deviation of: ", Max_AQI_std)
    print("The median is: ", Max_AQI_med)

    print("\n\nThe average percentage of Good Days across all counties for all years is: ",
          Good_mean *100, "%, with a standard deviation of: ", Good_std *100, "%")
    print("The median percentage is: ", Good_med*100, "%")

    print("\n\nThe average percentage of Moderate Days across all counties for all years is: ",
          Mod_mean *100, "%, with a standard deviation of: ", Mod_std *100, "%")
    print("The median percentage is: ", Mod_med*100, "%")

    print("\n\nThe average percentage of Unhealthy for Sensitive Groups Days across all counties for all years is: ",
          UHFSG_mean *100, "%, with a standard deviation of: ", UHFSG_std *100, "%")
    print("The median percentage: ", UHFSG_med*100, "%")

    print("\n\nThe average percentage of Hazardous Days across all counties for all years is: ",
          Haz_mean *100, "%, with a standard deviation of: ", Haz_std *100, "%")
    print("The median percentage is: ", Haz_med*100, "%")

AirQualitymeans(air)

def Cancermeans(data):
    #This function describes the mean, median and std for 3 attributes in the cancer dataset
    
	AA_mean = data[['Age-Adjusted Incidence Rate(†) - cases per 100,000']][
            data['Category']=='All'].mean()
	AA_med = data[['Age-Adjusted Incidence Rate(†) - cases per 100,000']][
            data['Category']=='All'].median()
	AA_std = data[['Age-Adjusted Incidence Rate(†) - cases per 100,000']][
            data['Category']=='All'].std()
    
	Count_mean = data[['Average Annual Count']][data['Category']=='All'].mean()
	Count_med = data[['Average Annual Count']][data['Category']=='All'].median()
	Count_std = data[['Average Annual Count']][data['Category']=='All'].std()

	yr_mean = data[['Recent 5-Year Trend (‡) in Incidence Rates']][data['Category']=='All'].mean()
	yr_med = data[['Recent 5-Year Trend (‡) in Incidence Rates']][data['Category']=='All'].median()
	yr_std = data[['Recent 5-Year Trend (‡) in Incidence Rates']][data['Category']=='All'].std()

	print("The average age adjusted incidence rate across all counties for all years is: ",
       AA_mean[0], "with a standard deviation of: ", AA_std[0])
	print("The median is: ", AA_med[0])

	print("\n\nThe average annual count of new cancer cases across all counties for all years is: ",
       Count_mean[0], " with a standard deviation of: ", Count_std[0] )
	print("The median is: ", Count_med[0])

	print("\n\nThe average trend in incidence rates across all counties for all years is: ",
       yr_mean[0], "%, with a standard deviation of: ", yr_std[0], "%")
	print("The median percentage is: ", yr_med[0], "%")

Cancermeans(cancer)

def waterQualitymeans(result):
    #This function describes the mean, median and std for 2 attributes in the cancer dataset
    Arsenic_content_mean=statistics.mean(result['Value']) 
    Arsenic_content_median=statistics.median(result['Value']) 
    Arsenic_content_sd=statistics.stdev(result['Value']) 
    Quality_mode=statistics.mode(result['Quality'])
    print("The average Arsenic_content in water across all counties for all years is: ",
          Arsenic_content_mean, "with a standard deviation of: ", Arsenic_content_median)
    print("The median is: ", Arsenic_content_sd)
    print("The mode of water quality level is ", Quality_mode)
 
waterQualitymeans(water)






######### ASSOCIATION RULE MINING CODE ####################################
def AssociationRuleMining(cancer, water, air):
    avg_value = water.groupby('FIPS', as_index=False)['Value'].mean()
    ### According to documents in its original website:
    ### level < 1 means non-dect arsenic
    ### level in (1-10) means less than MCL == "no harm"
    ### level in (10-50) means "harmful"
    bins = [-1,1,10,60]
    labels=['Non Detect','Less than or equal MCL','More than MCL' ]
    avg_value['Quality']=pd.cut(avg_value['Value'],bins,labels=labels)
    
    #calculate norms over all time
    max_aqi = air.groupby('FIPS', as_index=False)['Max AQI'].max()
    ninetieth = air.groupby('FIPS', as_index=False)['90th Percentile AQI'].mean()
    median = air.groupby('FIPS', as_index=False)['Median AQI'].mean()
    bins = [0,50,100,150,200,300,500]
    labels=['Good Max AQI','Moderate Max AQI','Unhealthy for Sensitive Groups Max AQI','Unhealthy Max AQI',
   	'Very Unhealthy Max AQI', 'Hazardous Max AQI']
    max_aqi['Max AQI Level']=pd.cut(max_aqi['Max AQI'],bins,labels=labels)
    labels=['Good 90th','Moderate 90th','Unhealthy for Sensitive Groups 90th','Unhealthy 90th',
            'Very Unhealthy 90th', 'Hazardous 90th']
    ninetieth['90th Percentile Level']=pd.cut(ninetieth['90th Percentile AQI'],bins,labels=labels)
    
    labels=['Good Median','Moderate Median','Unhealthy for Sensitive Groups Median','Unhealthy Median',
            'Very Unhealthy Median', 'Hazardous Median']
    median['Median Level']=pd.cut(median['Median AQI'],bins,labels=labels)
    wca = pd.merge(cancer[['FIPS', 'Recent Trend', 'Incidence Quant']][
           cancer['Category']=='All'], avg_value, on='FIPS')
    wca = pd.merge(wca, max_aqi, on='FIPS')
    wca = pd.merge(wca, ninetieth, on='FIPS')
    wca = pd.merge(wca, median, on='FIPS')
    asm = wca[['FIPS', 'Recent Trend', 'Incidence Quant', 'Quality', 'Max AQI Level', '90th Percentile Level', 'Median Level']]
    asm = wca[['Incidence Quant', 'Quality', '90th Percentile Level']]
    
    records = []
    for i in range(0, 599):  
        records.append([str(asm.values[i,j]) for j in range(0, 3)])

    #14 results
    results = list(apriori(records, min_support=0.0003, min_confidence=0.1, min_lift=2, min_length=2))
    #12 results
    results = list(apriori(records, min_support=0.0005, min_confidence=0.2, min_lift=2, min_length=2))
    #11 rules    
    results = list(apriori(records, min_support=0.001, min_confidence=0.3, min_lift=2, min_length=2))
    for item in results:
    	hypo = ''.join([x+' ' for x in item.ordered_statistics[0].items_base])
    	conc = ''.join([x+' ' for x in item.ordered_statistics[0].items_add])
    	print(str(hypo)+ " --> "+str(conc))
    	print("Support: " + str(item[1]))
    	print("Confidence: " + str(item[2][0][2]))
    	print("Lift: " + str(item[2][0][3]))
    	print("-----------------------------------")

AssociationRuleMining(cancer, water, air)

############################################################################
######### Hypothesis test -- KNN and Decision Trees ###############################
# Hypothesis → can air and water data be used to predict 5 year average age adjusted 
# cancer incidence rates per 100,000.  

# Calculate 5-year averages for Input data.  Merging cancer data to air
# and water reduced the number of data entries.  The counties in each data
# set does not seem to be overlapping.  
median = air.groupby('FIPS', as_index=False)['Median AQI'].mean()
pm = air.groupby('FIPS', as_index=False)['Days PM2.5_Norm'].mean()
so2 = air.groupby('FIPS', as_index=False)['Days SO2_Norm'].mean()
co = air.groupby('FIPS', as_index=False)['Days CO_Norm'].mean()
no2 = air.groupby('FIPS', as_index=False)['Days NO2_Norm'].mean()
ozone = air.groupby('FIPS', as_index=False)['Days Ozone_Norm'].mean()
ar = water.groupby('FIPS', as_index=False)['Value'].mean()


dataSubset = pd.merge(median, ar, on='FIPS')
dataSubset = pd.merge(dataSubset, ozone, on='FIPS')
dataSubset = pd.merge(dataSubset, pm, on='FIPS')
# Class label.
labels = cancer[['FIPS', 'Incidence Quant']][cancer['Category']=='All']

dataSubset = pd.merge(dataSubset, labels, on='FIPS')
dataSubset = dataSubset.drop('FIPS', axis=1)
dataSubset = dataSubset.dropna()

dataSubset['Incidence Quant'] = dataSubset['Incidence Quant'].astype('category')

def evaluateKnnDecisionTree(data):
      '''Evaluates different algorithms and their effectiveness at predicting
      the diabetes dataset.  The best accuracy score should be used to classify
      the test dataset'''
      # Separate training and final validation data set. First remove class
      # label from data (X). Setup target class (Y)
      # Then make the validation set 20% of the entire
      # set of labeled data (X_validate, Y_validate)
      test_size = 0.20  # Size of the test subset is 20% of the entire dataset
      seed = 7
      valueArrayD = data.values
      #X = valueArrayD[:,0:6]
      #Y = valueArrayD[:,6]
      X = valueArrayD[:,0:4]
      Y = valueArrayD[:,4]
      X_train, X_validate, Y_train, Y_validate = \
            model_selection.train_test_split(X, Y, test_size=test_size,
                                 random_state=seed)
      # Setup -fold cross validation to estimate the accuracy of different 
      # models.
      # Split data into 10 subsets.
      # Test options and evaluation metric.
      num_folds = 10
      seed = 7
      scoring = 'accuracy'
      # Add each algorithm and its name to the model array
      models = []
      models.append(('KNN', KNeighborsClassifier()))
      models.append(('CART', DecisionTreeClassifier()))
      
      # Normalized the training input dataset.
      #X_train[:,[0,2]] = normalize(X_train[:,[0,2]])
      X_train_norm = X_train
      # Normalize test dataset.
      #X_validate[:,[0,2]] = normalize(X_validate[:,[0,2]])
      X_validate_norm = X_validate
      
      # Evaluate each model.
      # Print the accuracy results (remember these are averages and std)
      print("Results from cross validation test:")
      for name, model in models:
            kfold = model_selection.KFold(n_splits=num_folds, 
                                          random_state=seed)
            cv_results_d = model_selection.cross_val_score(model, 
                                                           X_train_norm, 
                                                           Y_train, cv=kfold,
                                                           scoring=scoring)
            # cv_results2 are the accuracy results for each of the 10 subsets
            msg_d = "%s: \t mean=%f \t standard deviation={%f)"% (name,
                                                           cv_results_d.mean(),
                                                           cv_results_d.std())
            print(msg_d)
      # Using knn for the validation test.
      knn = KNeighborsClassifier()
      knn = knn.fit(X_train_norm, Y_train)
      predictions_d = knn.predict(X_validate_norm)
      print("\nThe accuracy score, confusion matrix, and classification " +
            "report for KNN is: \n", accuracy_score(Y_validate, 
                                                    predictions_d))
      print(confusion_matrix(Y_validate, predictions_d))
      print(classification_report(Y_validate, predictions_d))
      
      # Using decision tree for the validation test.
      dtc = DecisionTreeClassifier()
      dtc = dtc.fit(X_train_norm, Y_train)
      predictions_d = dtc.predict(X_validate_norm)
      print("\nThe accuracy score, confusion matrix, and classification " +
            "report for decision tree is: \n", accuracy_score(Y_validate, 
                                                    predictions_d))
      print(confusion_matrix(Y_validate, predictions_d))
      print(classification_report(Y_validate, predictions_d))
      
evaluateKnnDecisionTree(dataSubset)

################################### clustering analysis########################
###############################################################################
# average water value to match the average annual cancer count
avg_value = water.groupby('FIPS', as_index=False)['Value'].mean()
# subset all type cancer
cancer_alltype = cancer.loc[cancer['Category'] == 'All']
# merge chosen columns in cancer and water avg value
cancer_water = pd.merge(cancer_alltype[['FIPS','Average Annual Count']],avg_value,on='FIPS')
### cancer data has more fips than water/avg_value
###a = cancer_alltype['FIPS']
###b = avg_value['FIPS']
#list_1 = ["a", "b", "c", "d", "e"]
#list_2 = ["a", "f", "c", "m"] 
#morecancerfips = np.setdiff1d(b,a)
avg_gooddaynorm = air.groupby('FIPS', as_index=False)['Good Days_Norm'].mean()
#c = cancer_water['FIPS']
#d = avg_gooddaynorm['FIPS']
#list_1 = ["a", "b", "c", "d", "e"]
#list_2 = ["a", "f", "c", "m"] 
#morecancerfips = np.setdiff1d(c,d)
cancer_water_air = pd.merge(cancer_water,avg_gooddaynorm,on='FIPS')

##### Hierarchical Clustering
def getDendrogram(cancer_water_air):
    # Remove missing data 
    cancer_water_air = cancer_water_air.dropna()
    # normalize data
    mycancer_water_air=pd.concat([cancer_water_air['Average Annual Count'], cancer_water_air['Value'], cancer_water_air['Good Days_Norm']], 
                 axis=1, keys=['Average Annual Count','Value','Good Days_Norm' ])
    x = mycancer_water_air.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    normalizedDataFrame.columns = ['Average Annual Count','Value','Good Days_Norm']
    
    # generate the linkage matrix
    Z = linkage(normalizedDataFrame, 'ward')
    # calculate full dendrogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()
    plt.close()

def Hier_clustering(cancer_water_air,k):
    # Remove missing data 
    cancer_water_air = cancer_water_air.dropna()
    # normalize data
    mycancer_water_air=pd.concat([cancer_water_air['Average Annual Count'], cancer_water_air['Value'], cancer_water_air['Good Days_Norm']], 
                 axis=1, keys=['Average Annual Count','Value','Good Days_Norm' ])
    x = mycancer_water_air.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    normalizedDataFrame.columns = ['Average Annual Count','Value','Good Days_Norm']
    
    model = AgglomerativeClustering(n_clusters=k, affinity = 'euclidean', linkage = 'ward')
    clust_labels1 = model.fit_predict(normalizedDataFrame)
    agglomerative = pd.DataFrame(clust_labels1)
    
    # Determine if the clustering is good
    silhouette_avg = silhouette_score(normalizedDataFrame, clust_labels1)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    #centroids = model.cluster_centers_
    pprint(dict(pd.Series(clust_labels1).value_counts()))
    #pprint(centroids)
    
    # plot the clustering in 3D graph
    fig = plt.figure()
    ax = Axes3D(fig)
    scatter = ax.scatter(normalizedDataFrame['Value'],normalizedDataFrame['Good Days_Norm'],normalizedDataFrame['Average Annual Count'],
                         c=agglomerative[0],s=80,alpha=0.8)
    ax.set_title('Hierarchical Clustering')
    ax.set_xlabel('arsenic in water')
    ax.set_ylabel('rates of good air quality days per year')
    ax.set_zlabel('cancer rate')
    ax.set_zlim3d(0.0,0.3)
    ax.set_ylim3d(0.2,1.2)
    plt.colorbar(scatter)
    plt.close()
    

#####
#K means Clustering 
#####
def KMeans_cluster(cancer_water_air,k):
    # Remove missing data 
    cancer_water_air = cancer_water_air.dropna()
    # normalize data
    mycancer_water_air=pd.concat([cancer_water_air['Average Annual Count'], cancer_water_air['Value'], cancer_water_air['Good Days_Norm']], 
                 axis=1, keys=['Average Annual Count','Value','Good Days_Norm' ])
    x = mycancer_water_air.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    normalizedDataFrame.columns = ['Average Annual Count','Value','Good Days_Norm']
    
    kmeans = KMeans(n_clusters=k)
    cluster_labels = kmeans.fit_predict(normalizedDataFrame)

    # Determine if the clustering is good
    silhouette_avg = silhouette_score(normalizedDataFrame, cluster_labels)
    print("For n_clusters =", k, "The average silhouette_score is :", silhouette_avg)
    centroids = kmeans.cluster_centers_
    pprint(dict(pd.Series(cluster_labels).value_counts()))
    pprint(centroids)
    
    # plot the clustering in 3D graph
    kmeans = pd.DataFrame(cluster_labels)
    fig = plt.figure()
    ax = Axes3D(fig)
    scatter = ax.scatter(normalizedDataFrame['Value'],normalizedDataFrame['Good Days_Norm'],normalizedDataFrame['Average Annual Count'],
                         c=kmeans[0],s=80,alpha=0.8)
    ax.set_title('K-Means Clustering')
    ax.set_xlabel('arsenic in water')
    ax.set_ylabel('rates of good air quality days per year')
    ax.set_zlabel('cancer rate')
    ax.set_zlim3d(0.0,0.3)
    ax.set_ylim3d(0.2,1.2)
    plt.colorbar(scatter)
    plt.close()
    

    
# dbscan clustering
def DBSCAN_clustering(cancer_water_air):
    # Remove missing data 
    cancer_water_air = cancer_water_air.dropna()
    # normalize data
    mycancer_water_air=pd.concat([cancer_water_air['Average Annual Count'], cancer_water_air['Value'], cancer_water_air['Good Days_Norm']], 
                 axis=1, keys=['Average Annual Count','Value','Good Days_Norm' ])
    x = mycancer_water_air.values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalizedDataFrame = pd.DataFrame(x_scaled)
    normalizedDataFrame.columns = ['Average Annual Count','Value','Good Days_Norm']
    
    
    model = DBSCAN(eps=0.05, metric='euclidean', min_samples=5)
    clust_labels2 = model.fit_predict(normalizedDataFrame)
    dbscan = pd.DataFrame(clust_labels2)
    
    
    
    # Determine if the clustering is good
    silhouette_avg = silhouette_score(normalizedDataFrame, clust_labels2)
    print("The average silhouette_score is :", silhouette_avg)
    #centroids = model.cluster_centers_
    pprint(dict(pd.Series(clust_labels2).value_counts()))
    #pprint(centroids)
    
    # plot the clustering in 3D graph
    fig = plt.figure()
    ax = Axes3D(fig)
    scatter = ax.scatter(normalizedDataFrame['Value'],normalizedDataFrame['Good Days_Norm'],normalizedDataFrame['Average Annual Count'],
                         c=dbscan[0],s=80,alpha=0.8)
    ax.set_title('DBSCAN Clustering')
    ax.set_xlabel('arsenic in water')
    ax.set_ylabel('rates of good air quality days per year')
    ax.set_zlabel('cancer rate')
    ax.set_zlim3d(0.0,0.3)
    ax.set_ylim3d(0.2,1.2)
    plt.colorbar(scatter)
    plt.close()
    
    
## call functions
getDendrogram(cancer_water_air)
Hier_clustering(cancer_water_air,4)
KMeans_cluster(cancer_water_air,4)
DBSCAN_clustering(cancer_water_air)

############################ CORRELATION######################################
##############################################################################
# Calculate 5-year averages for Input data.  Merging cancer data to air
# and water reduced the number of data entries.  The counties in each data
# set does not seem to be overlapping.  
median = air.groupby('FIPS', as_index=False)['Median AQI'].mean()
pm = air.groupby('FIPS', as_index=False)['Days PM2.5_Norm'].mean()
so2 = air.groupby('FIPS', as_index=False)['Days SO2_Norm'].mean()
co = air.groupby('FIPS', as_index=False)['Days CO_Norm'].mean()
no2 = air.groupby('FIPS', as_index=False)['Days NO2_Norm'].mean()
ozone = air.groupby('FIPS', as_index=False)['Days Ozone_Norm'].mean()
ar = water.groupby('FIPS', as_index=False)['Value'].mean()
#data = pd.merge(median, pm, on='FIPS')
data = pd.merge(median, ar, on='FIPS')
data = pd.merge(data, ozone, on='FIPS')
data = pd.merge(data, pm, on='FIPS')
#data = pd.merge(data, so2, on='FIPS')
#data = pd.merge(data, co, on='FIPS')
#data = pd.merge(data, no2, on='FIPS')
#data = pd.merge(data, ar, on='FIPS')

# Class label.
labels = cancer[['FIPS', 'Incidence Quant']][cancer['Category']=='All']

data = pd.merge(data, labels, on='FIPS')
data = data.drop('FIPS', axis=1)
data = data.dropna()

scatter_matrix(data)
plt.show()
# calculate the correlation matrix
corr = data.corr() # contains the matrix of correlation coefficients
# plot the heatmap - creates a colorful matrix 
plt.figure()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns, cmap='GnBu')
plt.show()
plt.close()

#############################################################################
############### hypothesis 1(t-test & linear regression) #####################
##############################################################################
def hypo1(cancer, water):
    
    cancerSubset =cancer[cancer['Group']=='Total']    
    # create aa new data frame named cancer_new
    cancer_new = pd.DataFrame(columns = ["FIPS", "cancer_incidence"]) 
    cancer_new['FIPS']=cancerSubset['FIPS']
    cancer_new['cancer_incidence']=cancerSubset['Age-Adjusted Incidence Rate(†) - cases per 100,000']
    cancer_new=cancer_new.dropna()  # drop cancer_incidence=NaN


    result_prep = water.groupby(['FIPS','County','State'])['Value'].mean()
    result_prep = result_prep.to_frame().reset_index()
    
    ######### combine two tables#######################
    water_cancer = pd.merge(result_prep, cancer_new,on="FIPS",how='inner')#### combine tables by FIPS
    
    water_cancer['cancer_incidence']=pd.to_numeric(water_cancer['cancer_incidence'])
    water_cancer['Value']=pd.to_numeric(water_cancer['Value'])
    del water_cancer['FIPS']
    del water_cancer['County']
    del water_cancer['State']
    #Now, here is a table 'water_cancer' that only contain
    # the value of arsenic in water and the cancer incident
    
    
    ## 1.t-test and linear regression
    # H0: counties with arsenic at 'non-detected' level have the same cancer rate with arsenic detected 
    water_cancer1=water_cancer[water_cancer['Value']<=1]
    water_cancer2=water_cancer[water_cancer['Value']>1]
    cancer_gw=water_cancer1['cancer_incidence']# cancer incedence of water at 'non-detected' level
    cancer_bw=water_cancer2['cancer_incidence']# cancer incedence of water at 'non-detected' level
    
    p_value=stats.ttest_ind(cancer_gw,cancer_bw, equal_var = False)
    print(p_value)
    # Here, the pvalue=0.000283, which is smaller than 0.05. 
    # So counties with arsenic at 'non-detected' level have different cancer rate with arsenic at 'detectable' level 
    
    
    # 2.Linear Regression: y=ax+b, where the x= result['value'] and y=cancer['cancer_incidence']
    x= water_cancer.iloc[:, :-1].values   # x is the arsenic_content
    y = water_cancer.iloc[:, 1].values   #y is cancer incidence
    reg = LinearRegression().fit(x, y) # fit the model
    
    print('intercept is ',reg.intercept_)
    print('coefficient is ',reg.coef_)
    #the intercept in the regression is 456.85 and the slope is -4.91
    # so the linear regression is cancer_incidence=-4.91*arsenic_content+456.85
    
    plt.scatter(x, y, facecolor='None', edgecolor='k', alpha=0.3)
    plt.title("prediction of cancer incidence from water quality")
    plt.xlabel("arsenic content (µg/L)")
    plt.ylabel("cancer incidence(/100,000)")

    plt.plot(x, reg.predict(x.reshape(-1,1)), color='red')
    plt.show()
    plt.close()

hypo1(cancer, water)


###########################################################################
### Hypotheis 3: using SVM, NB and Random Forest
### Using water Impurity data, air quality(days) and cancer trend to predict the cancer trend.
### More impurity in water and less good days, the cancer trend will be cause more cancer rate 
def TrendHypo(cancer, water, air):
    
    cancerTotal = cancer[cancer['Group'] == 'Total']
    cancerData = cancerTotal[['FIPS','Recent Trend']]
    
    #waterTotal = water.groupby(['FIPS','County','State'])['Value'].mean()
    #waterTotal = waterTotal.to_frame().reset_index()
    # fix water data FIPS 
   # waterTotal['WaterImpurity'] = waterTotal['Value']
    #waterTotal = waterTotal.drop(['State', 'County','Value'], axis=1)
    
    
    airTotal = air.groupby(['FIPS','County','State'])['Median AQI'].mean()
    airTotal = airTotal.to_frame().reset_index()
    airTotal = airTotal.drop(['State', 'County'], axis=1)
    
    ############## Merging data into a new dataframe ############## 
    hypoData = pd.merge(airTotal, cancerData, on='FIPS',how='inner')
    #hypoData = pd.merge(waterTotal, airCancer, on='FIPS')
    hypoData = hypoData.drop(['FIPS'], axis=1)
    hypoData = hypoData.dropna()
    hypoData['Recent Trend'] = hypoData['Recent Trend'].astype('category')
    
    
    #######################################################
    ## Plot the new merging data
    #######################################################
    hypoData.plot(kind='box', subplots=True, layout=(3,3), sharex=False, sharey=False)
    hypoGroup = hypoData.groupby(['Recent Trend'])['Median AQI'].mean()
    hypoGroup.plot.bar()
    scatter_matrix(hypoData)
    plt.show()
    plt.close()
    
    ######################################################
    # Evaluate algorithms
    ######################################################
    
    # Separate training and final validation data set. First remove class
    # label from data (X). Setup target class (Y)
    # Then make the validation set 20% of the entire
    # set of labeled data (X_validate, Y_validate)
    
    # Normalize all data
    hypotest = pd.DataFrame()
    hypotest['Median AQI'] = hypoData['Median AQI']
    #hypotest['WaterImpurity'] = hypoData['WaterImpurity']
    dt = hypotest.values
    valueArray = normalize(dt, axis=0, norm='max')
    
    
    valueArray = hypoData.values
    X = valueArray[:,0:1]
    Y = valueArray[:,1]
#    X = sklearn.preprocessing.normalize(X)
    test_size = 0.20
    seed = 7
    X_train, X_validate, Y_train, Y_validate = cross_validation.train_test_split(X, Y, test_size=test_size, random_state=seed)
    
    # Setup 10-fold cross validation to estimate the accuracy of different models
    # Split data into 10 parts
    # Test options and evaluation metric
    num_folds = 10
    num_instances = len(X_train)
    seed = 7
    scoring = 'accuracy'
    
    ######################################################
    # Use different algorithms to build models
    ######################################################
    
    # Add each algorithm and its name to the model array
    models = []
    models.append(('NB', GaussianNB()))
    models.append(('SVM', SVC()))
    
    # Evaluate each model, add results to a results array,
    # Print the accuracy results (remember these are averages and std
    results = []
    names = []
    for name, model in models:
    	kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
    	cv_results = cross_validation.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
    	results.append(cv_results)
    	names.append(name)
    	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    	print(msg)
    
    
    ######################################################
    # For the best model, see how well it does on the
    # validation test. For example - this is for SVM
    ######################################################
    # Make predictions on validation dataset
    
    svm = SVC()
    svm.fit(X_train, Y_train)
    predictions = svm.predict(X_validate)
        
    
    print("\nThe accuracy score for SVM is:")
    print(accuracy_score(Y_validate, predictions))
    print(confusion_matrix(Y_validate, predictions))
    print(classification_report(Y_validate, predictions))
        
    
    print("\nThe accuracy score for NBGaussian is:")    
    nb = GaussianNB()
    nb.fit(X_train, Y_train)
    predictions_nb = nb.predict(X_validate)
    print(accuracy_score(Y_validate, predictions_nb))
    
    print("\n")
    
    
    ###### Random Forest
    
    print("\nThe random Forest hypothesis is:")  
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(X_train, Y_train)
    predicted = model.predict(X_validate)
    predictedInfo = pd.DataFrame(predicted, columns=['Prediction'])
    print(predictedInfo.describe())
    
TrendHypo(cancer, water, air)

##This function creates a histogram showing the frequency of cancer incidence by county/group
def cancerHist(result):
    name= "Cancer Incidence Rates by Group Histogram"
    result['Age-Adjusted Incidence Rate(†) - cases per 100,000'].hist(by=result['Group'])
    plt.suptitle("Number of counties at different Cancer Incidence Rates")
    plt.savefig(name)

cancerHist(cancer)

def AirBin(air):
    bins = [0, 0.2 , 0.4, 0.6, 0.8, 1]
    labels = [int(1),int(2),int(3),int(4),int(5)]
    air['Good Day Bin'] = pd.cut(air['Good Days_Norm'], bins=bins, labels=labels)
    
    
    return air
    
air = AirBin(air)

#####network#########
def network():
    import networkx as nx
    
    #print(air[:10])
    ##combine cancer air and water
    avg_value = water.groupby('FIPS', as_index=False)['Value'].mean()

    cancer_alltype = cancer.loc[cancer['Category'] == 'All']
    cancer_water = pd.merge(cancer_alltype[['FIPS','Incidence Quant','State']],avg_value, on='FIPS')

    air_new = air[['FIPS', 'Good Day Bin']]
    combined_data = pd.merge(air_new,cancer_water,on='FIPS')
    
    #print(combined_data[:10])
    #choose only california for analysis
    california = combined_data.loc[combined_data['State'] == 'California']
    california.to_csv('cali.txt')
    #print(california[:10])
    combined_data.to_csv('total.txt')
    
    import csv
    #draw network, connnect if same cancer rate###
    G = nx.Graph()
    #G = nx.cycle_graph(80)
    #pos = nx.circular_layout(G)
    f = csv.reader(open("cali.txt"),delimiter=',')
    #f= csv.reader(open('total.txt'), delimiter=',')
    next(f)
    node_color = []

    for row in f:
        attributes={'Air Quality': row[2], 'Cancer Rate': row[3], "State": row[4], "Water Quality": row[5]}
        G.add_node(row[1], attr_dict= attributes)
        for node in G.nodes(data=True):

    # if the node has the attribute group1
            if '1' in node[1]['attr_dict']['Air Quality']:
                node_color.append('red')

    # if the node has the attribute group1
            elif '2' in node[1]['attr_dict']['Air Quality']:
                node_color.append('blue')

    # if the node has the attribute group1
            elif '3' in node[1]['attr_dict']['Air Quality']:
                node_color.append('blue')

    # if the node has the attribute group1
            elif '4' in node[1]['attr_dict']['Air Quality']:
                node_color.append('green')

    # if the node has the attribute group1
            elif '5' in node[1]['attr_dict']['Air Quality']:
                node_color.append('green') 
        
    
    for node_r in G.nodes(data=True):
        for node in G.nodes(data=True):
            if node != node_r and node[1]['attr_dict']['Cancer Rate'] == node_r[1]['attr_dict']['Cancer Rate']:
                G.add_edge(node[0], node_r[0], attr_dict=None) 

    ####calculate local metrics#####
    
    #degree=G.degree(G.nodes)
    #avg_degree=nx.average_node_connectivity(G)
    #avg_connect=nx.average_degree_connectivity(G)
    #cluster= nx.average_clustering(G)
    #density=nx.density(G)
    #triang=nx.triangles(G)
    #centrality=nx.betweenness_centrality(G)

    #print("The degree for each county is: ",avg_degree)
    #print("\nThe average connectivity is: ",avg_connect)
    #print("\nThe clustering coefficient is: ",cluster)
    #print("\nThe triangle measure for each county is: ",triang)
    #print("\nThe density of the network is: ",density)
    #print("\nThe centrality is: ",centrality)
    
    
    # larger figure size
    plt.figure(figsize=(15,15)) 
    pos = nx.spring_layout(G,k=0.50,iterations=20)

    
    nx.draw(G,pos, with_labels=True, node_size= 200, node_color=node_color)
    
    
    plt.show()
 
    plt.savefig("network_cali.jpg")
    plt.close()
       

    #for n in G.nodes():
        #print('Node: ', n)
        #print('Atrributes',(G.node[n]['attr_dict']))
network()

#### focus on the hramful water(arsenic content>10µg/L)
def scatterplot_harmfulwater():
    
    cancerSubset =cancer[cancer['Group']=='Total']    
    # create aa new data frame named cancer_new
    cancer_new = pd.DataFrame(columns = ["FIPS", "cancer_incidence"]) 
    cancer_new['FIPS']=cancerSubset['FIPS']
    cancer_new['cancer_incidence']=cancerSubset['Age-Adjusted Incidence Rate(†) - cases per 100,000']
    cancer_new=cancer_new.dropna()  # drop cancer_incidence=NaN


    result_prep = water.groupby(['FIPS','County','State'])['Value'].mean()
    result_prep = result_prep.to_frame().reset_index()
    
    ######### combine two tables#######################
    water_cancer = pd.merge(result_prep, cancer_new,on="FIPS",how='inner')#### combine tables by FIPS
    
    water_cancer['cancer_incidence']=pd.to_numeric(water_cancer['cancer_incidence'])
    water_cancer['Value']=pd.to_numeric(water_cancer['Value'])
    del water_cancer['FIPS']
    del water_cancer['County']
    del water_cancer['State']
    #water_cancer=water_cancer[water_cancer['Value']>=10]
    #Now, here is a table 'water_cancer' that only contain FIPS,the value of arsenic in water and the cancer incident
    
    
    ## 1.t-test and linear regression
    # H0: counties with arsenic at 'non-detected' level have the same cancer rate with arsenic detected 
    water_cancer1=water_cancer[water_cancer['Value']<=10]
    water_cancer2=water_cancer[water_cancer['Value']>10]
    cancer_gw=water_cancer1['cancer_incidence']# cancer incedence of water at 'non-detected' level
    cancer_bw=water_cancer2['cancer_incidence']# cancer incedence of water at 'non-detected' level
        
    # 2.Linear Regression: y=ax+b, where the x= result['value'] and y=cancer['cancer_incidence']
    x= water_cancer2.iloc[:, :-1].values   # x is the arsenic_content
    y = water_cancer2.iloc[:, 1].values   #y is cancer incidence
    reg = LinearRegression().fit(x, y) # fit the model
    
    print('intercept is ',reg.intercept_)
    print('coefficient is ',reg.coef_)
    #the intercept in the regression is 375.122582516 and the slope is 2.72021998
    # so the linear regression is cancer_incidence=-4.91*arsenic_content+456.85
    
    # plot the scatter plot and regression of water and cancer
    plt.scatter(x, y,facecolor='blue', edgecolor='k', alpha=0.3)
    plt.title("trend of cancer incidence by harmful water quality")
    plt.xlabel("arsenic content (µg/L)")
    plt.ylabel("cancer incidence(/100,000)")

    plt.plot(x, reg.predict(x.reshape(-1,1)), color='blue')
    plt.show()
    plt.close()

scatterplot_harmfulwater()

def normansCode():
    # Have to specify dtype because FIPS State and FIPS County should be strings.
    # If this is not done, then python thinks its integers, which removes leading 0's.
    # Note, there might be bugs on an apple computer.  
    air = pd.read_csv('cleanPollutionData.csv', dtype={
            'FIPS State':object, 'FIPS County':object})
    
    water = pd.read_csv('water_clean.csv')
    cancer = pd.read_csv('cleaned_cancer.csv')
    # add leading 0's
    cancer['FIPS'] = cancer['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
    
    # fix water fips - add leading 0's.
    water['FIPS'] = water['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
    water['FIPS'] = water['FIPS'].astype(object)
    
    # Creating a single FIPS Column.
    air['FIPS'] = air['FIPS State'] + air['FIPS County']
    air = air.drop(['FIPS State', 'FIPS County'], axis=1)
    air['FIPS'] = air['FIPS'].str.replace("=", "")
    air['FIPS'] = air['FIPS'].str.replace("\"", "")
    
    cancer = cancer.dropna().reset_index(drop=True)
    temp = air.loc[:,'State'].unique()
    temp = pd.DataFrame(data=temp, index=None, columns=['State'])
    ###############################################################################
    ###############################################################################
    # Selecting category = All and group = Total
    cancer = cancer.loc[(cancer.loc[:, 'Category'] == 'All') & (
                        cancer.loc[:, 'Group'] == 'Total')]
    for state in air.loc[:,'State'].unique():
        temp.loc[temp.loc[:,'State'] == state, 'Days PM2.5'] = np.mean(
                air.loc[air.loc[:,'State'] == state, 'Days PM2.5'])
        temp.loc[temp.loc[:, 'State'] == state, 'Days PM10'] = np.mean(
                air.loc[air.loc[:, 'State'] == state, 'Days PM10'])
        temp.loc[temp.loc[:, 'State'] == state, 
                  'Age-Adjusted Incidence Rate(†) - cases per 1,000,000'] = np.mean(
                  cancer.loc[cancer.loc[:, 'State'] == state,
                             'Age-Adjusted Incidence Rate(†) - cases per 100,000'])/10
        
    # All numbers are rounded
    temp = round(temp)
    temp = temp.dropna().reset_index(drop=True)
    
    traceA = go.Bar(
            x=temp.loc[:,'State'].unique(),
            y=temp.loc[:,'Age-Adjusted Incidence Rate(†) - cases per 1,000,000'],
            name='Age-Adjusted Incidence Rate(†) - cases per 1,000,000',
            marker=dict(color='rgb(0,191,255)'))
    traceB = go.Bar(
            x=temp.loc[:,'State'].unique(),
            y=temp.loc[:,'Days PM2.5'],
            name='Days PM2.5',
            marker=dict(color='rgb(255,215,0)'))
    traceC = go.Bar(
            x=temp.loc[:,'State'].unique(),
            y=temp.loc[:,'Days PM10'],
            name='Days PM10',
            marker=dict(color='rgb(220,20,60)'))
    layout = go.Layout(
            title='Comparing number of days for PM2.5 and PM10 and Age-adjusted Cancer Rates for States',
            hovermode='closest',
            xaxis=dict(title='States',
                       ticklen=5,
                       zeroline=False),
            yaxis=dict(title='Values',
                       ticklen=5,
                       zeroline=False))
    temp = [traceA, traceB, traceC]
    figure = dict(data=temp, layout=layout)
    plotly.offline.plot(figure, filename='bar_plot.html')
    plt.close()
    ###############################################################################
    ###############################################################################
    ###############################################################################
    temp1 = air.loc[:,'State'].unique()
    temp1 = pd.DataFrame(data=temp1, index=None, columns=['State'])
    for state in air.loc[:,'State'].unique():
        temp1.loc[temp1.loc[:,'State'] == state, 'Mean Median AQI'] = np.mean(
                air.loc[air.loc[:,'State'] == state, 'Median AQI'])
        temp1.loc[temp1.loc[:, 'State'] == state, 
                  'Age-Adjusted Incidence Rate(†) - cases per 1,000,000'] = np.mean(
                  cancer.loc[cancer.loc[:, 'State'] == state,
                             'Age-Adjusted Incidence Rate(†) - cases per 100,000'])/10
        
    # All numbers are rounded
    temp1 = round(temp1)
    temp1 = temp1.dropna().reset_index(drop=True)
    
    traceA = go.Bar(
            x=temp1.loc[:,'State'].unique(),
            y=temp1.loc[:,'Age-Adjusted Incidence Rate(†) - cases per 1,000,000'],
            name='Age-Adjusted Incidence Rate',
            marker=dict(color='rgb(0,191,255)'))
    traceB = go.Bar(
            x=temp1.loc[:,'State'].unique(),
            y=temp1.loc[:,'Mean Median AQI'],
            name='Median AQI',
            marker=dict(color='rgb(255,215,0)'))
    layout = go.Layout(
            title='Comparing Median AQI and Age-adjusted Cancer Rates for each State',
            hovermode='closest',
            xaxis=dict(title='States',
                       ticklen=5,
                       zeroline=False),
            yaxis=dict(title='Values',
                       ticklen=5,
                       zeroline=False))
    temp = [traceA, traceB]
    figure = dict(data=temp, layout=layout)
    plotly.offline.plot(figure, filename='bar_plot_2.html')
    plt.close()
    
normansCode()

def waterimpurity ():
    
    ############## Import cancer data ##############
    cancerCSV1 = pd.read_csv('cleaned_cancer.csv') 
    cancerTotal1 = cancerCSV1[cancerCSV1['Group'] == 'Total']
    cancerData1 = pd.DataFrame(columns = ['FIPS','Recent Trend']) 
    # fix cancer data FIPS 
    cancerData1['FIPS'] = cancerTotal1['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
    cancerData1['Recent Trend'] = cancerTotal1['Recent 5-Year Trend (‡) in Incidence Rates']
    #cancerData['County'] = cancerTotal['County']
    #cancerData['State'] = cancerTotal['State']
    
    ############## Import Water data ##############
    waterCSV1 = pd.read_csv('water_clean.csv')
    
    waterTotal1 = waterCSV1
    waterTotal1['FIPS'] = waterTotal1['FIPS'].apply(lambda x: '{0:0>5}'.format(x))
    waterTotal1['WaterImpurity'] = waterTotal1['Value']
    waterTotal1 = waterTotal1.drop(['Value','Quality'], axis=1)
    # checking missing value of binned feature
    waterCSV1.info()
    waterCSV1['Quality'].describe()
    sum(waterCSV1['Quality'].isna())
    
    
    ############## Import air data ############## 
    airCSV1 = pd.read_csv('cleanPollutionData.csv')
    #fix air fips - combine state and county fips and get rid of = and “ characters
    airCSV1['FIPS'] = airCSV1['FIPS State'] + airCSV1['FIPS County']
    airCSV1['FIPS'] = airCSV1['FIPS'].str.replace("=", "")
    airCSV1['FIPS'] = airCSV1['FIPS'].str.replace("\"", "")
    
    airCSV1.info()
    airTotal1 = airCSV1.groupby(['FIPS','County','State'])['Days PM2.5'].mean()
    airTotal1 = airTotal1.to_frame().reset_index()
    airTotal1 = airTotal1.drop(['State', 'County'], axis=1)
    airTotal1['FIPS'] = airTotal1['FIPS']
    
    ############## Merging data into a new dataframe ############## 
    airCancer1 = pd.merge(airTotal1, cancerData1, on='FIPS',how='inner')
    hypoData1 = pd.merge(waterTotal1, airCancer1, on='FIPS')
    
    hypoData1 = hypoData1.drop(['FIPS'], axis=1)
    hypoData1 = hypoData1.dropna()
    #hypoData['Recent Trend'] = hypoData['Recent Trend'].astype('category')
    hypoData1['Recent Trend'] = pd.to_numeric(hypoData1['Recent Trend'])
    ##############visualization#####################
    
    waterPlutd = pd.DataFrame()
    waterPlutd = waterCSV1[waterCSV1['Value'] > 10]
    
#    hypoData1.info()
    DataPlutd = hypoData1[hypoData1['WaterImpurity'] > 10]
    
    plt.subplot(121)
    DataPlutd.groupby(['County','State'])['Recent Trend'].mean().plot(kind="bar")
    plt.title("Cancer Trend for high arsenic level area")
    #DataPlutd[['County','Recent Trend']].plot(kind="bar")
    
    plt.subplot(122)
    #DataPlutd.groupby(['County'])['Days PM2.5'].mean().unstack().plot(kind="bar")
    #DataPlutd.plot('County','Days PM2.5',kind='bar')
    DataPlutd.groupby(['County','State'])['Days PM2.5'].mean().plot(kind="bar")
    plt.title("The number of PM2.5 Days for high arsenic level area")

    waterPlutd.groupby(['County','State','Year'])['Value'].mean().unstack().plot(kind="bar")
    plt.title("High arsenic level area trend from 2011 - 2015")
    plt.show()
    plt.close()


waterimpurity()


########### scatter plot
air = pd.read_csv('cleanPollutionData.csv')
# Creating a single FIPS Column.
air['FIPS'] = air['FIPS State'] + air['FIPS County']
air = air.drop(['FIPS State', 'FIPS County'], axis=1)
air['FIPS'] = air['FIPS'].str.replace("=", "")
air['FIPS'] = air['FIPS'].str.replace("\"", "")
# subset only lung cancer
lungcancer = cancer.loc[cancer['Group'] == 'Lung Cancer']

# merge chosen columns in cancer and air avg value
avg_medianAQI= air.groupby('FIPS', as_index=False)['Median AQI'].mean()

lungcancer_air = pd.merge(lungcancer,avg_medianAQI,on='FIPS')
import matplotlib.pyplot as plt
plt.scatter(lungcancer_air['Median AQI'], lungcancer_air['Average Annual Count'], color='orange')
plt.title('Lung Cancer Counts by AQI Score')
plt.xlabel('Median AQI')
plt.ylabel('Average Annual Counts of Lung Cancer')
plt.show()
plt.close()