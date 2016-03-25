#coding = utf-8
"""
    @Author : Rosen
    use rules to do the prediction
"""

import csv
import sys

#rule1:cart buy
def cartBuy():
    user_file = file('data/nuser.csv','r')
    reader = csv.reader(user_file)

    cart_30 = set()
    buy_31 = set()
    cart_31 = set()

    for line in reader:
        if reader.line_num % 100000 ==0:
            sys.stdout.write('\r'+str(reader.line_num))
            sys.stdout.flush()
        if int(line[5]) == 30 and int(line[6]) > 8:
            if int(line[2]) == 3:cart_30.add((line[0],line[1]))
            if int(line[2]) == 4:
                if (line[0],line[1]) in cart_30:cart_30.remove((line[0],line[1]))
        if int(line[5]) == 31 and int(line[6]) > 8:
            if int(line[2]) == 3:cart_31.add((line[0],line[1]))
            if int(line[2]) == 4:
                if (line[0],line[1]) in cart_31:cart_31.remove((line[0],line[1]))
        if int(line[5]) == 31 and int(line[2]) == 4:
            buy_31.add((line[0],line[1]))
    user_file.close()
    return cart_30 , buy_31 , cart_31

if __name__ == '__main__':
    print '-----------------------------------'
    print 'Use cart buy rule'
    test_predict , test_result , prediction = cartBuy()

    print 'Test Predict Set Size: %d' % len(test_predict)
    print 'Test Result Set Size: %d' % len(test_result)
    print 'Prediction Set Size: %d' % len(prediction)

    import evaluate
    evaluate.evaluate(test_predict,test_result)

    pred_file = file('data/tianchi_mobile_recommendation_predict.csv','w')
    writer = csv.writer(pred_file)

    writer.writerow(['user_id','item_id'])
    for ui in prediction:writer.writerow(ui)

    pred_file.close()
