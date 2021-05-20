import sys
import operator

txn_data = [] #input data
mis_data = {} #mis data

#function to read transaction file
def read_txn():
    with open(sys.argv[1], mode='r') as file:
        for line in file:
            l = line.rstrip().split(", ")
            txn_data.append(l)
            
    for l1 in txn_data:
        for l2 in l1:
            if l2 not in mis_data.keys():
                mis_data[l2] = 0.0
                
    
#function to read parameter file
def read_mis():
    with open(sys.argv[2]) as file:
        for line in file:
            line = line.rstrip()
            if "=" in line:
                key, value = line.split("=")
                if key[0:3] == 'MIS':
                    key = key[4:-2]
                    if key == 'rest':
                        for k,v in mis_data.items():
                            if v == 0.0:
                                mis_data[k] = float(value)
                    else:
                        mis_data[key] = float(value)
                
                if key[0:3] == 'SDC':
                    mis_data[key.rstrip()] = float(value)
                    
    
def item_count(item):
    count = 0
    for txn in txn_data:
        if item in txn:
            count = count + 1
    
    return count        


def write_output(F):
    original_stdout = sys.stdout
    with open('output.txt', 'w') as f:
        sys.stdout = f
        F = F[1:]
        for f in F:
            n = F.index(f) + 1
            print('(Length-%d %d ' % (n, len(f)))
            
            for i in f:
                i_output = '(' + str(i).strip('[]').replace(',', '').replace("\'", '') + ')'
                print('\t%s' %  i_output)
                
            print(')')
        
    sys.stdout = original_stdout
    
    
def print_output():
    f = open("output.txt")
    lines = f.readlines()
    for line in lines:
        print(line.rstrip())
        
#initial pass through the data 
def init_pass(M):
    L = []
    n = len(txn_data)
    index = 0
    for i in M:
        index = index + 1
        if item_count(i[0]) >= (n * mis_data[i[0]]):
            L.append(i[0])
            
            rem_items = M[index: len(M)]
            for j in rem_items:
                if item_count(j[0]) >= (n * mis_data[L[0]]):
                    L.append(j[0])
        
            return L
    
    
#sort the mis data and remove data which is never used
def sort_items():
    
    a = mis_data.copy()
    for m in mis_data.keys():
        if item_count(m) == 0:
            del a[m]
    
    sorted_mis = sorted(a.items(), key=operator.itemgetter(1))

    # print(sorted_mis)
    return sorted_mis

#generate level 2 candidates
def level2_candidate_gen(L, sdc):
    C2 = []
    n = len(txn_data)
    index = 0    
    
    for l in L:
                
        index = index + 1
        if item_count(l) >= (n * mis_data[l]):
            rem_items = L[index: len(L)]
            for j in rem_items:
                if item_count(j) >= (mis_data[l] * n) and abs(item_count(j) - item_count(l)) <= (n * sdc):
                    c = []
                    c = [l,j]
                    C2.append(c)
    
    # print(C2)
    return C2


def MScandidate_gen(F,sdc):
    C = []
    n = len(txn_data)
    
    for f1 in F:
        for f2 in F:
            if f1[0:-1] == f2[0:-1] and f1[-1] < f2[-1] and abs(item_count(f1[-1]) - item_count(f2[-1])) <= (n * sdc):
                
                c = []
                c = f1[:]
                c.append(f2[-1])
                C.append(c)
                
    for k in C:
        index = C.index(k)
        subsets = []
        
        for i in k:
            subset = []
            index1 = k.index(i)
            subset = k[:index1] + k[index1 + 1:]
            subsets.append(subset)
            
        for subset in subsets:
            if k[0] in subset or mis_data[k[0]] == mis_data[k[1]]:
                if subset not in F:
                    del C[index]
                    break
                
                
    return C

def msapriori():
    n = len(txn_data)
    sdc = 0
    if 'SDC' in mis_data.keys():
        sdc = mis_data['SDC']
    
    # print(mis_data    )
    C = []
    F = []
    
    c_count = {}
    M = sort_items() #sort mis values
    # print(M)
    L = init_pass(M) 
    # print(L)
    F.append(L)
    #calculate f1
    F1 = []
    for l in L:
        if item_count(l) >= (n * mis_data[l]):
            F1.append(l)
    F.append(F1)
    # print(F1)
    
    k = 2
    while len(F[k-1]) != 0:
        
        if k == 2:
                C2 = level2_candidate_gen(L, sdc)
                C.append(C2)
        else:
                Ck = MScandidate_gen(F[k-1],sdc)
                C.append(Ck)
            
        
        Fk = []
        for t in txn_data:
            for c in C[-1]:
                if set(c).issubset(set(t)):
                    c_count[tuple(c)] = c_count.get(tuple(c), 0) + 1
                
                
        for c in C[k-2]:
            if tuple(c) in c_count.keys() and (c_count[tuple(c)] / n) >= mis_data[c[0]]:
                Fk.append(c)
                
        k = k+1 
        F.append(Fk)
    
    
    F = F[:-1]
    write_output(F)
    print_output()
    
def main():
    read_txn()
    read_mis()
    msapriori()
    
    
if __name__ == "__main__":
	main()
