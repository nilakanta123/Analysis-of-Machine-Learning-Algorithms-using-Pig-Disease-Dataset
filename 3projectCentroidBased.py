import pandas as pd
import numpy as np
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

from sklearn.model_selection import GridSearchCV, cross_validate
import matplotlib.pyplot as plt

# @@@@@@@@@ Function to find performance of the model using 10 folds cross-validation @@@@@@
def modelfit(alg, feature, label, performCV=True, printFeatureImportance=True, cv_folds=10):
    alg.fit(feature, label)
    
    print ("\n~~ Model Report ~~~~~~~~")
    scoring = {'accuracy': 'accuracy',
    'precision' : 'precision_macro',
    'recall': 'recall_macro',
    'f1': 'f1_macro'}

    if performCV:
        prec_scores = cross_validate(alg, feature, label, cv=cv_folds, scoring = scoring)
        # print(prec_scores)
        print("ACCURACY : %0.3f" % prec_scores['test_accuracy'].mean())
        print("PRECISION: %0.3f" % prec_scores['test_precision'].mean())
        print("RECALL: %0.3f" % prec_scores['test_recall'].mean())
        print("f1: %0.3f" % prec_scores['test_f1'].mean())

    if printFeatureImportance:
        feat_imp = pd.Series(alg.feature_importances_, X.columns).sort_values(ascending=False)
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importance Score')
        plt.show()
    return alg

def plotCvResult(gridresult,param_list,param_name):
    plt.figure(figsize=(15, 10))
    plt.plot(param_list,gridresult.cv_results_['split1_train_score'],color='blue',marker='o',markersize=5,label='training accuracy')   
    plt.plot(param_list,gridresult.cv_results_['split1_test_score'],color='green',marker='x',markersize=5,label='test accuracy')    
    plt.xlabel(param_name)
    plt.ylabel('Accuracy')
    plt.legend(loc='lower right')
    plt.ylim([0.5,1])
    plt.show()

# @@@@@@@@ READING DATA @@@@@@@
df = pd.read_csv('am.csv')
# print(df)
df.drop(['Probable_agent'], axis=1, inplace=True)

# @@@@@@@@ LABEL ENCODING CLASSES @@@@@@@
from sklearn import preprocessing
labelEncoder = preprocessing.LabelEncoder()
labelEncoder.fit(df['Probable_disease'])
df['Probable_disease']=labelEncoder.transform(df['Probable_disease'])

# @@@@@@@@ SET FEATURE AND TARGET @@@@@@@@@@@
from sklearn.utils import shuffle
X, y = shuffle(df.iloc[:,:-1],df.Probable_disease, random_state=13)

from sklearn.neighbors.nearest_centroid import NearestCentroid

# # (1) TRAINING MODEL on Default Parameter
# base_model = NearestCentroid()
# modelfit(base_model,X,y,printFeatureImportance=False)
# # ACCURACY : 0.953
# # PRECISION: 0.920
# # RECALL: 0.931
# # f1: 0.923

# # (2) CHOICE PARAMETER metric
# param_test1 = {'metric' : ['euclidean','manhattan']}
# gsearch1 = GridSearchCV(estimator = NearestCentroid(),
#   scoring='accuracy',param_grid=param_test1, cv=10)
# gsearch1.fit(X,y)
# plotCvResult(gsearch1,param_test1['metric'],'metric')
# print("BEST PARAM : ",gsearch1.best_params_)
# print("ACCURACY : ", gsearch1.best_score_)
# # The best c is the one where training and testing curve are closest

# # (3) FINAL MODEL FITTING
# tuned_model = NearestCentroid(metric='euclidean')
# modelfit(tuned_model,X,y,printFeatureImportance=False)
# # ACCURACY : 0.967
# # PRECISION: 0.941
# # RECALL: 0.956
# # f1: 0.946