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
        frontier = PriorityQueue(key=lambda n: self.g(n)) 
        reached = {} # Guarda o nó de menor custo para cada estado alcançado

        # COLOQUE AQUI O SEU CÓDIGO PARA TERMINAR UCS COM TABELA DE ESTADOS ALCANÇADOS 
       