import pandas as pd
from urllib.request import urlopen
import json
import folium
import geopandas as gpd
import webbrowser

estados = gpd.read_file('C:/Users/Markus/Documents/Web Projects/PI_3/Pesca Bem/Portal/flaskblog/static/CloroMap/brasil-desemprego-trimestre-2-2022.shp')
estados = gpd.read_file(url_for('static', filename='CloroMap/brasil-desemprego-trimestre-2-2022.shp'))

response = urlopen("http://127.0.0.1:5000/api?SEL=todos")
data_json = json.loads(response.read())

df = pd.DataFrame (data_json, columns = ['conduta','ramo','estado'])

est = df.groupby(['estado']).count()['ramo']
cond_est = df.groupby(['conduta','estado']).count()
bNE = cond_est.query("conduta == 'CNPJ não encontrado nos registros do IBAMA.'")['ramo'].droplevel(0)
bPO = cond_est.query("conduta == 'Possui certificado ambiental.'")['ramo'].droplevel(0)
bNP = cond_est.query("conduta == 'Não possui certificado ambiental.'")['ramo'].droplevel(0)

cons = pd.concat([est,bNE, bPO, bNP], axis=1).reset_index(level=0).fillna(0)
cons.columns=['ESTADO','Total de Empresas','CNPJ não encontrada na base do Ibama','Possui certificado','Não possui certificado']

estados = gpd.GeoDataFrame(estados, geometry='geometry')
estados.crs = 'epsg:4326'
estados = estados.merge(cons, on='ESTADO')

BR_LAT = -14.235
BR_LON = -51.9253

mapa = folium.Map(location=[BR_LAT,BR_LON], control_scale = True, zoom_start=5, tiles='cartodbpositron')

coropletico = folium.Choropleth(
    geo_data=estados,
    data=estados,
    columns=['ESTADO','Total de Empresas','CNPJ não encontrada na base do Ibama','Possui certificado','Não possui certificado'],
    key_on='feature.properties.ESTADO',
    legend_name='Número de Empresas por Estado (grupo das 500 maiores)',
    fill_color = 'YlOrRd'
).add_to(mapa)

coropletico.geojson.add_child(
    folium.features.GeoJsonTooltip(['ESTADO','Total de Empresas','CNPJ não encontrada na base do Ibama','Possui certificado','Não possui certificado'])
)

output_file = "map2.html"
mapa.save(output_file)
webbrowser.open(output_file, new=2) 
