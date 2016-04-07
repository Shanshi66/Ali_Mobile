from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import csv
from utility import cutoffLine, timekeeper, doneCount, dropItemsNotInSet, loadItemSubset
import time
import numpy as np
import evaluate

TRAIN_SET_DIR = 'training_set'
TRAIN_SET_FILES = 135

def logRes(X, y):
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

def train_LR():
    start_time = time.time()
    cutoffLine('*')
    print 'LR model training...'
    cutoffLine('-')
    t_file = file('data/training_set_10.csv', 'r')
    t_reader = csv.reader(t_file)
    X = []
    y = []
    for line in t_reader:
        line = map(int, line)
        X.append(line[2:-1])
        y.append(line[-1])
    model = logRes(X,y)
    item_subset = loadItemSubset()
    evaluate_model(model, item_subset)
    predict(model, item_subset)
    t_file.close()

    cutoffLine('*')
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print 'I takes %s to train , evaluate model and generate result' % duration

def evaluate_model(model, item_subset):
    cutoffLine('-')
    print 'offline evaluate LR model'
    test_file = file('splited_data/set_test.csv', 'r')
    test_reader = csv.reader(test_file)
    predict_set = set()
    real_set = set()
    for line in test_reader:
        doneCount(test_reader.line_num)
        line = map(int, line)
        if line[-1] == 1 : real_set.add((line[0],line[1]))
        if model.predict([line[2:-1]])[0] == 1: predict_set.add((line[0],line[1]))

    predict_set = dropItemsNotInSet(predict_set, item_subset)
    real_set = dropItemsNotInSet(real_set, item_subset)

    import evaluate
    P, R, F = evaluate.evaluate(predict_set, real_set)
    test_file.close()
    return P, R, F

def predict(model, item_subset):
    cutoffLine('-')
    print 'Generate result set'
    feature_file = file('splited_data/set_for_prediction.csv', 'r')
    result_file = file('data/prediction_lr.csv', 'w')
    f_reader = csv.reader(feature_file)
    r_writer = csv.writer(result_file)
    r_writer.writerow(['user_id','item_id'])
    predict_set = set()
    for line in f_reader:
        doneCount(f_reader.line_num)
        line = map(int, line)
        if model.predict([line[2:]])[0] == 1: predict_set.add((line[0], line[1]))

    cutoffLine('-')
    print "Prediction set size before drop: %d" % len(predict_set)
    predict_set = dropItemsNotInSet(predict_set, item_subset)
    r_writer.writerows(predict_set)
    print "Prediction set size after drop: %d" % len(predict_set)

    feature_file.close()
    result_file.close()

if __name__ == '__main__':
    train_LR()
