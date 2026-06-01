#-------------------------- Fila de Prioridade -------------------------------#
import heapq
import itertools
from typing import Callable
from search_base import Node

#-------------------------- Fila de Prioridade -------------------------------#
class PriorityQueue:
    # Construtor
    def __init__(self, items=(), key: Callable[[Node], float]=None):
        self.key = key
        self.elements = []
        self.counter = itertools.count() # Para desempate em caso de prioridades iguais
        # adiciona os itens iniciais, se houver
        for item in items:
            self.push(item)        

    # Adiciona um item com uma prioridade
    def push(self, item: Node)->None:
        heapq.heappush(self.elements, (self.key(item), next(self.counter), item)) 

    # Remove e retorna o nó com a menor prioridade
    def pop(self)->Node:
        return heapq.heappop(self.elements)[2]
    
    # Verifica se a fila de prioridade está vazia
    def is_empty(self)->bool:
        return len(self.elements) == 0
    
    # Retorna o número de elementos na fila de prioridade
    def __len__(self)->int:
        return len(self.elements)