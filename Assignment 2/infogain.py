import sys
import math
import csv
   

def main():
    
    attr = []
    class_col = []
    with open(sys.argv[1], mode='r') as csv_file:
        # csv_file = open(sys.argv[1], mode='r')
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        attr_no = int(sys.argv[2]) - 1
        for row in csv_reader:
            attr.append(row[attr_no])
            class_col.append(row[-1])
                
    # csv_file.close()
    n = len(attr)
    
    class_dict = {}
    for c in class_col:
        class_dict[c] = class_dict.get(c, 0) + 1
    # print(class_dict)
    
    entropy = 0
    for c,v in class_dict.items():
        entropy = entropy - (v/n) * math.log(v/n, 2)
        
    attr_dict = {}
    for a in attr:
        attr_dict[a] = attr_dict.get(a, 0) + 1
    # print(attr_dict)
    
    info_gain = entropy
    # print(entropy)
    

    count = {}
    for key in class_dict:
        count[key] = 0
    
    
    for a,an in attr_dict.items():
        count = count.fromkeys(count, 0)
        for i, val in enumerate(attr):
            if a == val:
                count[class_col[i]] = count[class_col[i]] + 1
            
        
        temp = 0
        for k,v in count.items():
            if (v/an) != 0:
                temp = temp + (v/an) * math.log(v/an,2)
                
        info_gain = info_gain - (an/n) * -1 * (temp)
    
    print("(IG %f)" %info_gain)
    
    f = open('output.txt', 'w')
    output = "(IG " + str(info_gain) + ")"
    f.write(output)
    f.close()
    
    
if __name__ == "__main__":
	main()