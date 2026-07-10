# %%
import rioxarray
import matplotlib.pyplot as plt
import numpy as np
import pandas
import shapely
import stackstac
import dask.array as da
from pystac_client import Client

# %% [markdown]
# ##  1: Develop Function(s) to Plot NDWI Time Series

# %%
"""This is the main function which is supposed to calculate mean ndwi
from January 1st 2020 to December 31st 2024"""

def main(bbox, starttime, endtime, filter_clouds):
    
    """This function searches for and reteives items from STAC API"""

    def search_item(starttime, endtime):
        
        api_url = "https://earth-search.aws.element84.com/v1"
        client = Client.open(api_url)
        item_collection = client.search(collections=["sentinel-2-l2a"],
                                        bbox=bbox,
                                        datetime= f'{starttime}/{endtime}',
                                        max_items=500).item_collection()
        return item_collection
        
    def get_xarray_object(items, assets, bbox):  
        
        """This function returns stacked scenes from STAC API with specific bands and bounding box"""
        
        stack = stackstac.stack(items, 
                                assets=assets, 
                                bounds_latlon=bbox, 
                                chunksize=4096, 
                                epsg=4326,
                                rescale=False,
                                fill_value=np.float32(np.nan)
                                )
        stack_bands = stack.assign_coords(band=["green", "nir", "scl"])
        return stack_bands
            
    def compute_mean_ndwi(stack_bands, filter_clouds):
        
        """This function computes the mean NDWI for each scene and returns its output"""
                
        green = stack_bands.sel(band="green")
        nir = stack_bands.sel(band="nir") 
        with np.errstate(divide='ignore', invalid='ignore'):
            ndwi = (green - nir) / (green + nir)
        if filter_clouds == True:
            scl = stack_bands.sel(band="scl")
            valid_mask = ~scl.isin([3, 8, 9, 10])
            ndwi = ndwi.where(valid_mask)
        mean_ndwi_scenes = ndwi.mean(dim=["x","y"], skipna=True)                    
        return mean_ndwi_scenes
    
    def plot_timeseries(mean_ndwi_scenes):
        
        """This function plots a time series of the mean NDWI of the mean scenes from January 2020 to December 2024"""

        mean_ndwi_scenes.name = "ndwi"
        df = mean_ndwi_scenes.to_dataframe().reset_index()        
        plt.figure(figsize=(12,8))
        plt.plot(df["time"], df["ndwi"], linestyle="-", color="blue", label="Mean NDWI")
        plt.grid(alpha=0.5)
        plt.title('Mean NDWI from January 1, 2020 to December 31, 2024', fontsize=10)
        plt.legend(loc="upper right", fontsize=10)
        plt.xlabel('Time', fontsize=10)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.ylabel('NDWI', fontsize=10)
        plt.show()
        plt.close()
        return None
    
    items = search_item(starttime, endtime)
    xarray_object = get_xarray_object(items, assets=["green", "nir", "scl"], bbox = bbox)
    mean_ndwi = compute_mean_ndwi(xarray_object, filter_clouds)
    plot_timeseries(mean_ndwi)
    
    return None



# %%
