from search_base import SearchProblem, SearchAlgorithm, Node, State
from util import PriorityQueue

#---------------- Busca A* (A-Star Search) ---------------#
class AStar(SearchAlgorithm):
    # Construtor
    def __init__(self):
        super().__init__()
        self.actions: list[str] = []           # Lista de ações para chegar ao estado objetivo
        self.states: list[State] = []          # Lista de estados para chegar ao estado objetivo
        self.path_cost: float = 0.0          # Soma dos custos ao longo do caminho
        self.num_states_explored: int = 0      # Número de estados explorados
         
    # COLOQUE AQUI O SEU CÓDIGO PARA IMPLEMENTAR A_STAR COM TABELA DE ESTADOS ALCANÇADOS
