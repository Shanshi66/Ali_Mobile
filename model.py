from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
from sklearn.externals import joblib
import csv
from utility import cutoffLine, timekeeper, doneCount, dropItemsNotInSet, loadItemSubset
import time
import numpy as np
import evaluate
import sys
import os


def LR(X, y):
    cutoffLine('-')
    print 'Training...'
    X = preprocessing.scale(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
    c_set = [0.01, 0.5, 0.1] + map(lambda x: x/100.0, range(50,1001,50))
    # c_set = [1]
    min_error = 100000
    best_model = 1
    best_c = -1
    for c in c_set:
        LR_model = LogisticRegression(C=c, penalty = 'l1', tol = 0.001, max_iter = 20000)
        LR_model.fit(X, y)
        y_pred = LR_model.predict(X_test)
        error = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
        if error < min_error:
            min_error = error
            best_model = LR_model
            best_c = c
    print "best C is %f, error is %f" % (best_c, min_error)
    print 'coefs below:'
    print best_model.coef_[0]
    return best_model

def SVM(X, y):
    cutoffLine('-')
    print 'Training...'
    X = preprocessing.scale(X)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)
    SVM_model = SVC()
    SVM_model.fit(X, y)
    return SVM_model

def RF(X, y):
    cutoffLine('-')
    print 'Training...'
    model = RandomForestClassifier(n_estimators = 100)
    model.fit(X, y)
    return model

def train(window, proportion, algo, confidence):
    start_time = time.time()
    cutoffLine('*')
    print '%s model training with sample proportion 1:%d...' %(algo, proportion)
    t_file = file('data/training_set_%d_%d.csv' % (window, proportion), 'r')
    t_reader = csv.reader(t_file)
    X = []
    y = []
    for line in t_reader:
        doneCount(t_reader.line_num)
        line = map(int, line)
        X.append(line[3:-1])
        y.append(line[-1])

    model_name = 'data/model/%s_%d_%d.model'%(algo, window, proportion)
    if os.path.exists(model_name): model = joblib.load(model_name)
    else:
        if algo == 'lr': model = LR(X, y)
        if algo == 'rf': model = RF(X, y)
        if algo == 'svm': model = SVM(X, y)
        joblib.dump(model, model_name)
    cutoffLine('-')
    print model.classes_
    item_subset = loadItemSubset()

    record_file = open('data/model_evaluate_record.txt','a')
    P, R, F= evaluate_model(algo, window, model, item_subset, confidence)
    predict_set_size = predict(window, model, item_subset, proportion, algo, confidence)
    record_file.write('window %d '%window + algo+' %d'%proportion + ' %.2f\n'%confidence)
    record_file.write('\tP: %f\n'%P)
    record_file.write('\tR: %f\n'%R)
    record_file.write('\tF1: %f\n'%F)
    record_file.write('Predict Set Size: %d\n'%predict_set_size)
    record_file.write('-'*30+'\n')
    record_file.close()



    t_file.close()
    cutoffLine('*')
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print 'I takes %s to train , evaluate model and generate result' % duration

def evaluate_model(algo, window, model, item_subset, confidence):
    cutoffLine('-')
    print 'offline evaluate model with confidence %f' % confidence
    test_file = file('splited_data_%d/set_test.csv'%window, 'r')
    test_reader = csv.reader(test_file)
    predict_set = set()
    real_set = set()
    UI = []
    X = []
    each_time = 500000
    for line in test_reader:
        doneCount(test_reader.line_num)
        line = map(int, line)
        UI.append(tuple(line[0:2]))
        X.append(line[3:-1])
        if line[-1] == 1 : real_set.add((line[0],line[1]))
        if test_reader.line_num % each_time == 0:
            if algo == 'lr' or algo == 'svm': X = preprocessing.scale(X)
            if algo == 'lr' or algo == 'rf':
                y_pred = model.predict_proba(X)
                for index, y in enumerate(y_pred):
                    if y[1] > confidence: predict_set.add(UI[index])
            if algo == 'svm':
                y_pred = model.predict(X)
                for index, y in enumerate(y_pred):
                    if y == 1: predict_set.add(UI[index])
            UI = []
            X = []
    if len(UI) > 0:
        if algo == 'lr' or algo == 'svm': X = preprocessing.scale(X)
        if algo == 'lr' or algo == 'rf':
            y_pred = model.predict_proba(X)
            for index, y in enumerate(y_pred):
                if y[1] > confidence: predict_set.add(UI[index])
        if algo == 'svm':
            y_pred = model.predict(X)
            for index, y in enumerate(y_pred):
                if y == 1: predict_set.add(UI[index])
        UI = []
        X = []

    predict_set = dropItemsNotInSet(predict_set, item_subset)
    real_set = dropItemsNotInSet(real_set, item_subset)
    import evaluate
    P, R, F = evaluate.evaluate(predict_set, real_set)
    test_file.close()
    return P, R, F

def predict(window, model, item_subset, proportion, algo, confidence):
    cutoffLine('-')
    print 'Generate result set with confidence %f' % confidence
    feature_file = file('splited_data_%d/set_for_prediction.csv'%window, 'r')
    result_file = file('data/tianchi_mobile_recommendation_predict_%d_%s_%d_%s.csv'%\
                                        (window, algo, proportion, str(confidence)), 'w')
    f_reader = csv.reader(feature_file)
    r_writer = csv.writer(result_file)
    r_writer.writerow(['user_id','item_id'])
    predict_set = set()
    UI = []
    X = []
    each_time = 500000
    for line in f_reader:
        doneCount(f_reader.line_num)
        line = map(int, line)
        UI.append(tuple(line[0:2]))
        X.append(line[3:])
        if f_reader.line_num % each_time == 0:
            if algo == 'lr' or algo == 'svm': X = preprocessing.scale(X)
            if algo == 'lr' or algo == 'rf':
                y_pred = model.predict_proba(X)
                print y_pred
                for index, y in enumerate(y_pred):
                    if y[1] > confidence: predict_set.add(UI[index])
            if algo == 'svm':
                y_pred = model.predict(X)
                for index, y in enumerate(y_pred):
                    if y == 1: predict_set.add(UI[index])
            UI = []
            X = []
    if len(UI) > 0:
        if algo == 'lr' or algo == 'svm': X = preprocessing.scale(X)
        if algo == 'lr' or algo == 'rf':
            y_pred = model.predict_proba(X)
            for index, y in enumerate(y_pred):
                if y[1] > confidence: predict_set.add(UI[index])
        if algo == 'svm':
            y_pred = model.predict(X)
            for index, y in enumerate(y_pred):
                if y == 1: predict_set.add(UI[index])
        UI = []
        X = []

    cutoffLine('-')
    print "Prediction set size before drop: %d" % len(predict_set)
    predict_set = dropItemsNotInSet(predict_set, item_subset)
    r_writer.writerows(predict_set)
    print "Prediction set size after drop: %d" % len(predict_set)

    feature_file.close()
    result_file.close()

    return len(predict_set)

if __name__ == '__main__':
    if len(sys.argv) < 4: print 'Need window, algorithm, propotion and confidence'
    else:
        window =  int(sys.argv[1])
        algo = sys.argv[2]
        propotion = int(sys.argv[3])
        confidence = float(sys.argv[4])
        print "Window %d" % window
        train(window, propotion, algo, confidence)
