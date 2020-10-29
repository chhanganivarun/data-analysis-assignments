import csv
import time


def ini(dataset,support):
    c = [0 for i in range(70000)]
    new = []
    for i in dataset:
        for j in i:
            c[j-1] += 1
    lc=len(c)
    for j in range(lc):
        if c[j] >= support:
            new.append([j+1])
    return new

def ins(a,b):
    flag=1
    for i in a:
        if i not in b:
            flag=0
            return flag
    
    return flag


def join(old):
    new = []
    final=[]
    ol=len(old)
    for i in range(ol):
        for j in range(i+1, ol):
            if old[i][:-1] == old[j][:-1]:
                if old[j][-1] != old[i][-1]:
                    diff=old[i][-1]-old[j][-1]
                    temp = old[i][:-1]
                    if diff>0:
                        temp.append(old[j][-1])
                        temp.append(old[i][-1])
                    else:
                        temp.append(old[i][-1])
                        temp.append(old[j][-1])
                    if temp not in new:
                        new.append(temp)  
    
    for i in new:
        flag=1
        for j in i:
            temp=(i.copy())
            temp.remove(j)
            if temp not in old:
                flag*=0
                break
        if flag == 1:
            final.append(i)
    return final


def prune(dataset,old,support):
    count = [0 for i in range(len(old))]
    c=0
    new = []
    lo=len(old)
    for i in dataset:
        c+=1
        for j in range(lo):
            if ins(old[j],i):
                count[j] += 1

    for j in range(lo):
        if support <= count[j] :
            new.append(old[j])

    return new


def opt2(dataset,isValid,old,support):
    new = []
    count = [0 for i in range(len(old))]
    lo=len(old)
    for i in range(len(dataset)):
        if isValid[i] == 0:
            continue
        fl = 0
        for j in range(lo):
            if ins(old[j],dataset[i]):
                fl = 1
                count[j] += 1
        isValid[i] = fl

    for j in range(lo):
        if support <= count[j]:
            new.append(old[j])

    return new,isValid

def opt3ini(dataset,has,k,support):
    new = []
    count = [0 for i in range(70000)]
    for i in dataset:
        li=len(i)
        for j in range(li):
            count[i[j]-1] += 1
            for k in range(j+1, li):
                if (i[j],i[k]) in has:
                    has[(i[j],i[k])] += 1
                else:
                    has[(i[j],i[k])] = 1

    for j in range(70000):
        if count[j] >= support:
            new.append([j+1])

    return new,has

def pruneFromHash(has,old,support):
    new=[]
    for i in old:
        # if has[(i[0],i[1])] >= support:
        if support <= has[(i[0],i[1])] :
            new.append(i)
    
    return new


def run_original(dataset,support,k):
    ans=[]
    al = ini(dataset,support) #Initialisation 

    for i in range(k): 
        if len(al) == 0:
            break
        for i in al:
            ans.append(i)
        al = join(al)
        al = prune(dataset,al,support)
    
    return len(ans)



def run_reduction(dataset,support,k):
    ans=[]
    al = ini(dataset,support)                                                      
    isValid = [1 for i in range(len(dataset))]

    for i in range(k):                                                
        if al == []:
            break
        for i in al:
            ans.append(i)
        al = join(al)
        al,isValid = opt2(dataset,isValid,al,support)

    return len(ans)




def run_hash(dataset,support,k):
    has = dict()
    ans=[]
    al,has = opt3ini(dataset,has,k,support)                                                    
    for i in range(k):                                                
        if len(al) == 0:
            break
        for i in al:
            ans.append(i)
        al = join(al)
        if k!=2:
            al = prune(dataset,al,support)
        else:
            al = pruneFromHash(has,al,support)

    return len(ans)


def read_file(filename):
    dataset = []

    f=open(filename, 'r')
    reader = csv.reader(f)
    for row in reader:
        new=sorted([int(i) for i in row[0].split('-1')[:-1]])
        dataset.append(new)
    return dataset

def main():
    dataset=read_file('SIGN.txt')
    support = 400
    k = 10
    print('run_original')
    start = time.time()
    print(run_original(dataset,support,k))
    end = time.time()
    print(end - start)
    print('run_reduction')
    start = time.time()
    print(run_reduction(dataset,support,k))
    end = time.time()
    print(end - start)
    print('run_hash')
    start = time.time()
    print(run_hash(dataset,support,k))
    end = time.time()
    print(end - start)




if __name__=="__main__":
    main()