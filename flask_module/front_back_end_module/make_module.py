#!/usr/bin/env python3

def printline(lines):
    print('[')
    for i,line in enumerate(lines):
        print(i, line)
    print(']')

def module_to_lines():
    s = ''
    with open('module.txt', 'r+') as f:
        s = f.read()

    lines = s.split('\n')
    # printline(lines)
    lines = [line if '#' not in line else line.split('#', 1)[0]
        for line in lines
    ]
    # printline(lines)
    lines = [line for line in lines
        if line.strip() != ''
    ]
    return lines

def tab_text(line):
    n = 0
    while line[0] == ' ':
        line = line[4:]
        n += 1
    return (n, line)

class Node:
    def __init__(self, data=None, father=None):
        self.data = data
        self.sons = []
        self.father = father
    def parse_lines(lines):
        root = Node({'tab':-1})
        cur_node = root
        for line in lines:
            tab,code = tab_text(line)
            while cur_node.data['tab'] != tab - 1:
                cur_node = cur_node.father
            cur_node.sons.append(Node({'tab':tab, 'code':code}, father=cur_node))
        return root

lines = module_to_lines()
root = Node.parse_lines(lines)






# printline(lines)




