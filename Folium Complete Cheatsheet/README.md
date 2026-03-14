# Folium Cheatsheet Concepts

This notebook covers the following Folium concepts and workflows:

1. Folium setup and imports (`folium`, `pandas`).
2. Creating a base map with `folium.Map`.
3. Setting map center and `zoom_start`.
4. Saving interactive maps to HTML (`.save()`).
5. Loading external geospatial/CSV data with `pandas.read_csv`.
6. Building choropleth maps with `folium.Choropleth`.
7. Choropleth styling options (`fill_color`, `fill_opacity`, `line_opacity`, `legend_name`, `key_on`).
8. Adding standard markers with `folium.Marker`.
9. Marker popups and tooltips.
10. Using alternate tile layers/basemaps (e.g., `CartoDB positron`, `openstreetmap`).
11. Using icon customization in markers via `folium.Icon`.
12. Using polygon markers with `folium.RegularPolygonMarker`.
13. Configuring polygon marker shape (`number_of_sides`) and size (`radius`).
14. Drawing circles with `folium.Circle`.
15. Drawing routes/paths with `folium.PolyLine`.
16. Creating multiple maps in one notebook (`my_map`, `kol`, `kol2`, `pak`, `india2`).
17. Plotting multiple locations from tabular data using loops.
18. Making notebook data-loading robust with a fallback dataset when local files are missing.
19. Basic multi-region examples (USA choropleth, Boulder markers, Kolkata points, Pakistan polyline, India state markers).

