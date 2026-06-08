from search_base import SearchProblem, SearchAlgorithm, Node, State
from util import PriorityQueue

#---------------- Busca com custo uniforme (Uniform-Cost Search - UCS) ---------------#
class UniformCostSearch(SearchAlgorithm):
    # Construtor
    def __init__(self):
        super().__init__()
        self.actions: list[str] = []           # Lista de ações para chegar ao estado objetivo
        self.states: list[State] = []          # Lista de estados para chegar ao estado objetivo
        self.path_cost: float = None           # Soma dos custos ao longo do caminho
        self.num_states_explored: int = 0      # Número de estados explorados
         
    def g(self, n:Node)->float:
        return n.path_cost
    
    # Implementação da UCS com tabela de estados alcançados para evitar reexploração    
    def solve(self, search_problem: SearchProblem) -> None: 
        # re-inicializa as variáveis 
        self.actions: list[str] = []
        self.states: list[State] = []           
        self.path_cost: float = None           
        self.num_states_explored: int = 0      
        
        # Inicializa a fronteira e a tabela de estados alcançados
        start = Node(search_problem.get_initial_state())
        frontier = PriorityQueue(key=lambda n: self.g(n)) 
        frontier.push(start)
        reached = {start.state: start} # Guarda o nó de menor custo para cada estado alcançado

        while not frontier.is_empty():

            removed = frontier.pop()
            self.num_states_explored += 1

            if search_problem.is_goal(removed.state):

                self.actions = removed.path_actions()
                self.states = removed.path_states()
                self.path_cost = removed.path_cost

                return self
            
            for child in removed.expand(search_problem):

                s = child.state
                if s not in reached or child.path_cost < reached[s].path_cost:
                    reached[s] = child
                    frontier.push(child)

       