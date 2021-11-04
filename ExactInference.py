import numpy as np
import itertools

class ExactInference:
    def __init__(self):
        pass

    def variableElimination(self, query, evidence, bn):
        if query in evidence.keys():
            print("NOPE")
            quit()
        factors = {}
        # instead of reversed do we need a heuristic for ordering
        for v in reversed(bn.variables):
            factors[v] = self.makeFactor(v, evidence, bn)
            if v != query and v not in evidence.keys():    #is a hidden variable if hidden we sum over that var
                factors = self.sumOut(v, factors)
        return np.linalg.norm(self.pointwiseProduct(factors))


    def makeFactor(self, v, e, bn):
        #get probs
        node = bn.getNode(v)
        var = []
        par_val = []
        factors = {}
        for par in node.parent:
            if par not in e.keys():
                var.append(par)
                par_val.append(bn.getNode(par).domain)
            else:
                par_val.append([e[par]])
        if v in e.keys():
            print('in')
            v_key = [e[v]]
        else:
            print('not')
            v_key = node.domain
        print(v_key)
        par_keys = list(itertools.product(*par_val))
        for pk in par_keys:
            key = ""
            for val in pk:
                key += str(val) + ', '
            key = key[:-2]
            factors[key] = {}
            print(key)
            for vk in v_key:
                print(vk)
                factors[key][vk] = node.prob[key][vk]

        return factors #dict of probs

    def sumOut(self, v, factors):
        #iterate over domain v
        return factors

    def pointwiseProduct(self, factors):
        return factors