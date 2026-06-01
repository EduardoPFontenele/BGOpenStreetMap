import argparse
import json
from typing import List
import plotly.graph_objects as go
from map_util import CityMap, add_landmarks, read_map


def plot_map(city_map: CityMap, path: List[str], waypoint_tags: List[str], map_name: str):
    """
    Plota o mapa completo, destacando o caminho fornecido.

    city_map: mapa da cidade a ser plotado.
    path: Lista de rótulos (labels) de localizações do caminho.
    waypoint_tags: Lista de tags que queremos destacar ao longo do caminho.
    map_name: Título a ser exibido para a visualização do mapa.
    """
    lat, lon = [], []

    # Convert `city_map.distances` to a list of (source, target) tuples...
    connections = [(source, target) for source in city_map.distances for target in city_map.distances[source]]
    for source, target in connections:
        lat.append(city_map.geo_locations[source].latitude)
        lat.append(city_map.geo_locations[target].latitude)
        lat.append(None)
        lon.append(city_map.geo_locations[source].longitude)
        lon.append(city_map.geo_locations[target].longitude)
        lon.append(None)

    # Plot all states & connections
    #fig = px.line_geo(lat=lat, lon=lon)
    fig = go.Figure()
    fig.add_trace(go.Scattermap(lat=lat,lon=lon,mode="lines"))
    fig.update_layout(map_style="open-street-map")
    
    # Plot path (represented by connections in `path`)
    if len(path) > 0:
        solution_lat, solution_lon = [], []

        # Get and convert `path` to (source, target) tuples to append to lat, lon lists
        connections = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        for connection in connections:
            source, target = connection
            solution_lat.append(city_map.geo_locations[source].latitude)
            solution_lat.append(city_map.geo_locations[target].latitude)
            solution_lat.append(None)
            solution_lon.append(city_map.geo_locations[source].longitude)
            solution_lon.append(city_map.geo_locations[target].longitude)
            solution_lon.append(None)

        # Visualize path by adding a trace
        fig.add_trace(
            go.Scattermap(
                lat=solution_lat,
                lon=solution_lon,
                mode="lines",
                line=dict(width=5, color="blue"),
                name="solution",
            )
        )

        # Plot the points
        for i, location in enumerate(path):
            tags = set(city_map.tags[location]).intersection(set(waypoint_tags))
            if i == 0 or i == len(path) - 1 or len(tags) > 0:
                for tag in city_map.tags[location]:
                    if tag.startswith("landmark="):
                        tags.add(tag)
            if len(tags) == 0:
                continue

            # Add descriptions as annotations for each point
            description = " ".join(sorted(tags))

            # Color the start node green, the end node red, intermediate gray
            if i == 0:
                color = "red"
            elif i == len(path) - 1:
                color = "green"
            else:
                color = "gray"

            waypoint_lat = [city_map.geo_locations[location].latitude]
            waypoint_lon = [city_map.geo_locations[location].longitude]

            fig.add_trace(
                go.Scattermap(
                    lat=waypoint_lat,
                    lon=waypoint_lon,
                    mode="markers",
                    marker=dict(size=20, color=color),
                    name=description,
                )
            )

    # Plot city_map locations with special tags (e.g. landmarks, amenities)
    for location_id, lat_lon in city_map.geo_locations.items():
        tags = city_map.tags[location_id]
        for tag in tags:
            if "landmark" in tag:
                fig.add_trace(
                    go.Scattermap(
                        #locationmode="USA-states",
                        lon=[lat_lon.longitude],
                        lat=[lat_lon.latitude],
                        text=tag.split("landmark=")[1],
                        name=tag.split("landmark=")[1],
                        marker=dict(size=10, color="purple"),
                    )
                )
            elif "amenity" in tag:
                fig.add_trace(
                    go.Scattermap(
                        #locationmode="USA-states",
                        lon=[lat_lon.longitude],
                        lat=[lat_lon.latitude],
                        text=tag.split("amenity=")[1],
                        name=tag.split("amenity=")[1],
                        marker=dict(size=10, color="blue"),
                    )
                )


    fig.update_layout(
    title=map_name,
    title_x=0.5,
    map=dict(
        style="open-street-map",
        center=dict(lat=-15.8750393, lon=-52.3119392),
        zoom=16  # ajuste fino: 12–15 normalmente
    ),
    margin=dict(l=0, r=0, t=40, b=0))
    
    fig.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--map-file", 
        type=str, 
        default="data/barra-do-garcas.pbf", 
        help="Map (.pbf)"
    )
    parser.add_argument(
        "--landmark-file",
        type=str,
        default= "data/bg-landmarks.json",
        help="Landmarks (.json)",
    )
    parser.add_argument(
        "--path-file",
        type=str,
        default= None, #"path.json",
        help="Path to visualize (.json), path should correspond to some map file",
    )
    args = parser.parse_args()

    # Create city_map and populate any relevant landmarks
    bg_map_name = args.map_file.split("/")[-1].split("_")[0]
    bg_city_map = read_map(args.map_file)
    if args.landmark_file is not None:
        print(f"Adding landmarks from {args.landmark_file} to city map...")
        add_landmarks(bg_city_map, args.landmark_file)

    # (Optional) Lê o caminho a ser visualizado do arquivo JSON
    if args.path_file is not None:
        with open(args.path_file) as f:
            data = json.load(f)
            parsed_path = data["path"]
            parsed_waypoint_tags = data["waypoint_tags"]
    else:
        parsed_path = []
        parsed_waypoint_tags = []

    # Roda a visualização
    plot_map(
        city_map=bg_city_map,
        path=parsed_path,
        waypoint_tags=parsed_waypoint_tags,
        map_name=bg_map_name,
    )
