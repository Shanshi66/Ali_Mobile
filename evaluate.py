#coding = utf-8

"""
    @Author : Rosen
    offline evaluate
"""

def evaluate(prediction,result):
    prediction = set(prediction)
    result = set(result)

    intersection = prediction & result

    precision = float(len(intersection))/len(prediction)
    recall = float(len(intersection))/len(result)

    F1 = 2 * precision * recall / (precision + recall)

    print 'P : %f' % precision
    print 'R : %f' % recall
    print 'F1: %f' % F1
