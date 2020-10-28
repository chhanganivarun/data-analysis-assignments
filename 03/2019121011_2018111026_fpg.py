#!/usr/bin/env python
# config utf-8

# In[]:
import numpy as np
from copy import deepcopy
# In[]:
with open('test.txt', 'r') as fi:
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


class fp_tree_top_down:
    def __init__(self, dataset, support):
        self.root = node(-1, np.inf)

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

    def increment_item_subtree(self, subtree, item_name, link, count):
        flag = 0
        new_node = deepcopy(link)
        for i in range(len(subtree)):
            if subtree[i]['item'] == item_name:
                flag = 1

                # new_node.link = subtree[i]['link']
                # subtree[i]['link'] = new_node
                iter_in = subtree[i]['link']
                while iter_in.link is not None:
                    iter_in = iter_in.link
                iter_in.link = new_node
                new_node.count += count

                subtree[i]['count'] += count
        if not flag:
            subtree.append(
                {'item': item_name, 'count': count, 'link': link})

    def find_idx(self, table, item_name):
        for i in range(len(table)):
            if table[i]['item'] == item_name:
                return i
        return -1

    def clear_tree_above(self, i_h):
        iter_i = self.header_table[i_h]['link']
        while iter_i is not None:
            iter_p = iter_i.parent
            while iter_p.count != np.inf:
                iter_p.count = 0
                iter_p = iter_p.parent
            iter_i = iter_i.link

    def buildsubtable(self, I):
        subtree = list()
        i_h = self.find_idx(self.header_table, I['item'])
        self.clear_tree_above(i_h)
        iter_i = self.header_table[i_h]['link']
        while iter_i is not None:
            cnt = iter_i.count
            iter_p = iter_i.parent
            while iter_p.count != np.inf:
                p_sh = self.find_idx(subtree, iter_p.item)
                if p_sh == -1:
                    p_h = self.find_idx(self.header_table, iter_p.item)
                    subtree.append(
                        {'item': iter_p.item, 'count': cnt, 'link': self.header_table[p_h]['link']})
                else:
                    subtree[p_sh]['count'] += cnt
                iter_p.count += cnt
                iter_p = iter_p.parent
            iter_i = iter_i.link

        return subtree

    def findfqt(self, table=None, parentnode=None):
        if len(list(self.root.children.keys())) == 0:
            return None
        if table is None:
            table = self.header_table
        if parentnode is None:
            parentnode = list()

        result = []
        sup = self.support
        # starting from the end of nodetable
        for n in table:
            if n['count'] >= sup:
                # print([n, *parentnode])
                result.append([n, *parentnode])
                subtable = self.buildsubtable(n)
                result += self.findfqt(subtable, [n, *parentnode])
        return result
# In[]:


class fp_tree:
    def __init__(self, dataset, support):
        self.root = node(-1, np.inf)

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


# In[]:
min_sup = 2

test_data = dataset

# In[]:

# Using bottom up:

fptree = fp_tree(test_data, min_sup)
# print(fptree.root.visittree())
frequentwordset = fptree.findfqt()
frequentwordset = sorted(frequentwordset, key=lambda k: -k[1])


for word in frequentwordset:
    count = (str(word[1])+"\t")
    words = ''
    for val in word[0]:
        words += (str(val)+" ")
    print(count+words)


# In[]:
# Using top down


fptree = fp_tree_top_down(test_data, min_sup)
frequentwordset = fptree.findfqt()
for word in frequentwordset:
    cnt = len(test_data)
    for i in word:
        cnt = min(i['count'], cnt)
    count = (str(cnt)+"\t")
    words = ''
    for val in word:
        words += (str(val['item'])+" ")
    print(count+words)
# %%
