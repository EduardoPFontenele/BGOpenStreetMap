from search_base import SearchProblem, SearchAlgorithm, Node, State
from util import PriorityQueue

class AStar(SearchAlgorithm):
    # Construtor
    def __init__(self):
        super().__init__()
        self.actions: list[str] = []           # Lista de ações para chegar ao estado objetivo
        self.states: list[State] = []          # Lista de estados para chegar ao estado objetivo
        self.path_cost: float = None           # Soma dos custos ao longo do caminho
        self.num_states_explored: int = 0      # Número de estados explorados

    
    def f(self, n:Node, problem: SearchProblem)-> float:
        """
        f(n) = custo real de ir de um ponto à outro + estimativa de ir de um ponto à outro.
        Formalmente: f(n) = g(n) + h(n).
        """
        return n.path_cost + problem.h(n.state)
         
        # Implementação da UCS com tabela de estados alcançados para evitar reexploração    
    def solve(self, search_problem: SearchProblem) -> None: 
        # re-inicializa as variáveis 
        self.actions: list[str] = []
        self.states: list[State] = []           
        self.path_cost: float = None           
        self.num_states_explored: int = 0      

        # Inicializa a fronteira e a tabela de estados alcançados
        frontier = PriorityQueue(key=lambda n: self.f(n, search_problem)) 
        reached = {} 

        node = Node(search_problem.get_initial_state())
        frontier.push(node)
        reached = {node.state: node}

        while not frontier.is_empty():
            node = frontier.pop()
            self.num_states_explored += 1

            # VERIFICA SE O NÓ REMOVIDO DA FRONTEIRA É O ESTADO-META
            if search_problem.is_goal(node.state):
                self.actions = node.path_actions()
                self.states = node.path_states()
                self.path_cost = node.path_cost
                
                return self
            
            for child in node.expand(search_problem):
                s = child.state

                if s not in reached or self.f(child,search_problem) < self.f(reached[s],search_problem):
                    reached[s] = child
                    frontier.push(child)
    