from typing import Iterator

#----------------- Classe que define estados (State) ----------------------#
class State:
    """
    Um estado consiste em uma string `location` e `memory` (possivelmente null).
    Note que `memory` deve ser um tipo de dado "Hashable" (porque implementamos 
    o algoritmo de busca usando um dict e usamos instâncias da classe `State` 
    como chaves para os valores). Por exemplo:
        - qualquer primitivo não mutável (str, int, float, etc.)
        - tuplas
        - combinações aninhadas dos itens acima
    A medida que você implementa diferentes tipos de problemas de busca ao longo
    da tarefa, pense no que `memory` deve conter para permitir uma busca eficiente!

    Uso:
        state = State(location="A", memory=("some_hashable_data_type", 123))
    """         

    def __init__(self, location: str, memory: frozenset=None):
        self.location = location    
        self.memory = memory if memory is not None else frozenset()

    # Dada uma label e um frozenset retorna um IDENTIFICADOR inteiro para a tupla
    def __hash__(self):
        return hash((self.location, self.memory))
    
    def __repr__(self):
        return f"State(location={self.location!r}, memory={self.memory!r})"
    
    # Para vericiar se a label e uma info extra são IGUAIS
    def __eq__(self, other):
        return (self.location, self.memory) == (other.location, other.memory)
    
#----------Classe base para problemas de busca (SearchProblem) -------------#
class SearchProblem:
    # Construtor da classe Problem
    def __init__(self, initial_state: State, goal_state: State): 
        self.initial_state = initial_state # Estado inicial do problema
        self.goal_state = goal_state       # Estado objetivo do problema 
    
    # Retorna os estados sucessores de um estado, junto com a ação e o custo
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
        raise NotImplementedError("Override me")        

    # Retorna o estado inicial do problema
    def get_initial_state(self) -> State:
        return self.initial_state
    
    # Verifica se um estado é o estado objetivo
    def is_goal(self, state: State) -> bool:
        return state == self.goal_state
    
    # Heuristica usada em buscas informadas (A* por exemplo)
    def h(self, state: State)-> float:
        raise NotImplementedError("Override me")
    
    # Mostra o problema como uma string formatada
    def __repr__(self)-> str:
        return f"Problem(initial={self.initial_state!r}, goal={self.goal_state!r})"
    
#-------------Classe que define nós da árvore de busca (Node) ---------------#
class Node:
    # Construtor da classe Node
    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state         # Estado atual do nó
        self.parent = parent       # Referência para o nó pai (None para raiz)
        self.action = action       # Ação que levou a este nó (None para raiz)
        self.path_cost = path_cost # g(n) - Custo acumulado para chegar ao nó
    
    # Retorna a sequência de ações da raiz até chegar ao nó
    def path_actions(self)-> list[str]:
       actions = []
       node = self
       
       # Constrói a lista de ações
       while node.parent is not None:
          actions.append(node.action)
          node = node.parent
       
       # Inverte a lista e retorna
       actions.reverse()
       return actions
        
    # Retorna a sequência de estados da raiz até chegar ao nó
    def path_states(self)-> list[State]:
        node = self
        states = []

        # Constrói a lista de estados
        while node is not None:
            states.append(node.state)
            node = node.parent
        
        # Inverte a lista e retorna
        states.reverse()
        return states
   
    # Computa a profundidade do nó
    def depth(self)-> int:
        node = self
        d = 0
        while node.parent is not None:
            d += 1
            node = node.parent
        return d

    # Expande o nó, de acordo com um problema, retornando uma lista de nós filhos
    def expand(self, problem: SearchProblem):
        for state, action, cost in problem.successors(self.state):
            yield Node(state, self, action, self.path_cost + cost)
    
    # Mostra o estado do nó como uma string formatada
    def __repr__(self):
        return f"Node({self.state!r})" 
    
#-------------Classe base para algoritmos de busca (SearchAlgorithm) ---------------#
class SearchAlgorithm:    
    def solve(self, search_problem: SearchProblem) -> None:
        raise NotImplementedError("Override me")