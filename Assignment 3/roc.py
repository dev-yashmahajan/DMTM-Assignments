import sys
import math
import csv
import matplotlib.pyplot as plt

classification_accuracy = 0
precision = 0
recall = 0
F1score = 0
tpr_main = 0
fpr_main = 0
sensitivity = 0
specificity = 0
auc = 0


def write_output():
    original_stdout = sys.stdout
    with open('output.txt', 'w') as f:
        sys.stdout = f
        print('(')
        print('(Accuracy %f' %classification_accuracy + ')')
        print('(Precision %f' %precision + ')')
        print('(Recall %f' %recall + ')')
        print('(F1 %f' %F1score + ')')
        print('(TPR %f' %tpr_main + ')')
        print('(FPR %f' %fpr_main + ')')
        print('(Specificity %f' %specificity + ')')
        print('(Sensitivity %f' %sensitivity + ')')
        print('(AUC %f' %auc + ')')
        print(')')
    sys.stdout = original_stdout
    
def print_output():
    f = open("output.txt")
    lines = f.readlines()
    for line in lines:
        print(line.strip())

def main():
    
    global classification_accuracy
    global precision
    global recall 
    global F1score 
    global tpr_main
    global fpr_main
    global sensitivity 
    global specificity 
    global auc
    
    prob = []
    true_class = []
    with open(sys.argv[1], mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            prob.append(float(row[1].strip()))
            true_class.append(int(row[-1].strip()))    
    

    n = len(true_class)
    predicted_class = []
    for p in prob:
        if p > 0.5:
            predicted_class.append(1)
        else:
            predicted_class.append(0)
            
    #Classification accuracy
    classification_accuracy = 0
    for i in range(n):
        if true_class[i] == predicted_class[i]:
            classification_accuracy += 1
    
    classification_accuracy = classification_accuracy / n
  
    #Confusion matrix
    TP = 0
    FN = 0
    FP = 0
    TN = 0
    
    for i in range(n):
        if true_class[i] == 1 and predicted_class[i] == 1:
            TP += 1
        elif true_class[i] == 1 and predicted_class[i] == 0:
            FN += 1
        elif true_class[i] == 0 and predicted_class[i] == 1:
            FP += 1   
        elif true_class[i] == 0 and predicted_class[i] == 0:
            TN += 1


    #Precision, recall, F-1 score
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    F1score = (2 * precision * recall ) / (precision + recall)

    #True positive rate
    tpr_main = recall
    fpr_main = FP / (TN + FP)
    sensitivity = tpr_main
    specificity = 1 - fpr_main
     
    
    
    #ROC Curve
    scoring = sorted(zip(prob, true_class), reverse = True)
    # print(scoring)
    
    
    tp_list = []
    fp_list = []
    tn_list = []
    fn_list = []
    tpr_list = []
    fpr_list = []
    for i in range(n + 1):
        pos_classes = scoring[0 : i]
        neg_classes = scoring[i:]
        
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        tpr = 0
        fpr = 0
        
        for p , c in pos_classes:
            if c == 1:
                tp += 1
            else:
                fp += 1
        for n , c in neg_classes:
            if c == 0:
                tn += 1
            else:
                fn += 1
        
        if (tp + fn) == 0:
            tpr = 0
        else:
            tpr = tp / (tp + fn)
            
        if (tn + fp) == 0:
            fpr = 0
        else:
            fpr = fp / (tn + fp)
        
        tp_list.append(tp)
        fn_list.append(fn)
        tn_list.append(tn)
        fp_list.append(fp)
        tpr_list.append(tpr)
        fpr_list.append(fpr)
        
    print(tpr_list)    
        
    
    plt.figure()
    plt.plot(fpr_list, tpr_list)
    plt.plot([0,1] , [0,1], 'r--')
    plt.xlim([0.0,1.0])
    plt.ylim([0.0,1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.show()
    
    
    
    
    auc = 0
    for i in range(1, len(fpr_list)):
        h = fpr_list[i] - fpr_list[i-1]
        auc += h * (tpr_list[i-1] + tpr_list[i]) / 2
        
    write_output()
    print_output()
    
if __name__ == "__main__":
	main()
