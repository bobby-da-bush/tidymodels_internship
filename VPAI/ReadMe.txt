VPA (value per acre) is a concept popularized by the Strong Towns movement (https://www.strongtowns.org/journal/2018/10/19/value-per-acre-analysis-a-how-to-for-beginners). The purpose of this project is to showcase the fastai package to see if we can create a model that can predict the VPA of a parcel based on the map image.

All data is taken from the Camden County Open Data Portal, specifically the parcel data collected in 2021.
URL: https://camdencountynj-ccdpw.opendata.arcgis.com/datasets/CCDPW::parcel-data-2021-redacted/about

VPA is calculated by dividing the Net_Value column by the Shape__Area column. Shape__Area is in square feet and must first be divided by 43560 to convert to acres.
 