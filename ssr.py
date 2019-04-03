# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 19:59:33 2019

@author: kuttattu
"""
import pandas as pd
from sklearn.model_selection import train_test_split
df = pd.read_csv("my_csv.csv")
df['Learner']=df['Learner'].map({'A':0,'V':1,'K':2})
#print(df)
def preprocess_features(X):
    
    output = pd.DataFrame(index = X.index)

    # Investigate each feature column for the data
    #df.iteritems(): Iterator over (column name, Series) pairs.
    for col, col_data in X.iteritems():
        
        if col_data.dtype == object:
            col_data = col_data.replace(['yes', 'no'], [1, 0])

        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix = col)  
        
        output = output.join(col_data)
    
    return output
    
    
X_all=preprocess_features(df)

from sklearn.cluster import KMeans
n_clusters=7
kmeans = KMeans(n_clusters)
kmeans.fit(X_all)
centroids =(kmeans.cluster_centers_)
cluster = kmeans.predict(X_all)
print("Cluster Result:")
print(cluster)


x=X_all.iloc[:,:-1]
y=X_all.iloc[:,-1]
x['Cluster'] = cluster
x_train,x_test, y_train, y_test=train_test_split(x,y,test_size=0.30)

from sklearn.svm import SVC
model=SVC()
model.fit(x_train, y_train)
pred=model.predict(x_test)
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import accuracy_score
print("Accuracy:")
print(accuracy_score(y_test,pred))
print("Confusion Matrix :")
print(confusion_matrix(y_test,pred))
print("Classification Matrix :")
print(classification_report(y_test, pred))


from scipy.spatial import distance
cluster_distance=[]
for i in range(0,len(centroids)):
    temp=[]
    for c in centroids:
        temp.append(distance.euclidean(centroids[i],c))
    cluster_distance.append(temp)
print(cluster_distance)




