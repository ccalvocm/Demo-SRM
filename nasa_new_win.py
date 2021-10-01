#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:07:55 2021
@author: faarrosp
"""
import os
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
from nasa_aux_functions import List_Files, Exists, Enforce_List, Identify, Grab_Data_Info


def Prepare_MODIS(Package,Year):

    Year=str(Year) # OK
    rawmodis = os.path.abspath(os.path.join(Package,Year))  # OK
    readymodis = os.path.abspath(os.path.join(rawmodis,'prm')) # OK
    reprojmodis = os.path.abspath(os.path.join(readymodis,'reproj'))
    # reference_file=os.path.join(Package,'Ejecutables','Reference','Elev_Zones.tif') # OK raster de cuenca

    if not os.path.exists(readymodis): # OK
        os.makedirs(readymodis) # OK
    
    if not os.path.exists(reprojmodis): # OK
        os.makedirs(reprojmodis) # OK
        
    # prjpath = '"' + prjpath + '"'
    # print(prjpath)
    # Extract all the HDFs in the specified year for the given basin.
    hdf_list=List_Files(False,rawmodis,['.hdf'],['.xml','.ovr','.aux'],False) # OK
    Extract_MODIS_HDF(hdf_list,[0],['NDSI_Snow_Cover'],rawmodis,False) # OK
    
    # Mosaic all possible MODIS tiles together.  
    mosaic_list=List_Files(False,rawmodis,['.tif','NDSI_Snow_Cover'],['.xml','.ovr','.aux'],False) # OK
    Mosaic_MODIS(mosaic_list, '8_BIT_UNSIGNED', '1', 'LAST','FIRST',readymodis,False) # OK

    # reprojects all files to the desired projection.
    # cambie readymodis por rawmodis
    project_list=List_Files(False,readymodis,[Year,'.tif'],['.xml','.ovr','.aux'],False)
    Project_Filelist(project_list,reprojmodis,False,False,Quiet=False)
    
    return


def Extract_MODIS_HDF(filelist,layerlist,layernames,outdir,Quiet=False):
#--------------------------------------------------------------------------------------
# Function extracts tifs from HDFs such as MODIS data.
#
# inputs:
#   filelist    list of '.hdf' files from which data should be extracted
#   layerlist   list of layer numbers to pull out as individual tifs should be integers
#               such as [0,4] for the 0th and 4th layer respectively.
#   layernames  list of layer names to put more descriptive names to each layer
#   outdir      directory to which tif files should be saved
#               if outdir is left as 'False', files are saved in the same directory as
#               the input file was found.
#--------------------------------------------------------------------------------------

    # import modules
    import sys, os, time # OK

    # Set up initial arcpy modules, workspace, and parameters, and sanitize inputs.
    # Check_Spatial_Extension()
    # arcpy.env.overwriteOutput = True

    # enforce lists for iteration purposes
    filelist=Enforce_List(filelist) # OK
    layerlist=Enforce_List(layerlist) # OK
    layernames=Enforce_List(layernames) # OK
    
    # ignore user input layernames if they are invalid, but print warnings
    if layernames and not len(layernames)==len(layerlist): # OK
        print('{Extract_MODIS_HDF} layernames must be the same length as layerlist!') # OK
        print('{Extract_MODIS_HDF} ommiting user defined layernames!') # OK
        layernames=False # OK

    # create empty list to add failed file names into
    failed=[] # OK

    print('{Extract_MODIS_HDF} Beginning to extract!') # OK
    
    # cambiar de directorio
    folder = os.path.split(filelist[0])[0]
    os.chdir(folder)
    
    # iterate through every file in the input filelist
    for infile in filelist: # ok
        # pull the filename and path apart 
        path,name = os.path.split(infile) # OK
        # arcpy.env.workspace = path

        for i in range(len(layerlist)):
            layer=layerlist[i]
            
            # specify the layer names.
            if layernames:
                layername=layernames[i]
            else:
                layername=str(layer).zfill(3)

            # use the input output directory if the user input one, otherwise build one  
            if not os.path.exists(outdir):
                os.makedirs(outdir)
                
            # outname=os.path.join(outdir,name[:-4] +'_'+ layername +'.tif')
            outname=os.path.join(name[:-4] +'_'+ layername +'.tif')
            
            # print(outname)
            # perform the extracting and projection definition
            try:
                # extract the subdataset
                ExtractSubDataset_management(infile, outname, str(layer))
                
                # define the projection as the MODIS Sinusoidal
                
                ######## PENDIENTE, DESCOMENTAR CUANDO TERMINE LA PRUEBA
                # Define_MODIS_Projection(outname)
                
                
                if not Quiet:
                    # print('{Extract_MODIS_HDF} Extracted ' + outname)
                    pass
            except:
                if not Quiet:
                    print('{Extract_MODIS_HDF} Failed extract '+ outname + ' from ' + infile)
                failed.append(infile)
    
                
    
    
    if not Quiet:print('{Extract_MODIS_HDF} Finished!')
    return(failed)
        
def ExtractSubDataset_management(infile, outname, layer):
    # print('inside')
    # print(infile)
    # print(layer)
    os_command = 'gdal_translate -of GTiff '
    folder = os.path.abspath(os.path.split(infile)[0])
    os.chdir(folder)
    name = os.path.split(infile)[1]
    file_prefix = 'HDF4_EOS:EOS_GRID:'
    suffix = ':MOD_Grid_Snow_500m:NDSI_Snow_Cover'
    
    outname = os.path.split(outname)[1]
    
    final_name = file_prefix + '"' + name + '"' + suffix
    # final_name = os.path.join(folder,final_name)
    # final_name = "'" + final_name + "'"
    # print(final_name)
    # 'HDF4_EOS:EOS_GRID:"MOD13C2.A2001001.005.2007078152825.hdf":MOD_Grid_monthly_CMG_VI:CMG 0.05 Deg Monthly NDVI'
    os_command = 'gdal_translate -of GTiff '
    os_command = os_command + final_name + ' ' + "" + outname + ""
    print(os_command)
    os.system(os_command)


def Mosaic_MODIS(filelist, pixel_type, bands, m_method, m_colormap, outdir=False,Quiet=False):
#--------------------------------------------------------------------------------------
# This script will find and mosaic all MODIS tiles groups with different time names in a
# directory. It will automatically identify the date ranges in the MODIS filenames and
# iterate through the entire range while skipping dates for which there are not at least
# two tiles. Users should be mindful of file suffixes from previous processing.
#
# This script centers around the 'arcpy.MosaicToNewRaster_management' tool
# [http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//001700000098000000]
#
# Inputs:
#   indir           the directory containing MODIS data, will search recursively.
#   pixel_type      exactly as the input for the MosaicToNewRaster_management tool
#   bands           exactly as the input for the MosaicToNewRaster_management tool
#   m_method        exactly as the input for the MosaicToNewRaster_management tool
#   m_colormap      exactly as the input for the MosaicToNewRaster_management tool
#   contains        additional search criteria for deciding which MODIS tiles to mosaic
#                   This is required when the same directory contains multiple extracted
#                   layers from the MODIS HDF file. (unless the user decides to treat
#                   the multiple layers as bands in the same image stack)
#   outdir          the directory to save output files to. If none is specified, a
#                   default directory will be created as '[indir]_Mosaicked'
#   Quiet           True to silence output, defaults to False.
#
# Outputs:
#   failed          mosaic opperations which failed due to one or more missing tiles
#
# Example usage:
#
#       import ND
#       indir=      r'C:\Users\jwely\Desktop\Shortcuts\Testbed\Test tiles\MODIS LST\2013\day'
#       pixel_type= "16_BIT_UNSIGNED"
#       bands=      "1"
#       m_method=   "LAST"
#       m_colormap= "FIRST"
#
#       ND.Mosaic_MODIS_Dir(filelist,pixel_type,bands,m_method,m_colormap,'day')
#--------------------------------------------------------------------------------------
    # typically unchanged parameters of raster dataset. Change at will.
    coordinatesys="#"
    cellsize="#"

    # import modules
    import sys, os, time

    # Set up initial arcpy modules, workspace, and parameters, and sanitize inputs.
    # Check_Spatial_Extension()
    # arcpy.env.overwriteOutput = True
    if outdir: OUT=outdir

    # initialize empty lists for tracking
    mosaiclist=[]
    yearlist=[]
    daylist=[]
    productlist=[]
    tilelist=[]
    failed=[]

    # grab info from all the files left in the filelist.
    for item in filelist:
        info=Grab_Data_Info(item,False,True)
        yearlist.append(int(info.year))
        daylist.append(int(info.j_day))

        # find all tiles being represented
        if info.tile not in tilelist:
            tilelist.append(info.tile)
            
        # find all MODIS products existing
        if info.product not in productlist:
            productlist.append(info.product)
            
    # define the range of years and days to look for
    years=range(min(yearlist),max(yearlist)+1)
    days=range(min(daylist),max(daylist)+1)

    # print some status updates to the screen
    if not Quiet:
        print('{Mosaic_MODIS} Found tiles : ' + str(tilelist))
        print('{Mosaic_MODIS} Found tiles from years: ' + str(years))
        print('{Mosaic_MODIS} Found tiles from days:  ' + str(days))
        print('{Mosaic_MODIS} Found tiles from product: ' + str(productlist))
    #.....................................................................................
    # now that we know what to look for, lets go back through and mosaic everything
    for product in productlist:
        for year in years:
            for day in days:

                # build the search criteria
                search=[(product +'.A'+ str(year)+str(day).zfill(3))]
                
                # find files meeting the criteria and sanitize list from accidental metadata inclusions
                for filename in filelist:
                    if all(x in filename for x in ['.tif']+search):
                        if not any(x in filename for x in ['.aux','.xml','.ovr','mosaic']):
                            mosaiclist.append(filename)
                

                # only continue with the mosaic if more than one file was found!
                if len(mosaiclist)>1:
                
                    # if user did not specify an outdir, make folder next to first mosaic file
                    if not outdir:
                        head,tail=os.path.split(mosaiclist[0])
                        OUT=os.path.join(head,'Mosaicked')

                    # make the output directory if it doesnt exist already    
                    if not os.path.isdir(OUT):
                        os.makedirs(OUT)

                    # grab suffix from input files for better naming of output files
                    info=Grab_Data_Info(mosaiclist[0],False,True)
                    suffix=info.suffix.split('_')[1:]
                    
                    # define the output name based on input criteria
                    path,filename= os.path.split(mosaiclist[0])
                    outname = '.'.join(search+['mosaic'])
                    outname = '_'.join([outname] +suffix)
                    
                    # perform the mosaic!
                    try:
                        # MosaicToNewRaster_management(mosaiclist,OUT,\
                        #     outname,coordinatesys,pixel_type,cellsize,bands,\
                        #     m_method,m_colormap)
                        MosaicToNewRaster_management(mosaiclist,OUT,outname)
                           
                        # make sure the mosaic list is empty!
                        if not Quiet: print(outname +' mosaciked!')
                        
                    except:
                        if not Quiet: print('{Mosaic_MODIS} Failed to mosaic files! ' + outname)
                        failed=failed+mosaiclist
                        
                # do not attempt a mosaic if only one tile on given day exists!    
                elif len(mosaiclist)==1:
                    if not Quiet:
                        print('{Mosaic_MODIS} More than one file is required for mosaicing!: '
                              + str(search))
                    failed=failed+mosaiclist

                # delete the list of search parameters for this mosaic operation
                del search[:]
                del mosaiclist[:]

                    
    if not Quiet:print('{Mosaic_MODIS} Finished!')
    return(failed)



def MosaicToNewRaster_management(mosaiclist,OUT,outname):
    src_files_to_mosaic = []
    print(os.path.join(OUT,outname))
    for fp in mosaiclist:
        src = rasterio.open(fp)
        src_files_to_mosaic.append(src)
        
    mosaic, out_trans = merge(src_files_to_mosaic)
    out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                      "height": mosaic.shape[1],
                      "width": mosaic.shape[2],
                      "transform": out_trans})
    out_fp = os.path.join(OUT,outname)
    with rasterio.open(out_fp,'w', **out_meta) as dest:
        dest.write(mosaic)
    

def Project_Filelist(filelist,outdir=False,resampling_type=False,cell_size=False,Quiet=False):

    import os

    # sanitize inputs and create directories
    # Exists(reference_file)
    filelist=Enforce_List(filelist)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    
    # grab data about the spatial reference of the reference file. (prj or otherwise)
    # if reference_file[-3:]=='prj':
    #     Spatial_Reference=arcpy.SpatialReference(Spatial_Reference)
    # else:
    #     Spatial_Reference=arcpy.Describe(reference_file).spatialReference
        
    # # determine wether coordinate system is projected or geographic and print info
    # if Spatial_Reference.type=='Projected':
    #     if not Quiet:
    #         print('{Project_Filelist} Found ['+ Spatial_Reference.PCSName +
    #                 '] Projected coordinate system')
    # else:
    #     if not Quiet:
    #         print('{Project_Filelist} Found ['+ Spatial_Reference.GCSName +
    #                 '] Geographic coordinate system')

    # begin projecting each file in the filelist
    for filename in filelist:

        # grab info for the output name
        head,tail=os.path.split(filename)
        filename = '"' + filename + '"'
        # print(filename)

        # set the workspace to be right where the files are.
        # arcpy.env.workspace = head
        
        # removes the file extention from the end without bothering other '.' characters
        ext=tail.split('.')[-1]
        tail='.'.join(tail.split('.')[:-1])
        
        command = ' '.join(['gdalwarp',
                            '-t_srs EPSG:32719']) 

        # assemble the output filepath, with user input 'outdir' if applicable
        if outdir: 
            outname = os.path.join(outdir,tail + '_p.'+ext)
            
            
        else: 
            outname=os.path.join(head,tail + '_p.'+ext)
            
    
        # Perform the projection!...................................................
        try:
            outname = '"' + outname + '"'
            command = command + ' ' + filename + ' ' + outname
            os.system(command)
            # use ProjectRaster_management for files with extensions listed here
            # if any( ext==filename[-3:] for ext in ['bil','bip','bmp','bsq','dat',
            #         'gif','img','jpg','jp2','png','tif']):
            #     if resampling_type:
            #         if cell_size:
            #             arcpy.ProjectRaster_management(filename,outname,Spatial_Reference,
            #                     resampling_type,cell_size)
            #         else:
            #             arcpy.ProjectRaster_management(filename,outname,Spatial_Reference,
            #                     resampling_type)
            #     else:
            #         arcpy.ProjectRaster_management(filename,outname,Spatial_Reference)
                    
            # # otherwise, use Project_management for featureclasses and featurelayers
            # else:
            #     arcpy.Project_management(filename,outname,Spatial_Reference)

            # print a status update    
            if not Quiet: print('{Project_Filelist} Wrote projected file to ' + outname)
            
        except:
            if not Quiet: print('{Project_Filelist} Failed to project file ' +filename)
    
    # return(Spatial_Reference)



    
    
####################### INICIAR PREPARE MODIS ################################


# ''' VARIABLES
# Package: Ruta de carpeta principal
# Year: año de analisis
# La idea es que las carpetas queden asi:
#     /MODIS2021
#         /Datos
#             /NASA_Datos
#                 /MODIS
#                     /<año> por ejemplo:
#                     /2019
#                     /2020
#                     /2021
#                         /prm (en esta carpeta iran los mosaicos)
#                         /MOD10A1.xxxxxx.xxxxxx.xxxx.hdf (imagen MODIS cruda)
#                         /Mod10A1.xxxxxx.xxxxxx.xxxy.hdf
# '''
    


# Package = os.path.join('/','home','faarrosp','Insync', 'farrospide@ciren.cl',
#                        'OneDrive Biz - Shared', 'AOHIA_ZC','Etapa 3',
#                        'Scripts','MODIS2021')

# Year = '2021'

# prjpath = os.path.join('/','home','faarrosp','Insync', 'farrospide@ciren.cl',
#                        'OneDrive Biz - Shared', 'AOHIA_ZC','Etapa 3',
#                        'Scripts','MODIS2021','SIN.prj')

# Prepare_MODIS(Package, Year, prjpath)