from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import csv
from utility import cutoffLine, timekeeper, doneCount
import time
import numpy as np
import evaluate

TRAIN_SET_DIR = 'training_set'
TRAIN_SET_FILES = 135

def RF(X, y):
    model = RandomForestClassifier(n_estimators = 200)
    model.fit(X,y)
    return model

def train_RF():
    start_time = time.time()
    cutoffLine('*')
    print 'Use RF model to train %d models'%TRAIN_SET_FILES
    for i in range(1, 1 + 1):
    #for i in range(1, TRAIN_SET_FILES + 1):
        cutoffLine('-')
        print 'model %d'%i
        t_file = file(TRAIN_SET_DIR + '/%d.csv'%i, 'r')
        t_reader = csv.reader(t_file)
        X = []
        y = []
        for line in t_reader:
            line = map(int, line)
            X.append(line[2:-1])
            y.append(line[-1])
        model = RF(X, y)
        P ,R ,F = evaluate_model(model, i)
        predict(model, i)
        models.append(model)
        t_file.close()

    cutoffLine('*')
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print 'I takes %s to train , evaluate model and generate result'% duration

def LR_model_record(writer, coef, c, error, P, R, F):
    writer.writerow(coef)
    writer.writerow(['c',c])
    writer.writerow(['error', error])
    writer.writerow(['P', P])
    writer.writerow(['R', R])
    writer.writerow(['F', F])

def evaluate_model(model, index):
    cutoffLine('-')
    print 'offline evaluate RF model %d' % index
    test_file = file('splited_data/set_test.csv', 'r')
    test_reader = csv.reader(test_file)
    predict_set = set()
    real_set = set()
    for line in test_reader:
        doneCount(test_file.line_num)
        line = map(int, line)
        if line[-1] == 1 : real_set.add((line[0],line[1]))
        if model.predict([line[2:-1]])[0] == 1: predict_set.add((line[0],line[1]))
    import evaluate
    P, R, F = evaluate.evaluate(predict_set, real_set)
    test_file.close()
    return P, R, F

def predict(model, index):
    cutoffLine('-')
    print 'Generate result set %d' % index
    feature_file = file('splited_data/set_for_prediction.csv', 'r')
    result_file = file(TRAIN_SET_DIR + '/' + 'lr_result_%d.csv' % index, 'w')
    f_reader = csv.reader(feature_file)
    r_writer = csv.writer(result_file)
    r_writer.writerow(['user_id','item_id'])
    for line in f_reader:
        doneCount(f_reader.line_num)
        line = map(int, line)
        if model.predict([line[2:]])[0] == 1: r_writer.writerow(line[0:2])

    feature_file.close()
    result_file.close()

if __name__ == '__main__':
    train_RF()
