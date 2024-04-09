import geopandas as gpd
import xarray as xr
import numpy as np

# Step 1: Read the county shapefile into a GeoDataFrame
county_shapefile_path = 'county.shp'  # Adjust the path to your county shapefile
gdf_counties = gpd.read_file(county_shapefile_path)

# Step 2: Read the population projection data from the NetCDF file
nc_file = 'ssp5rur2020.nc'  # Adjust the path to your NetCDF file
ds = xr.open_dataset(nc_file)
population_projection_variable = ds['ssp5rur2020']  # Adjust the variable name if needed

# Step 3: Function to find nearest latitude and longitude indices in NetCDF data
def find_nearest_index(lon, lat, lon_values, lat_values):
    lon_index = np.abs(lon_values - lon).argmin()
    lat_index = np.abs(lat_values - lat).argmin()
    return lon_index, lat_index

# Step 4: Loop through each county and extract population projection for 2030
population_projections = []
shapefile_latitudes = []
shapefile_longitudes = []
nc_latitudes = []
nc_longitudes = []
for index, row in gdf_counties.iterrows():
    lon, lat = row.geometry.centroid.x, row.geometry.centroid.y
    lon_index, lat_index = find_nearest_index(lon, lat, population_projection_variable.lon.values, population_projection_variable.lat.values)
    population_projection = population_projection_variable[lat_index, lon_index].values.item()
    population_projections.append(population_projection)
    
    shapefile_latitudes.append(lat)
    shapefile_longitudes.append(lon)
    nc_latitudes.append(population_projection_variable.lat.values[lat_index])
    nc_longitudes.append(population_projection_variable.lon.values[lon_index])

# Step 5: Assign population projections, latitude, and longitude to counties
gdf_counties['population_projection_2020'] = population_projections
gdf_counties['shapefile_latitude'] = shapefile_latitudes
gdf_counties['shapefile_longitude'] = shapefile_longitudes
gdf_counties['nc_latitude'] = nc_latitudes
gdf_counties['nc_longitude'] = nc_longitudes

# Step 6: Save the GeoDataFrame with population projections, latitude, and longitude to a CSV file
output_csv = 'county_population_projections_rural_2020.csv'
gdf_counties[['STATE', 'COUNTYNAME', 'shapefile_latitude', 'shapefile_longitude', 'nc_latitude', 'nc_longitude', 'population_projection_2020']].to_csv(output_csv, index=False)

print(f"County-specific population projections with latitude and longitude for 2030 saved to '{output_csv}'.")
