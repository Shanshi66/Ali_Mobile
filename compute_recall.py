import sys

def computeRecall(P, F1):
    R = F1*P/(2*P-F1)
    print "P: %f"%P
    print "R: %f"%R
    print "F1: %f"%F1

if __name__ == '__main__':
    if len(sys.argv) != 3: print "Need two parameters"
    else:
        P = float(sys.argv[1])
        F1 = float(sys.argv[2])
        computeRecall(P, F1)
