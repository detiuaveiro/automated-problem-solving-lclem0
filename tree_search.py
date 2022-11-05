
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
        
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,actioncost,problem): 
        self.state = state
        self.parent = parent 
        #self.problem = problem #ex 11
        self.depth = 0 if parent == None else parent.depth + 1
        self.cost = 0 if parent == None else  parent.cost + actioncost  #ex8
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        heuristic = self.problem.domain.heuristic(self.problem.initial, self.problem.goal)
        root = SearchNode(problem.initial, None,None, heuristic) #ex 8
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0

    # obter o caminho (sequencia de estados) da raiz ate um nó
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    @property # propriedade é uma solucao que ja existe, é so acessar
    def length(self):
        return self.solution.depth

    @property # propriedade é uma solucao que ja existe, é so acessar
    def avg_branching(self):    #Average VB = (N-1)/X   #ex 6
        N = self.terminals + self.non_terminals
        X = self.non_terminals
        return (N-1)/X
    @property # propriedade é uma solucao que ja existe, é so acessar
    def cost(self):    #Average VB = (N-1)/X   #ex 6
        return self.solution.cost


    # procurar a solucao
    def search(self,limit = None):
        self.non_terminals = 0  #ex 5
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.solution = node 
                self.terminals =  len(self.open_nodes)+1  #ex 5
                return self.get_path(node)
            self.non_terminals += 1     #ex 5
            if limit != None and node.depth >= limit:
                continue #vai diretamente para o inicio do while
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    actioncost = self.problem.domain.cost(node.state,a) #ex 8
                    heuristic = self.problem.domain.heuristic(newstate,self.problem.goal) #ex 12  problema    #ver todos ex para preparar  para tp1 dia 4 nov
                    newnode = SearchNode(newstate,node,actioncost,heuristic)
                    lnewnodes.append(newnode)
                    
            self.add_to_open(lnewnodes)
        return 

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)       #ex 10
            self.open_nodes.sort(key = lambda n : n.cost)

