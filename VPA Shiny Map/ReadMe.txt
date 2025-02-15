VPA (value per acre) is a concept popularized by the Strong Towns movement (https://www.strongtowns.org/journal/2018/10/19/value-per-acre-analysis-a-how-to-for-beginners). The purpose of this Shiny app is to highlight the VPA of parcels (grouped by block) in the municipalities of Camden County, New Jersey.

All data is taken from the Camden County Open Data Portal, specifically the parcel data collected in 2021.
URL: https://camdencountynj-ccdpw.opendata.arcgis.com/datasets/CCDPW::parcel-data-2021-redacted/about
You will need to download the parcel geometries from the Open Data Portal link above. The data is available as a geojson file. For this app, the geojson file was filtered to only contain columns for OBJECTID, MUNICIPALITY, and geometry.

VPA is calculated by dividing the Net_Value column by the Shape__Area column. Shape__Area is in square feet and must first be divided by 43560 to convert to acres. The data was then grouped by block and the mean VPA was taken.

The .data file avg_vpa_by_objectid contains only two columns: OBJECTID and avg_vpa (per block). The muns.txt file contains the list of all municipalities in the data set.

