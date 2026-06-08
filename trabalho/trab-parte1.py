from search_base import SearchProblem, SearchAlgorithm, State
from map_util import CityMap, GeoLocation, create_bg_map, location_from_tag, read_map, print_path,compute_distance
from visualization import plot_map
import plotly.graph_objects as go
from typing import Iterator
from ucs import UniformCostSearch
from a_start import AStar

# Modela o problema de encontrar o caminho mais curto entre duas localizações em um mapa da cidade
class ShortestPathProblem(SearchProblem):
    def __init__(self, start_location: str, end_location: str, city_map: CityMap):
        super().__init__(initial_state=State(start_location), goal_state=State(end_location))
        self.city_map = city_map

    
    def successors(self, state: State) -> Iterator[tuple[State, str, float]]:

        for neighbor, dist in self.city_map.distances[state.location].items():
           yield State(neighbor), neighbor, dist

    def h(self, state: State) -> float:
        return compute_distance(
            self.city_map.geo_locations[state.location],
            self.city_map.geo_locations[self.goal_state.location])

# Realiza testes e visualiza os resultados
if __name__ == "__main__":
    # Exemplo de uso
    city_map = create_bg_map()  # criar um mapa de bg
    start = location_from_tag("landmark=ufmt-biblioteca", city_map)
    end = location_from_tag("landmark=madre-marta", city_map)
    
    problem = ShortestPathProblem(start_location=start, end_location=end, city_map=city_map)
    ucs = AStar()
    ucs.solve(problem)

    # Função para gerar um arquivo json com o caminho encontrado, caso queira salva-lo
    # para visualização posterior: python visualization.py --path-file path.json
    print_path([start] + ucs.actions, [], city_map) 
    
    # Visualiza o mapa e o caminho encontrado 
    plot_map(city_map, [start] + ucs.actions, waypoint_tags=[], map_name="Shortest Path Visualization")