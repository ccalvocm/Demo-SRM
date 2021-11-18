import ee
import geemap
import os


dic_cuencas = {'01_Maipo': ['01_RMELA', '02_RMEEM'],
               '02_Rapel': ['01_RCEPTDC', '02_RCEHLN', '03_RTBLB'],
               '03_Mataquito': ['01_RTDJCC', '02_RCEJCP', '03_RPEJCC'],
               '04_Maule': ['01_RMEA']}
dic_subcuencas = {'01_RMELA': 'Rio Mapocho en Los Almendros',
                  '02_RMEEM': 'Rio Maipo en El Manzano',
                  '01_RCEPTDC': 'Rio Cachapoal en Puente Termas de Cauquenes',
                  '02_RCEHLN': 'Rio Claro en Hacienda Las Nieves',
                  '03_RTBLB': 'Rio Tinguiririca bajo Los Briones',
                  '01_RTDJCC': 'Rio Teno despues de junta con Claro',
                  '02_RCEJCP': 'Rio Colorado en junta con Palos',
                  '03_RPEJCC': 'Rio Palos en junta con Colorado',
                  '01_RMEA': 'Rio Maule en Armerillo'}

def create_dataset_map(dataset_str, outpath):
    ee.Initialize()

    Map = geemap.Map()
    geo_list = []

    for key in list(dic_cuencas.keys())[1:2]:
        for cuenca in dic_cuencas[key]:
            shp_path = os.path.join(key, cuenca, 'Shapes', 'cuenca_4326.shp')
            geo = geemap.shp_to_ee(shp_path).geometry()
            geo_list.append(geo)

    macrocuencas = ee.FeatureCollection(geo_list)
    macrocuencas = macrocuencas.geometry()

    CHIRPS = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    CHIRPS = CHIRPS.select('precipitation').filterBounds(ee.Geometry(macrocuencas))
    CHIRPS = CHIRPS.filterDate('2021-07-01', '2021-07-30').max().clip(macrocuencas)
    precipParams = {
        'min': -0.4,
        'max': 29.55,
        'opacity': 0.6,
        'palette': ['white', 'green', 'blue']
    }

    Map.centerObject(macrocuencas, zoom=8)
    Map.addLayer(macrocuencas,opacity=0.5)
    Map.addLayer(CHIRPS, name='Precipitacion', opacity=0.7, vis_params=precipParams)
    Map.add_colorbar(vis_params=precipParams, layer_name='Precipitacion',
                     orientation="vertical", transparent_bg=True, discrete=True)
    Map.to_html(outfile=outpath)


if __name__ == '__main__':
    create_dataset_map('a', 'test.html')