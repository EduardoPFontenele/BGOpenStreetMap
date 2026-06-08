from search_base import SearchProblem, SearchAlgorithm, State
from map_util import CityMap, GeoLocation, create_bg_map, location_from_tag, read_map, print_path
from visualization import plot_map
import plotly.graph_objects as go
from typing import Iterator
from ucs import UniformCostSearch

# Modela o problema de encontrar o caminho mais curto entre duas localizações em um mapa da cidade
class ShortestPathProblem(SearchProblem):
    def __init__(self, start_location: str, end_location: str, city_map: CityMap):
        super().__init__(initial_state=State(start_location), goal_state=State(end_location))
        self.city_map = city_map

    
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:
        # IMPLEMENTE AQUI: Gere os estados sucessores a partir do estado atual
        pass


# Realiza testes e visualiza os resultados
if __name__ == "__main__":
    # Exemplo de uso
    city_map = create_bg_map()  # criar um mapa de bg
    start = location_from_tag("landmark=ufmt-biblioteca", city_map)
    end = location_from_tag("landmark=madre-marta", city_map)
    
    problem = ShortestPathProblem(start_location=start, end_location=end, city_map=city_map)
    ucs = UniformCostSearch()
    ucs.solve(problem)

    # Função para gerar um arquivo json com o caminho encontrado, caso queira salva-lo
    # para visualização posterior: python visualization.py --path-file path.json
    print_path([start] + ucs.actions, [], city_map) 
    
    # Visualiza o mapa e o caminho encontrado 
    plot_map(city_map, [start] + ucs.actions, waypoint_tags=[], map_name="Shortest Path Visualization")