#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:15:44 2021

@author: faarrosp
"""

def List_Files(recursive,Dir,Contains,DoesNotContain,Quiet=False):
#======================================================================================
# This function sifts through a directory and returns a list of filepaths for all files
# meeting the input criteria. Useful for discriminatory iteration or recursive searches.
# Could be used to find all tiles with a given datestring such as 'MOD11A1.A2012', or
# perhaps all Band 4 tiles from a directory containing landsat 8 data.
#
# Inputs:
#       recursive       'True' if search should search subfolders within the directory
#                       'False'if search should ignore files in subfolders.
#       Dir             The directory in which to search for files meeting the criteria
#       Contains        search criteria to limit returned file list. File names must
#                       contain parameters listed here. If no criteria exists use 'False'
#       DoesNotContain  search criteria to limit returned file list. File names must not
#                       contain parameters listed here. If no criteria exists use 'False'
#       Quiet           Set Quiet to 'True' if you don't want anything printed to screen.
#                       Defaults to 'False' if left blank.
# Outputs:
#       filelist        An array of full filepaths meeting the criteria.
#
# Example Usage:
#       import ND
#       filelist=ND.List_Files(True,r'E:\Landsat7','B1',['gz','xml','ovr'])
#
#       The above statement will find all the Band 1 tifs in a landsat data directory
#       without including the associated metadata and uncompressed gz files.
#       "filelist" variable will contain full filepaths to all files found.
#--------------------------------------------------------------------------------------

    # import modules and set up empty lists
    import os,glob,datetime
    filelist=[]
    templist=[]

    # ensure input directory actually exists
    if not Exists(Dir): return(False) # OK

    # Ensure single strings are in list format for the loops below
    if Contains: Contains = Enforce_List(Contains) # OK
    if DoesNotContain:
        DoesNotContain = Enforce_List(DoesNotContain)
        DoesNotContain.append('sr.lock')    # make sure lock files don't get counted
    else:
        DoesNotContain=['sr.lock']          # make sure lock files don't get counted
    
    # use os.walk commands to search through whole directory if recursive
    if recursive:
        for root,dirs,files in os.walk(Dir):
            for basename in files:
                filename = os.path.join(root,basename)
                
                # if both conditions exist, add items which meet Contains criteria
                if Contains and DoesNotContain:
                    for i in Contains:
                        if i in basename:
                            templist.append(filename)
                    # if the entire array of 'Contains' terms were found, add to list
                    if len(templist)==len(Contains):
                        filelist.append(filename)
                    templist=[]
                        
                    # remove items which do not meet the DoesNotcontain criteria
                    for j in DoesNotContain:
                        if j in basename:
                            try: filelist.remove(filename)
                            except: pass
                                    
                # If both conditions do not exist (one is false)                        
                else:
                    # determine if a file is good. if it is, add it to the list.
                    if Contains:
                        for i in Contains:
                            if i in basename:
                                templist.append(filename)
                        # if the entire array of 'Contains' terms were found, add to list
                        if len(templist)==len(Contains):
                            filelist.append(filename)
                        templist=[]

                    # add all files to the list, then remove the bad ones.        
                    if DoesNotContain:
                        filelist.append(filename)
                        for j in DoesNotContain:
                            if j in basename:
                                try: filelist.remove(filename)
                                except: pass
                                        
                # if neither condition exists
                    if not Contains and not DoesNotContain:
                        filelist.append(filename)

    # use a simple listdir if file list if recursive is False
    else:
        # add files that meet all contain critiera
        for basename in os.listdir(Dir):
            filename= os.path.join(Dir,basename)
            if Contains:
                for i in Contains:
                    if i in basename:
                        templist.append(filename)
                        
                # if the entire array of 'Contains' terms were found, add to list
                if len(templist)==len(Contains):
                    filelist.append(filename)
                templist=[]
                
            # Remove any files from the filelist that fail DoesNotContain criteria
            if DoesNotContain:
                for j in DoesNotContain:
                    if j in basename:
                        try: filelist.remove(filename)
                        except: pass
                        

    # Print a quick status summary before finishing up if Quiet is False
    if not Quiet:
        print('{List_Files} Files found which meet all input criteria: ' + str(len(filelist)))
        print('{List_Files} finished!')
    
    return(filelist)

def Exists(location):

    # import modules
    import os
    
    # if the object is neither a file or a location, return False.
    if not os.path.exists(location) and not os.path.isfile(location):
        print('{Exists} '+location + ' is not a valid file or folder!')
        return(False)
    
    #otherwise, return True.
    return(True)

def Enforce_List(item):

    if not isinstance(item,list) and item:
        return([item])
    
    elif isinstance(item,bool):
        print('{Enforce_List} Cannot enforce a bool to be list! at least one list type input is invalid!')
        return(False)
    
    else:
        return(item)
    
#======================================================================================
def Identify(name):
#======================================================================================
# function to examine a filename and compare it against known file naming conventions
#
# Inputs:
#   filename    any filename of a file which is suspected to be a satellite data product
#
# Outputs:
#   data_type   If the file is found to be of a specific data type, output a string
#               designating that type. The options are as follows, with urls for reference                          
#
# data_types:
#       MODIS       https://lpdaac.usgs.gov/products/modis_products_table/modis_overview
#       Landsat     http://landsat.usgs.gov/naming_conventions_scene_identifiers.php
#       TRMM        http://disc.sci.gsfc.nasa.gov/precipitation/documentation/TRMM_README/
#       AMSR_E      http://nsidc.org/data/docs/daac/ae_ocean_products.gd.html
#       ASTER       http://mapaspects.org/article/matching-aster-granule-id-filenames
#       AIRS        http://csyotc.cira.colostate.edu/documentation/AIRS/AIRS_V5_Data_Product_Description.pdf
#       False       if no other types appear to be correct.  
#--------------------------------------------------------------------------------------

    if  any( x==name[0:2] for x in ['LC','LO','LT','LE','LM']):
        return('Landsat')
    elif any( x==name[0:3] for x in ['MCD','MOD','MYD']):
        return('MODIS')
    elif any( x==name[0:4] for x in ['3A11','3A12','3A25','3A26','3B31','3A46','3B42','3B43']):
        return('TRMM')
    elif name[0:3]=='GPM':
        return('GPM')
    elif name[0:6]=='AMSR_E':
        return('AMSR_E')
    elif name[0:3]=='AST':
        return('ASTER')
    elif name[0:3]=='AIR':
        return('AIRS')
    
    
def Grab_Data_Info(filepath,CustGroupings=False,Quiet=False):
#======================================================================================
# This function simply extracts relevant sorting information from a MODIS or Landsat
# filepath of any type or product and returns object properties relevant to that data.
# it will be expanded to include additional data products in the future.
#
# Inputs:
#       filepath        full or partial filepath to any modis product tile
#       CustGroupings   User defined sorting by julian days of specified bin widths.
#                       input of 5 for example will gorup January 1,2,3,4,5 in the first bin
#                       and january 6,7,8,9,10 in the second bin, etc.
#       Quiet           Set Quiet to 'True' if you don't want anything printed to screen.
#                       Defaults to 'False' if left blank.
# Outputs:
#       info            on object containing the attributes (product, year, day, tile)
#                       retrieve these values by calling "info.product", "info.year" etc.
#
# Attributes by data type:
#       All             type,year,j_day,month,day,season,CustGroupings,suffix
#
#       MODIS           product,tile
#       Landsat         sensor,satellite,WRSpath,WRSrow,groundstationID,Version,band
#
# Attribute descriptions:
#       type            NASA data type, for exmaple 'MODIS' and 'Landsat'
#       year            four digit year the data was taken
#       j_day           julian day 1 to 365 or 366 for leap years
#       month           three character month abbreviation
#       day             day of the month
#       season          'Winter','Spring','Summer', or 'Autumn'
#       CustGroupings   bin number of data according to custom group value. sorted by
#                       julian day
#       suffix          Any additional trailing information in the filename. used to find
#                       details about special
#
#       product         usually a level 3 data product from sensor such as MOD11A1
#       tile            MODIS sinusoidal tile h##v## format
#
#       sensor          Landsat sensor
#       satellite       usually 5,7, or 8 for the landsat satellite
#       WRSpath         Landsat path designator
#       WRSrow          Landsat row designator
#       groundstationID ground station which recieved the data download fromt he satellite
#       Version         Version of landsat data product
#       band            band of landsat data product, usually 1 through 10 or 11.      
#--------------------------------------------------------------------------------------

    #import modules
    import os
    import datetime
    
    # pull the filename and path apart 
    path,name=os.path.split(filepath)
    #### nueva linea
    # print(name)
    # create an object class and the info object
    class Object(object):pass
    info = Object()

    # figure out what kind of data these files are. 
    data_type = Identify(name)
    
    # if data looks like MODIS data
    if data_type == 'MODIS':
        params=['product','year','j_day','tile','type','suffix']
        string=[name[0:7],name[9:13],name[13:16],name[17:23],'MODIS',name[25:]]
        for i in range(len(params)):
            setattr(info,params[i],string[i])
            
    # if data looks like Landsat data
    elif data_type =='Landsat':
        params=['sensor','satellite','WRSpath','WRSrow','year','j_day','groundstationID',
                'Version','band','type','suffix']
        name=name.split('.')[0] #remove file extension
        string=[name[1],name[2],name[3:6],name[6:9],name[9:13],name[13:16],name[16:19],
                name[19:21],name[23:].split('_')[0],'Landsat','_'.join(name[23:].split('_')[1:])]
        for i in range(len(params)):
            setattr(info,params[i],string[i])

    # if data looks like TRMM data
    elif data_type == 'TRMM':
        print('{Grab_Data_Info} no support for TRMM data yet! you should add it!')
        return(False)

    # if data looks like AMSR_E data
    elif data_type == 'AMSR_E':
        print('{Grab_Data_Info} no support for AMSR_E data yet! you should add it!')
        return(False)

    # if data looks like ASTER data
    elif data_type == 'ASTER':
        print('{Grab_Data_Info} no support for ASTER data yet! you should add it!')
        return(False)

    # if data looks like AIRS data
    elif data_type == 'AIRS':
        print('{Grab_Data_Info} no support for AIRS data yet! you should add it!')
        return(False)

    # if data doesnt look like anything!
    else:
        print('Data type for file ['+name+'] could not be identified as any supported type')
        print('improve this function by adding info for this datatype!')
        
        return(False)
    # ................................................................................

    # fill in date format values and custom grouping and season information based on julian day
    
    # many files are named according to julian day. we want the date info for these files
    try:
        tempinfo= datetime.datetime(int(info.year),1,1)+datetime.timedelta(int(int(info.j_day)-1))
        info.month  = tempinfo.strftime('%b')
        info.day    = tempinfo.day
    # some files are named according to date. we want the julian day info for these files
    except:
        fmt = '%Y.%m.%d'
        tempinfo= datetime.datetime.strptime('.'.join([info.year,info.month,info.day]),fmt)
        info.j_day = tempinfo.strftime('%a')

    # fill in the seasons by checking the value of julian day
    if int(info.j_day) <=78 or int(info.j_day) >=355:
        info.season='Winter'
    elif int(info.j_day) <=171:
        info.season='Spring'
    elif int(info.j_day)<=265:
        info.season='Summer'
    elif int(info.j_day)<=354:
        info.season='Autumn'
        
    # bin by julian day if integer group width was input
    if CustGroupings:
        CustGroupings=Enforce_List(CustGroupings)
        for grouping in CustGroupings:
            if type(grouping)==int:
                groupname='custom' + str(grouping)
                setattr(info,groupname,1+(int(info.j_day)-1)/(grouping))
            else:
                print('{Grab_Data_Info} invalid custom grouping entered!')
                print('{Grab_Data_Info} [CustGrouping] must be one or more integers in a list')

    # make sure the filepath input actually leads to a real file, then give user the info
    if Exists(filepath):
        if not Quiet:
            print('{Grab_Data_Info} '+ info.type + ' File ['+ name +'] has attributes ',vars(info))
        return(info)
    else: return(False)
