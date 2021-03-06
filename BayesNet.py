from Node import Node
import re

class BayesNet:
    def __init__(self, file):
        self.file_name = file
        self.nodes = []
        self.variables = []

    def generateList(self):
        file = open(self.file_name, 'r')  # opens file
        fileline = file.read().split('}\n')
        for val in fileline:
            if not val:
                continue
            val = val.split('{\n')
            head = val[0].split()
            type = head[0]
            name = head[1]
            try:
                rest = val[1]
            except:
                pass
            if rest and type == 'variable':
                rest = re.split(r'{|}', rest)
                domain = rest[1].replace(" ", '').split(',')
                self.nodes.append(Node(name, domain))
                self.variables.append(name)
            elif rest and type == 'probability':
                dependence = re.split(r'[(|)]', val[0].replace(" ", ''))
                var = dependence[1]
                parents = dependence[2]
                node = self.getNode(var)
                if parents:
                    node.parent = parents.split(',')
                    for parent in node.parent:
                        par = self.getNode(parent)
                        par.children.append(node.name)
                #deal with rest
                rest = rest.split(';\n')
                for r in rest:
                    if not r:
                        continue
                    if '(' in r:
                        prob = re.split(r'[()]', r)
                        probs = prob[2].split((','))
                        node.prob[prob[1]] = {}
                        for i in range(len(node.domain)):
                            node.prob[prob[1]][node.domain[i]] = float(probs[i])
                    else:
                        probs = re.split(r"[' ',]", r)
                        while '' in probs:
                            probs.remove('')
                        probs = probs[1:]
                        for i in range(len(node.domain)):
                            node.prob[node.domain[i]] = float(probs[i])

    def getNode(self, varName):
        for node in self.nodes:
            if node.name == varName:
                return node

    def updateState(self, node, state):
        for n in self.nodes:
            if n == node:
                n.state = state
