'''functions to get osm ids from points'''

import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point, LineString


def get_osm_ids_from_points(points, bbox_geojson=None):
    # Define the custom filter for the types of roads you're interested in
    custom_filter = (
        '["highway"~"motorway|trunk|primary|secondary|tertiary|'
        'unclassified|residential|service|motorway_link|trunk_link|'
        'primary_link|secondary_link|tertiary_link|living_street|'
        'road|track"]'
    )

    # If a bounding box is provided, create a graph from the polygon
    if bbox_geojson:
        polygon_gdf = gpd.read_file(bbox_geojson)
        polygon_gdf = polygon_gdf.to_crs('EPSG:4326')
        polygon = polygon_gdf.geometry.iloc[0]

        # Create a graph from the bounding box
        G = ox.graph_from_polygon(polygon, network_type='drive', custom_filter=custom_filter)

        # Extract x and y coordinates from points
        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]
    else:
        # Extract x and y coordinates from points
        x_coords = [point.x for point in points]
        y_coords = [point.y for point in points]

        # Calculate the bounding box (min longitude, min latitude, max longitude, max latitude)
        min_lon, min_lat = min(x_coords), min(y_coords)
        max_lon, max_lat = max(x_coords), max(y_coords)

        # Create a graph from the bounding box
        G = ox.graph_from_bbox(north=max_lat, south=min_lat, east=max_lon, west=min_lon, network_type='drive', custom_filter=custom_filter)

    # Find the nearest edge to each point
    nearest_edges = ox.distance.nearest_edges(G, X=x_coords, Y=y_coords)

    # Pre-calculate and store the geometries and OSM IDs for the edges
    edge_data = {(u, v, key): (G[u][v][key].get('geometry'), G[u][v][key].get('osmid'))
                 for u, v, key in nearest_edges}

    points_with_osmid = []
    for point, (u, v, key) in zip(points, nearest_edges):
        # Retrieve pre-calculated geometry and OSM IDs
        geometry, osmids = edge_data[(u, v, key)]

        if isinstance(osmids, list) and geometry:
            # If there are multiple OSM IDs, calculate the distance to each corresponding line
            line = LineString(list(geometry.coords))
            distances = [(osmid, point.distance(line)) for osmid in osmids]

            # Sort by distance and get the closest OSM ID
            distances.sort(key=lambda x: x[1])
            closest_osmid = distances[0][0] if distances else None
        else:
            # If there's only one OSM ID or no geometry, use it directly
            closest_osmid = osmids

        # Append the point and the closest OSM ID as a tuple
        points_with_osmid.append((point, closest_osmid))

    return points_with_osmid

# Usage example:
# my_points = [Point(1, 1), Point(2, 2), Point(3, 3)]
# osm_ids = get_osm_ids_from_points(my_points, bbox_geojson='my_polygon.geojson')
# print(osm_ids)
