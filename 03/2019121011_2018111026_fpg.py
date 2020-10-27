#!/usr/bin/env python
# config utf-8

# In[]:
import numpy as np
# In[]:
with open('BMS1.txt', 'r') as fi:
    dataset = fi.readlines()
dataset = ''.join(dataset)
dataset = dataset.replace('\n', ' ')
dataset = dataset.replace('\r', ' ')
dataset = dataset.split('-2')

for idx, val in enumerate(dataset):
    dataset[idx] = [int(x) for x in val.split('-1') if x.strip() != '']

# In[]:


class node:
    def __init__(self, item, count=1, parent=None, link=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.link = link
        self.children = dict()

    def visittree(self):
        output = []
        output.append(str(self.item) + " " + str(self.count))
        if len(list(self.children.keys())) > 0:
            for i in (list(self.children.keys())):
                output.append(self.children[i].visittree())
        return output

# In[]:


class fp_tree:
    def __init__(self, dataset, support):
        self.root = node(-1, 0)

        self.sorted_dataset = []
        self.dataset = dataset

        self.items = {}
        self.header_table = []

        self.item_rank = {}
        self.keys_k1 = []

        self.support = support

        self.get_item_supports()

        self.prune_item()

        self.make_header()

        self.sort_dataset()

        self.make_tree()

    def get_item_supports(self):
        for transaction in self.dataset:
            for item in transaction:
                if item in self.items.keys():
                    self.items[item] += 1
                else:
                    self.items[item] = 1

    def prune_item(self):
        for item in list(self.items.keys()):
            if self.items[item] < self.support:
                del self.items[item]

    def make_header(self):
        self.header_table = sorted(
            list(self.items.items()), key=lambda x: (x[1], x[0]), reverse=True)
        for idx, val in enumerate(self.header_table):
            self.item_rank[val[0]] = idx
            self.header_table[idx] = {'item': val[0],
                                      'count': self.items[val[0]], 'link': None}

    def sort_dataset(self):
        for transaction in self.dataset:
            updated_transaction = []
            for item in transaction:
                if item in self.items.keys():
                    updated_transaction.append(item)
            if len(updated_transaction) <= 0:
                continue
            updated_transaction = sorted(
                updated_transaction, key=lambda x: self.item_rank[x])
            self.sorted_dataset.append(updated_transaction)

    def make_tree(self):
        for transaction in self.sorted_dataset:
            current = self.root
            for item in transaction:
                if item not in current.children.keys():
                    current.children[item] = node(item, 1, current, None)
                    current = current.children[item]
                    for item_in in self.header_table:
                        if item_in['item'] == current.item:
                            if item_in['link'] is not None:
                                iter_in = item_in['link']
                                while iter_in.link is not None:
                                    iter_in = iter_in.link
                                iter_in.link = current
                            else:
                                item_in['link'] = current
                else:
                    current.children[item].count += 1
                    current = current.children[item]

    def condtreetran(self, N):
        if N is None:
            return [[]]
        if N.parent is None:
            return None

        condtreeline = []
        # starting from the leaf node reverse add word till hit root
        while N is not None:
            line = []
            PN = N.parent
            while PN.parent is not None:
                line.append(PN.item)
                PN = PN.parent
            line = line[::-1]
            for i in range(N.count):
                condtreeline.append(line)
            N = N.link
        return condtreeline

    def findfqt(self, parentnode=None):
        if len(list(self.root.children.keys())) == 0:
            return None
        result = []
        sup = self.support
        # starting from the end of nodetable
        revtable = self.header_table[::-1]
        for n in revtable:
            fqset = [set(), 0]
            if(parentnode == None):
                fqset[0] = {n['item'], }
            else:
                fqset[0] = {n['item']}.union(parentnode[0])
            fqset[1] = n['count']
            result.append(fqset)
            condtran = self.condtreetran(n['link'])
            # recursively build the conditinal fp tree
            contree = fp_tree(condtran, sup)
            conwords = contree.findfqt(fqset)
            if conwords is not None:
                for words in conwords:
                    result.append(words)
        return result

    def checkheight(self):
        if len(list(self.root.children.keys())) == 0:
            return False
        else:
            return True


# In[]:
min_sup = 4

test_data = [['I1', 'I2', 'I5'],
             ['I2', 'I4'],
             ['I2', 'I3'],
             ['I1', 'I2', 'I4'],
             ['I1', 'I3'],
             ['I2', 'I3'],
             ['I1', 'I3'],
             ['I1', 'I2', 'I3', 'I5'],
             ['I1', 'I2', 'I3']]


fptree = fp_tree(test_data, min_sup)  # create FP tree on data
# print(fptree.root.visittree())
print("\n========== Printing Frequent Word Set on  ==========")
frequentwordset = fptree.findfqt()  # mining frequent patt
frequentwordset = sorted(frequentwordset, key=lambda k: -k[1])


# print frequent patt
for word in frequentwordset:
    count = (str(word[1])+"\t")
    words = ''
    for val in word[0]:
        words += (str(val)+" ")
    print(count+words)

print('test')
# print conditional fp tree height >1
for i in fptree.header_table[::-1]:
    lines = fptree.condtreetran(i['link'])
    condtree = fp_tree(lines, min_sup)
    if(condtree.checkheight()):
        print('Condtional FPTree Root on '+(i['item']))
        print(condtree.root.visittree())

# %%
