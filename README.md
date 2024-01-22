[//]: # (FILEPATH: /Users/amirbabaei/Projs/osm-id-lookup/README.md)

## Overview
This Python code allows you to interactively retrieve OpenStreetMap (OSM) IDs for given points in road networks. It utilizes the OpenStreetMap and GeoPandas libraries to create a custom filter for road types and find the nearest OSM IDs for each point, considering a bounding box if provided. The resulting OSM IDs are returned as a list of tuples containing the point and its closest OSM ID.

## Usage
1. Clone the repository to your local machine:
    ```
    git clone https://github.com/yourusername/osm-id-lookup.git
    ```
2. Navigate to the project directory:
    ```
    cd osm-id-lookup
    ```
3. Install the required Python libraries if you haven't already:
    ```
    pip install openai openstreetmap geojson
    ```
4. Use the `get_osm_ids_from_points` function in your Python code to perform OSM ID lookups for points:
    ```python
    from osm_id_lookup import get_osm_ids_from_points

    # Define your points (list of Shapely Point objects)
    points = [...]

    # Call the function with your points
    osm_ids = get_osm_ids_from_points(points)

    # Print the results
    print(osm_ids)
    ```
5. Feel free to contribute to this project by creating issues, suggesting improvements, or submitting pull requests.

## License
This code is licensed under the GNU General Public V3 License.

## Acknowledgments
This project was inspired by the need to efficiently retrieve OSM IDs for points in road networks. It makes use of popular Python libraries for geospatial analysis and data manipulation.

Enjoy exploring and using this interactive OSM ID lookup tool for your geospatial projects!