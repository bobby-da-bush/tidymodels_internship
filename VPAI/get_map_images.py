import folium
import gc
import geopandas as gd
import os
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile
import time

path = ".data/Parcel_Data_2021_Redacted.geojson"
gdf = gd.read_file(path)

gdf["Net_Value"] = pd.to_numeric(gdf["Net_Value"], errors='coerce')
gdf["Shape__Area"] = pd.to_numeric(gdf["Shape__Area"], errors='coerce')
gdf["VPA"] = gdf["Net_Value"] / (gdf["Shape__Area"] / 43560) # sq.ft. per acre

gdf = gdf[["OBJECTID", "VPA", "geometry"]]
gdf = gdf.dropna(subset=["VPA"])
gdf["VPA"] = gdf["VPA"].astype(int)

def generate_parcel_maps(gdf, output_dir, buffer_miles=1):
    """
    Generate map images for each parcel in a GeoDataFrame.
    
    Parameters:
    -----------
    gdf : GeoDataFrame
        Input parcel data with geometry column
    output_dir : str
        Directory to save the map images
    buffer_miles : float
        Buffer distance in miles around the centroid
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Set up Chrome options for headless browsing
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    
    # Initialize webdriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # Calculate buffer in degrees (approximate)
    # 1 degree of latitude ≈ 69 miles
    buffer_degrees = buffer_miles / 69
    
    temp_dir = tempfile.mkdtemp()

    for idx, row in gdf.iterrows():
        try:
            # Get centroid
            centroid = row.geometry.centroid
            
            # Create map centered on parcel
            m = folium.Map(
                location=[centroid.y, centroid.x],
                zoom_start=16,
                tiles='OpenStreetMap'
            )
            
            # Calculate bounds
            bounds = [
                [centroid.y - buffer_degrees, centroid.x - buffer_degrees],
                [centroid.y + buffer_degrees, centroid.x + buffer_degrees]
            ]
            m.fit_bounds(bounds)
            
            # Create a unique temporary file path
            temp_html = os.path.join(temp_dir, f'map_{idx}.html')
            
            try:
                # Save map to HTML file
                m.save(temp_html)
                
                # Use selenium to capture screenshot
                driver.get(f'file:///{temp_html}')
                time.sleep(2)  # Increased wait time for map to load
                
                # Save screenshot
                output_file = os.path.join(output_dir, f'{row["OBJECTID"]}_{row["VPA"]}.png')
                driver.save_screenshot(output_file)
                
            finally:
                # Close any open file handles
                driver.execute_script("window.onbeforeunload = null;")
                
                # Try to delete the temporary file
                try:
                    if os.path.exists(temp_html):
                        driver.get('about:blank')  # Navigate away from the file
                        time.sleep(0.5)  # Give browser time to release the file
                        os.remove(temp_html)
                except Exception as e:
                    print(f"Warning: Could not delete temporary file {temp_html}: {str(e)}")
            
            # Force garbage collection
            gc.collect()
            
            print(f"Generated map for parcel {idx}")
            
        except Exception as e:
            print(f"Error processing parcel {idx}: {str(e)}")
    
    # Clean up
    driver.quit()
    
    # Final cleanup of temp directory
    try:
        for file in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, file))
            except:
                pass
        os.rmdir(temp_dir)
    except:
        print(f"Warning: Could not fully clean up temporary directory {temp_dir}")

gdf_shuffled = gdf.sample(frac=1, random_state=42).reset_index(drop=True)
output_directory = '.data/parcel_maps'
generate_parcel_maps(gdf_shuffled, output_directory)