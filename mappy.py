# Author: Cameron F. Abrams, <cfa22@drexel.edu>
"""
Plot the US State boundaries for the Northeast/Mid-Atlantic 
region and indicate locations of all NEMA CHE institutions

Required input files:
data/NEMA CHE Chairs.xlsx -- database of each school that must include
latitude and longitude
data/cb_2018_us_state_500k.shp -- the shapefile for the US (from census bureau)

"""
import geopandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

my_params={"axes.spines.right":False,"axes.spines.top":False,"axes.spines.bottom":False,"axes.spines.left":False,"ytick.left":False}
sns.set_theme(style="white",rc=my_params)
institutions=pd.read_excel('data/NEMA CHE Chairs.xlsx',header=0,index_col=None,nrows=48)
gdf=geopandas.GeoDataFrame(institutions,geometry=geopandas.points_from_xy(institutions.Longitude,institutions.Latitude),crs='EPSG:4326')
states=geopandas.read_file(r'data\cb_2018_us_state_500k.shp')
fig,ax=plt.subplots(figsize=(8,16))
ax.set_xlim([-81,-67])
ax.set_ylim([37.5,48])
ax.set_xticks([],[])
ax.set_yticks([],[])
institutions.fillna(0,inplace=True)
alphas=(1+institutions['Data survey?'])/2.0
markersizes=alphas*50
colors=[]
markers=[]
for x in institutions['Data survey?']:
    if x:
        colors.append('green')
        markers.append('*')
    else:
        colors.append('grey')
        markers.append('o')
gdf.plot(ax=ax,marker='*',markersize=markersizes,alpha=1,color=colors)
states.boundary.plot(ax=ax,color='black')
plt.savefig(f'graphics/states.png',bbox_inches='tight')


