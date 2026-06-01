import json
from collections import defaultdict
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

import osmium
from osmium import osm

# Constants
RADIUS_EARTH = 6371000  # Raio da terra em metros (~ equivalent to 3956 miles).
UNIT_DELTA = 0.00001    # Valor em graus (latitude ou longitude) que equivale a um ~1m.

#------------- Classe usada para abstrair uma localização geográfica ------------------#  
class GeoLocation:
    # Construtor da classe GeoLocation    
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    # Define uma representação em string para a classe GeoLocation
    def __repr__(self):
        return f"{self.latitude},{self.longitude}"

# ---------------------- Classe que define um mapa da cidade ------------------#
class CityMap:
   
    def __init__(self) -> None:
        # Dicionário: {label da localização -> Geolocation (latitude/longitude}
        # (e.g., self.geo_locations["0,1"] = GeoLocation(37.423576, -122.170087)
        self.geo_locations: dict[str, GeoLocation] = {}

        # Dicionário: {label da localização -> lista de tags}
        # (e.g., self.tags["0,1"] = ["amenity=building", "landmark=Gates"])
        self.tags: dict[str, list[str]] = defaultdict(list)

        # Dicionário: {label da localização -> {label da localização adjacente -> distância entre as duas}}
        # (e.g., self.distances["0,1"]["0,2"] = 21.3)
        self.distances: dict[str, dict[str, float]] = defaultdict(dict)

    # Adiciona uma localização ao mapa, com um label e um conjunto de tags
    def add_location(self, label: str, location: GeoLocation, tags: list[str]) -> None:
        assert label not in self.geo_locations, f"Localização {label} já processada!"
        self.geo_locations[label] = location
        self.tags[label] = [f"label={label}"] + tags

    # Adiciona uma conexão entre duas localizações, incluindo a distância entre elas
    def add_connection(self, source: str, target: str, distance: float = None) -> None:
        if distance is None:
            distance = compute_distance(self.geo_locations[source], self.geo_locations[target])
        self.distances[source][target] = distance
        self.distances[target][source] = distance


# Função para adicionar marcos (landmarks) ao mapa da cidade, associando-os a localizações geográficas
def add_landmarks(city_map: CityMap, landmark_path: str, tolerance_meters: float = 250.0) -> None:
    """
    Landmarks are explicitamente definidos no arquivo `landmark_path`, cujas coordenadas foram 
    obtidas do Google Maps. Eles podem não se alinhar exatamentecom as localizações existentes 
    no CityMap, por isso mapeamos um determinado landmark para a localização existente mais próxima 
    (de acordo com uma tolerância máxima).
    """
    with open(landmark_path) as f:
        landmarks = json.load(f)

    # Iterate through landmarks and map onto the closest location in `city_map`
    for item in landmarks:
        latitude_string, longitude_string = item["geo"].split(",")
        geo = GeoLocation(float(latitude_string), float(longitude_string))

        # Find the closest location by searching over all locations in `city_map`
        best_distance, best_label = min(
            (compute_distance(geo, existing_geo), existing_label)
            for existing_label, existing_geo in city_map.geo_locations.items()
        )

        if best_distance < tolerance_meters:
            for key in ["landmark", "amenity"]:
                if key in item:
                    print(f"Adding landmark {item[key]} to location {best_label} (distance = {best_distance:.2f}m)" )
                    city_map.tags[best_label].append(f"{key}={item[key]}")

# Função para encontrar uma localização no mapa a partir de uma tag específica
def location_from_tag(tag: str, city_map: CityMap) -> str | None:
    possible_locations = sorted([location for location, tags in city_map.tags.items() if tag in tags])
    return possible_locations[0] if len(possible_locations) > 0 else None

# Função para calcular a distância entre duas localizações geográficas usando a fórmula de Haversine
def compute_distance(geo1: GeoLocation, geo2: GeoLocation) -> float:
    """
    Calcula a distância em linha reta entre duas localizações geográficas
    especificadas por latitude e longitude.

    Essa função é análoga ao cálculo da distância euclidiana entre pontos
    em um plano. Entretanto, como a Terra possui formato aproximadamente
    esférico, utilizamos a fórmula de Haversine para calcular a distância
    sobre a superfície curva do planeta.

    Mais informações sobre a fórmula de Haversine:
    https://en.wikipedia.org/wiki/Haversine_formula

    Parametros:
    `geo1`: Localização de origem (`GeoLocation`) contendo latitude e longitude.
    `geo2`: Localização de destino (`GeoLocation`) contendo latitude e longitude.
    
    Returns:
    Distância entre `geo1` e `geo2` em metros.
    """
    lon1, lat1 = radians(geo1.longitude), radians(geo1.latitude)
    lon2, lat2 = radians(geo2.longitude), radians(geo2.latitude)

    # Formula Haversine
    delta_lon, delta_lat = lon2 - lon1, lat2 - lat1
    haversine = (sin(delta_lat / 2) ** 2) + (cos(lat1) * cos(lat2)) * (sin(delta_lon / 2) ** 2)

    # Retorna a distância em metros
    return 2 * RADIUS_EARTH * asin(sqrt(haversine))


# Função para ler um arquivo `.pbf` do OpenStreetMaps e construir um `CityMap`
def read_map(osm_path: str) -> CityMap:
    """
    Cria um objeto CityMap dado um caminho para um arquivo OSM `.pbf`; 
    utiliza o pacote osmium para realizar todo o processamento de localizações 
    discretas e conexões entre elas.

    :param osm_path: Caminho para o arquivo `.pbf` que define um conjunto de localizações e conexões.
    :return Um objeto CityMap inicializado, construído usando os dados do OpenStreetMaps.
    """
    # Note :: `osmium` defines a nice class called `SimpleHandler` to facilitate
    # reading `.pbf` files.
    #   > You can read more about this class/functionality here:
    #     https://docs.osmcode.org/pyosmium/latest/intro.html
    class MapCreationHandler(osmium.SimpleHandler):
        def __init__(self) -> None:
            super().__init__()
            self.nodes: dict[str, GeoLocation] = {}
            self.tags: dict[str, list[str]] = defaultdict(list)
            self.edges: set[tuple[str, str]] = set()

        def node(self, n: osm.Node) -> None:
            """An `osm.Node` contains the actual tag attributes for a given node."""
            self.tags[str(n.id)] = [f"{key}={value}" for key, value in n.tags]
        
        def way(self, w: osm.Way) -> None:
            """An `osm.Way` contains an ordered list of connected nodes."""

            # We only include "ways" that are accessible on foot
            #   =>> Reference: https://github.com/Tristramg/osm4routing2
            #                  See -> `src/osm4routing/categorize.rs#L96`
            path_type = w.tags.get("highway", None)
            if path_type is None or path_type in {
                "motorway",
                "motorway_link",
                #"trunk",
                "trunk_link",
            }:
                return
            elif (
                w.tags.get("pedestrian", "n/a") == "no"
                or w.tags.get("foot", "n/a") == "no"
            ):
                return

            # Otherwise, iterate through all nodes along the "way"...
            way_nodes = w.nodes
            for source_idx in range(len(way_nodes) - 1):
                s, t = way_nodes[source_idx], way_nodes[source_idx + 1]
                s_label, t_label = str(s.ref), str(t.ref)
                s_loc = GeoLocation(s.location.lat, s.location.lon)
                t_loc = GeoLocation(t.location.lat, t.location.lon)

                # Assert that the locations aren't the same!
                assert s_loc != t_loc, "Source and Target are the same location!"

                # Add to trackers...
                self.nodes[s_label], self.nodes[t_label] = s_loc, t_loc
                self.edges.add((s_label, t_label))

    # Build nodes & edges via MapCreationHandler
    #   > Pass `location=True` to enforce embedded lat/lon geometries!
    map_creator = MapCreationHandler()
    map_creator.apply_file(osm_path, locations=True)

    # Build CityMap by iterating through the parsed nodes and connections
    city_map = CityMap()
    for node_label in map_creator.nodes:
        city_map.add_location(node_label, map_creator.nodes[node_label], tags=map_creator.tags[node_label])

    # When adding connections, don't pass distance flag (automatically compute!)
    for src, tgt in map_creator.edges:
        city_map.add_connection(src, tgt)

    return city_map

# Função para imprimir o caminho encontrado, incluindo as tags associadas a cada localização no caminho
def print_path(path: list[str], waypoint_tags: list[str], city_map: CityMap, out_path: str = "path.json"):
    done_waypoint_tags = set()
    for location in path:
        for tag in city_map.tags[location]:
            if tag in waypoint_tags:
                done_waypoint_tags.add(tag)
        tags_str = " ".join(city_map.tags[location])
        done_tags_str = " ".join(sorted(done_waypoint_tags))
        print(f"Location {location} tags:[{tags_str}]; done:[{done_tags_str}]")

    # (Optional) Write path to file, for use with `visualize.py`
    if out_path is not None:
        with open(out_path, "w") as f:
            data = {"waypoint_tags": waypoint_tags, "path": path}
            json.dump(data, f, indent=2)



# Mostra uma visão geral do mapa fornecido, com tags para cada localização.
def print_map(city_map: CityMap):
    for label in city_map.geo_locations:
        tags_str = " ".join(city_map.tags[label])
        print(f"{label} ({city_map.geo_locations[label]}): {tags_str}")
        for label2, distance in city_map.distances[label].items():
            print(f"  -> {label2} [distance = {distance}]")

# Função para criar um mapa específico da cidade de Barra do Garças
def create_bg_map() -> CityMap:
    city_map = read_map("data/barra-do-garcas.pbf")
    add_landmarks(city_map, "data/bg-landmarks.json")
    return city_map

if __name__ == "__main__":
    bg_map = create_bg_map()
    locations = location_from_tag(f"amenity=food", bg_map)
    print(f"Locations with 'amenity=food': {locations}")