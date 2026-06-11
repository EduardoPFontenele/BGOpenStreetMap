from search_base import SearchProblem, SearchAlgorithm, State
from map_util import CityMap, GeoLocation, create_bg_map, location_from_tag, read_map, print_path,compute_distance
from visualization import plot_map
import plotly.graph_objects as go
from typing import Iterator
from ucs import UniformCostSearch
from a_start import AStar


class WaypointsShortestPathProblem(SearchProblem):

    def __init__ (self, start_location: str, end_location: str, waypoint_tags: list[str], city_map: CityMap):

        self.city_map = city_map
        self.end_location = end_location
        self.waypoint_tags = frozenset(waypoint_tags)

        start_memory = set()

        # ITERA SOBRE OS PONTOS OBRIGATÓRIOS
        for tag in waypoint_tags:

            # VERIFICA SE O WAYPOINT ESTÁ NA LISTA DE TAGS DO LOCAL ATUAL
            if tag in city_map.tags[start_location]:
                start_memory.add(tag)

        super().__init__(
            initial_state = State(start_location, frozenset(start_memory)),
            goal_state = State(end_location, self.waypoint_tags),
        )

    def successors(self,state):
        
        for neighbor, distance in self.city_map.distances[state.location].items():
            new_memory = set(state.memory)

            for tag in self.waypoint_tags:
                if tag in self.city_map.tags[neighbor]:
                    new_memory.add(tag)
            
            yield State(neighbor, frozenset(new_memory)), neighbor, distance

    def h(self, state: State) -> float:
        return compute_distance(
            self.city_map.geo_locations[state.location],
            self.city_map.geo_locations[self.end_location],
        )
    
if __name__ == "__main__":

    city_map = create_bg_map()
    start = location_from_tag("landmark=ufmt-administracao", city_map)
    end = location_from_tag("landmark=forum", city_map)
    waypoint_tags = ["landmark=igreja_matriz", "landmark=flutuante"]

    problem = WaypointsShortestPathProblem(start, end ,waypoint_tags , city_map)
    astar = AStar()
    astar.solve(problem)

    #ucs = UniformCostSearch()
    #ucs.solve(problem)

    print_path([start] + astar.actions, waypoint_tags, city_map)
    plot_map(city_map, [start] + astar.actions,waypoint_tags=waypoint_tags, map_name="A* com Waypoints")