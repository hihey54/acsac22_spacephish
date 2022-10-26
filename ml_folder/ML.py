import pandas as pd
import time
import numpy as np
from sklearn.feature_selection import SelectKBest,chi2,f_classif,RFE,SequentialFeatureSelector
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score,KFold,cross_val_predict,cross_validate
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import svm,metrics,preprocessing,tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from collections import Counter
from sklearn.metrics import classification_report,confusion_matrix, recall_score,ConfusionMatrixDisplay,plot_confusion_matrix,precision_score,roc_curve,auc
import json
import joblib
from scipy.stats import pearsonr
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv1D,Dropout,MaxPooling1D,Flatten
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import os
import random
import operator
#cnn models
def create_model_cnn():
    model = Sequential()
    model.add(Conv1D(48, 2, activation="relu", input_shape=(58,1)))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Conv1D(64, 2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Conv1D(128,2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    #32
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(32, activation="relu"))
    model.add(Dense(2, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy',#sparse_categorical_crossentropy
      optimizer = "adam",
                metrics = [tf.keras.metrics.CategoricalAccuracy()])#CategoricalTruePositives(),CategoricalTrueNegative(),CategoricalFalseNegative()])#,CategoricalTrueNegative(),CategoricalFalseNegative(),CategoricalFalsePositive()]) #,metric_recall,metric_FPR
    #model.summary()
    return model

def create_model_html():
    model = Sequential()
    model.add(Conv1D(48, 2, activation="relu", input_shape=(22,1))) #48
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Conv1D(64, 2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Conv1D(128,2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Dense(64, activation="relu"))
    #32
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(32, activation="relu"))
    model.add(Dense(2, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy',#sparse_categorical_crossentropy
      optimizer ="adam",
                metrics = [tf.keras.metrics.CategoricalAccuracy()])
    return model

def create_model_url():
    model = Sequential()
    model.add(Conv1D(48, 2, activation="relu", input_shape=(36,1))) 
    model.add(Conv1D(64, 2, activation="relu"))
    model.add(Conv1D(64, 2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
    model.add(Conv1D(128,2, activation="relu"))
    model.add(Conv1D(128,2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))

    model.add(Conv1D(256,2, activation="relu"))
    model.add(Conv1D(256,2, activation="relu"))
    model.add(MaxPooling1D())
    model.add(Dropout(0.2))
     
    model.add(Flatten())
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(2, activation = 'softmax'))
    model.compile(loss = 'categorical_crossentropy',#sparse_categorical_crossentropy 
      optimizer ="adam", # "adam",               
                metrics = [tf.keras.metrics.CategoricalAccuracy()])#  
    #model.summary()
    return model
def get_fpr(y,y_pred):
    cm = confusion_matrix(y, y_pred)
    tn=cm[0, 0]
    fp=cm[0, 1]
    fn=cm[1, 0]
    tp=cm[1, 1]
    '''
    print('tn',tn)
    print('tp',tp)
    print('fp',fp)
    print('fn',fn)
    '''
    fpr=fp/(fp+tn)
    recall=tp/(tp+fn)
    return fpr,recall

def rfe_get_score(model,num,data,label,test_x,test_y):
    #print('==============mmodel',str(model))
    rfe = RFE(estimator=LogisticRegression(max_iter=1000), n_features_to_select=num)
    rfe=rfe.fit(data,label)
    x_rfe=rfe.transform(data)#must change to this, only fit the train data, but transfer the test data to this format
    test_x_rfe=rfe.transform(test_x)
    start=time.time()
    model.fit(x_rfe,label)
    end=time.time()
    time1=(end-start)*1000
    #print('selected feature in test part',test_x_rfe.support_)
    cv_results = cross_validate(model, test_x_rfe, test_y, cv=10,
                            scoring=confusion_matrix_scorer)
    #print('cv_results',cv_results)
    fprs=cv_results['test_score']
    fpr_ave=np.mean(fprs)
    fpr_std=np.std(fprs)
    #get the standard devition of cross_validation
    recalls=cross_val_score(model,test_x_rfe,test_y,scoring='recall',cv=10)
    recall=np.mean(recalls)
    #print('recall:',recall) 
    re_std=np.std(recalls)
    #print('re_std',re_std)
    #print('fpr_ave',fpr_ave) 
    #print('fpr_std',fpr_std)
    #print('training time:',time1)
    return model,fpr_ave,fpr_std,recall,re_std,time1,rfe

def chi_get_score(model,data,label,test_x,test_y,num):
    chi2_selector = SelectKBest(chi2, k=num)
    chi2_selector=chi2_selector.fit(data,label)
    train_x_chi2 = chi2_selector.transform(data)
    test_x_chi2=chi2_selector.transform(test_x)
    start=time.time()
    model.fit(train_x_chi2,label)
    end=time.time()
    time1=(end-start)*1000
    cv_results = cross_validate(model, test_x_chi2, test_y, cv=10,
                            scoring=confusion_matrix_scorer)
    fprs=cv_results['test_score']
    fpr_ave=np.mean(fprs)
    print('fpr_ave',fpr_ave) 
    fpr_std=np.std(fprs)
    print('fpr_std',fpr_std)
    #get the standard devition of cross_validation
    recalls=cross_val_score(model,test_x_chi2,test_y,scoring='recall',cv=10)
    #print('recalls',recalls)
    recall=np.mean(recalls)
    print('recall:',recall) 
    re_std=np.std(recalls)
    print('re_std',re_std)
    print('training time:',time1)
    return model,fpr_ave,fpr_std,recall,re_std,time1,chi2_selector



def get_base_rf_fpr(model,test_x,test_y,selector):
    se_test_x=selector.transform(test_x)
    #print('se_test_x.shape',se_test_x.shape)#25
    pre_y=model.predict(se_test_x)
    #print('pre_y:',pre_y)
    error_sam=[]#get misclassified sample
    cm=confusion_matrix(test_y,pre_y)
    try:
        fp=cm[0,1]
        tn=cm[0,0]
        #tp=cm[1,1]
        #fn=cm[1,0]
        fpr=fp/(fp+tn)
        #recall=tp/(tp+fn)
        print('fpr',format(fpr,'.3f'))
        return fpr
    except:
        #print('pre_class:',pre_class)
        #print('test_y',test_y)
        if operator.eq(test_y.all(),pre_y.all()):
            print('fpr',0)
            return 0
        else:
            print('fpr',1)
            return 1
def get_base_sub_rf_recall(model,test_x,test_y,selector,phish_sub_test_x):
    se_test_x=selector.transform(test_x)
    #print('se_test_x.shape',se_test_x.shape)#25
    pre_y=model.predict(se_test_x)
    cm=confusion_matrix(test_y,pre_y)
    error_sam=[]
    for ind, prediction, label in zip (phish_sub_test_x.index, pre_y, test_y):
        if prediction!=label:
            error_sam.append(ind)
            #print(ind, 'has been classified as ', prediction, 'and should be ', label)
   # print('misclassified samples are:',error_sam)
    try:
        tp=cm[1,1]
        fn=cm[1,0]
        recall=tp/(tp+fn)
        '''
        print('tp',tp)
        print('fn',fn)
        print('cm',cm)'''
        print('recall',format(recall,'.2f'))
        return recall,error_sam
    except:
        print('test_y',test_y)
        print('pre_y',pre_y)
        if operator.eq(test_y.all(),pre_y.all()):
            return 1,error_sam
        else:
            return 0,error_sam
def get_base_sub_recall_cnn(model,test_x,test_y,phish_sub_test_x):
    predict_y=model.predict(test_x)
    pre_class=np.argmax(predict_y,axis=1)
    cm= confusion_matrix(test_y, pre_class)
    error_sam=[]
    for ind, prediction, label in zip (phish_sub_test_x.index, pre_class, test_y): 
        if prediction!=label:
            error_sam.append(ind)
            #print(ind, 'has been classified as ', prediction, 'and should be ', label)
    #print('misclassified samples are:',error_sam)
    
    try:
        tp=cm[1,1]
        fn=cm[1,0]
        cnn_recall=tp/(tp+fn)
        print('tp',tp)
        print('fn',fn)
        print('cm',cm)
        print('cnn_recall',cnn_recall)
        return cnn_recall,error_sam
    except:
        print('test_y',test_y)
        print('pre_class',pre_class)
        #operator.eq(a,b)
        
        if operator.eq(test_y.all(),pre_class.all()):
            print('recall',1)
            return 1,error_sam
        else:
            print('recall',0)
            return 0,error_sam
        
def get_base_recall_cnn(model,test_x,test_y):
    predict_y=model.predict(test_x)
    pre_class=np.argmax(predict_y,axis=1)
    cm= confusion_matrix(test_y, pre_class)
    
    try:
        tp=cm[1,1]
        fn=cm[1,0]
        cnn_recall=tp/(tp+fn)
        print('cnn_recall',format(cnn_recall,'.2f'))
        return cnn_recall
    except:
        #print('test_y',test_y)
        #print('pre_class',pre_class)
        if operator.eq(test_y.all(),pre_class.all()):
            print('recall',1)
            return 1
        else:
            print('recall',0)
            return 0
        
def get_base_fpr_cnn(model,test_x,test_y):
    predict_y=model.predict(test_x)
    pre_class=np.argmax(predict_y,axis=1)
    cm= confusion_matrix(test_y, pre_class)
    error_sam=[]
    try:
        fp=cm[0, 1]
        tn=cm[0, 0]
        cnn_fpr=fp/(fp+tn)
        print('fpr',format(cnn_fpr,'.3f'))
        return cnn_fpr
    except:
        print('pre_class:',pre_class)
        print('test_y',test_y)
        if operator.eq(test_y.all(),pre_class.all()):
            print('fpr',0)
            return 0
        else:
            print('fpr',1)
            return 1


def data_load(json_file):
    json_data=open(json_file).read()
    f=json.loads(json_data)
    data=pd.json_normalize(f)#dataframe
    data_ze=data.iloc[:,:60]#include 'label', 'index', 
    data_ze=data_ze.astype(float)
    return data_ze
def confusion_matrix_scorer(clf, X, y):
    y_pred = clf.predict(X)
    cm = confusion_matrix(y, y_pred)
    tn=cm[0, 0]
    fp=cm[0, 1]
    fn=cm[1, 0]
    tp=cm[1, 1]
    fpr=fp/(fp+tn)
    return fpr
def get_sub_base_rf_recall(model,test_x,test_y,selector):
    se_test_x=selector.transform(test_x)
    pre_y=model.predict(se_test_x)
    cm=confusion_matrix(test_y,pre_y)
    try:
        tp=cm[1,1]
        fn=cm[1,0]
        recall=tp/(tp+fn)
        print('recall',format(recall,'.2f'))
        #print('cm',cm)
        return recall
    except:
        #print('test_y',test_y)1
        #print('pre_y',pre_y)1
        if operator.eq(test_y.all(),pre_y.all()):
            print('recall',1)
            return 1
        else:
            print('recall',0)
            return 0  
