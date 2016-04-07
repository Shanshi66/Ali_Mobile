#coding = utf-8

"""
    @Author : Rosen
    offline evaluate
"""

def evaluate(prediction,result):
    prediction = set(prediction)
    result = set(result)

    intersection = prediction & result

    precision = float(len(intersection))/len(prediction)*100
    recall = float(len(intersection))/len(result)*100

    F1 = 2 * precision * recall / (precision + recall)

    print 'P : %2f' % precision
    print 'R : %2f' % recall
    print 'F1: %2f' % F1
    return precision, recall, F1
