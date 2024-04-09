import xarray as xr

# Open the netCDF file
nc_file = 'ssp1rur2020.nc'
ds = xr.open_dataset(nc_file)

# Print the dataset structure
print(ds)

# Print metadata (attributes)
print(ds.attrs)

# Print variables and their attributes
for var_name in ds.variables:
    print(var_name)
    print(ds[var_name])

# If you're interested in dimensions
print("Dimensions:")
for dim_name, dim in ds.dims.items():
    print(f"{dim_name}: {dim}")

# If you're interested in coordinates
print("Coordinates:")
for coord_name, coord in ds.coords.items():
    print(f"{coord_name}: {coord}")
