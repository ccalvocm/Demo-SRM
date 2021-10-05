# DEVELOP_SRM_BeoPEST.m

#==========================================================================
#     NASA DEVELOP- Modified Implimentation of the Snowmelt Runoff Model
#==========================================================================
    
#   This script should be called through the matlab script titled 
#   'SRM_Terminal.m', or by a GUI titled GUI_English.m or GUI_Spanish.m
    
#   This modified version of the SRM model first developed by the US
#   department of agriculture has been coded for use in the Coquimbo and
#   Atacama regions of Chile as part of a NASA DEVELOP project. This model
#   has been programed to enable simulation and short range forecasting of
#   stream flow data and was delivered with all necessary information for
#   the basins of Limari, Copiapo, and Huasco.
    
    #   Function Usage:
#       [TuneError,ProjError]=DEVELOP_SRM(root,Basin,...
#       year,TimelagS,TimelagP,Eref,BaseFlow,type,DegDayF,RCsnowF,RCPsF,...
#       RCPnF,TlapseF,XF,YF,Tcrit,Threshold_TRMM_Precip_Zone,Save_Output,...
#       FZS,eseg,tseg)
    
    #   Variable Definitions:
#       root      =Directory where NASA_DEVELOP package is locally saved
#       Basin     =name of folder containing basin for analysis
#       year      =year to process
#       TimelagS  =Timelag according to SRM parameter manual for Snowmelt
#       TimelagP  =Timelag according to SRM parameter manual for precip
#       Eref      =Reference elevation zone (avg elevation of Temperature
#                   stations) for extrapolating T values. 
#       BaseFlow  =minimum flow rate for the simulation period
#       type      =Either 'Validate' or 'Project'. The validate option
#                   requires a complete historical record of actual flow 
#                   rates with which to tune SRM parameters. Project option
#                   should be used in the early springtime to forecast 
#                   water availability until the end of the year.
#       Tcrit     = The critical temperature to be used
#       Threshold_TRMM_Precip_Zone = the minimum elevation zone at which to
#                   use NASA measured precipitation data
#       Save_Output = either 0 or 1 to save an output file or not.
#       FZS       = The forecast Zone Start as described in the GUI
#       eseg      = The Forecast Zone Width as described in the GUI
#       tseg      = The Tuning Zone Width as described in the GUI
    
    #       Mutliplicative factors for tuning:
#           DegDayF
#           RCsnowF
#           RCPsF
#           RCPnF
#           TlapseF
#           XF
#           YF
#       The tuned versions of these parameters will be saved in the output
#       file to preserve a proper record of the caculations performed.
    
    #--------------------------------------------------------------------------
    
    #   This implimentation of the Snowmelt Runoff model deviates from the
#   standard USDA version outlined in the SRM manual in a few key ways to
#   permit proper characterization of these uniquely dry basins and cater
#   to the data sets available. Specific deviations are outlined below.
    
    #   SRM deviations:
#       Time lag: Separate time lag coefficients have been used for flow
#                   calculated from snowmelt and that from precipitation.
#                   It is theorized that snowmelt is slow enough that the
#                   majority of this flow actually becomes groundwater
#                   first. Liquid precipitation on the other hand has been
#                   observed to runoff more immediately.
    
    #       Runoff coefficient: Two sources of precipitation data were used for
#                   simulation in this study. These basins are extremely
#                   steep, and observations have indicated that
#                   precipitation is several times higher in the mountains
#                   than it is in the lowlands where monitoring stations
#                   are present. TRMM data was used in lieu of better
#                   in-situ data at elevations above 2000 meters. TRMM data
#                   is not expected to be particularly accurate for this
#                   climate, but serves as a great placeholder for GPM data
#                   when it becomes available sometime in late 2014. As a
#                   result of this change, two separate runoff coefficients
#                   for each distinct set of precipitation data were used.
    
    #       Baseflow: Prevents 0 flow from causing impossible recession 
#		    coefficients. All calculated flow has the value of 
#		    Baseflow added to it, thus shifting the curve up. this
# 		    is a valuable tuning parameter.
#
    
    #   CIREN
#   contact: ccalvo@ciren.cl
#   version: 19/01/2021 
#========================================================================== 
#                           cargar librerias
#==========================================================================
import pandas as pd
import numpy as np
from hydroeval import evaluator, nse
import datetime
import os
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------

#========================================================================== 
#                           funciones
#==========================================================================

def NSE(nse, sim_flow, obs_flow, axis=1):
        
    # Parameters
    # ----------
    # nse : TYPE
    #     DESCRIPTION.
    # sim_flow : TYPE
    #     DESCRIPTION.
    # obs_flow : TYPE
    #     DESCRIPTION.
    # axis : TYPE, optional
    #     DESCRIPTION. The default is 1.
    
    # Returns
    # -------
    # my_nse : TYPE
    #     DESCRIPTION.
    
    
    serie_sim = sim_flow.ravel()
    serie_obs = obs_flow.ravel()
    my_nse = evaluator(nse, serie_sim, serie_obs, axis=1)
    return my_nse

def DEVELOP_SRM(folder, type_, alpha = 0.959, Tcrit = 1):
    #%%
    
    # Parameters
    # ----------
    # years : int
    #     anos de la simulacion.
    # root : str
    #     ruta de la carpeta de la simulacion.
    # Basin : str
    #     nombre de la cuenca.
    # type_ : str
    #     periodo de validacion o predictivo.
    # Tcrit : float
    #     temperatura critica.
    # bf : str
    #     nombre del archivo de flujo base.
    # si : float
    #     nieve acumulada inicial.
 
    # Returns
    # -------
    # n_se : TYPE
    #     DESCRIPTION.
    # r2 : TYPE
    #     DESCRIPTION.
    # --------------------------------------------------------------------------
    
    #==========================================================================
    #              Retrieve and define all required model inputs
    #==========================================================================
    
    # variables de configuracion de la simulacion
    # -------------------------------------------------------------------------
    # rutas
    root = os.path.join(folder,'SRM')
    Basin = folder.split(os.sep)[-1]

    #leer curva hipsometrica de topografia
    import loopCython
    import loopQtotalCython
    import baseflow_eckhardt

    ruta_hipso = os.path.join(root,'Inputs',r'Hypso.csv')
    hipso = pd.read_csv(ruta_hipso, index_col = 0)
    
    # leer areas glaciares
    ruta_glaciar = os.path.join(root,'Inputs',r'HypsoGlacier.csv')
    hipso_glaciar = pd.read_csv(ruta_glaciar)
    hipso_glaciar = hipso_glaciar.values
    
    # leer time lags y DDs factor
    ruta_timelags_DDs = os.path.join(root,'Inputs',r'timeLagDDsb.csv')
    time_lags_DDs = pd.read_csv(ruta_timelags_DDs)
    # guardar time lags
    tls = time_lags_DDs.values.astype(int)[0,1]
    tlr = time_lags_DDs.values.astype(int)[0,0]
    DDs_fd = time_lags_DDs.values[0,2]
    DDs_fw = time_lags_DDs.values[0,3]
    beta = time_lags_DDs.values[0,4]
    
    # leer master del periodo anterior
    master = pd.read_csv(os.path.join(root,'Inputs',r'Master.csv'), index_col = 0, parse_dates = True)
    
    # última fecha con datos 
    lastDate = pd.read_csv(os.path.join(root,'Inputs',r'LastDateVal.csv'), index_col = 0).index[-1]
           
   # leer archivos para el periodo de validacion
    if type_ == 'V':
        
        # seleccionar hasta la última fecha de validación
        master = master.loc[pd.date_range('2000-01-01', lastDate, freq = '1d')]
    
    # else:
    #     # Primer día de la temporada actual de riego
    #     LastSeason = master.index[-1]
                                                                             
    # años de la simulacíon
    years = str(master.index[0].year)+'-'+str(master.index[-1].year)
        
    # % Cargar caudal observado
    # leer numero de dias
    master.reset_index(drop = True, inplace = True)
    Days =  master.index.values           # List of days
    Qactual = master['Measured Discharge'].values # Actual flow (m3/s)
    
    # cargar coberturas de nieve y glaciares
    SCA = master[[x for x in master.columns if ('Zone' in x) & ('.' not in x)]]         # Snow Covered Area (%)          
    SCA = SCA.values
    GCA = master[[x for x in master.columns if ('Zone' in x) & ('.' in x)]]     # Glacier Covered Area (%)                   
    GCA = GCA.values
    
    Tlapse =    master['Tlapse']  #Tasa de ajuste de temperatura (degC)
    Tlapse = Tlapse.values
    Pbands =     master[[x for x in master.columns if 'Pp_z' in x]]/1000          # Precip bands(m/day)
    Pbands = Pbands.values
    Tbands =     master[[x for x in master.columns if 'T_z' in x]]+Tlapse[0];            # T bands(degC)
    Tbands = Tbands.values
    
    # flags años secos y humedos
    idx_d = master[master['flag_wd'] == 'd'].index
    idx_w = master[master['flag_wd'] == 'w'].index
    
    # multiplicar los factores grado día calibrados
    master.loc[idx_d,'DegDaySnow'] = DDs_fd*master.loc[idx_d,'DegDaySnow'].values
    master.loc[idx_w,'DegDaySnow'] = DDs_fw*master.loc[idx_w,'DegDaySnow'].values
    
    DegDaySnow = master['DegDaySnow']/100           # Factor grado-d�a para nieve(m/degday)
    DegDaySnow = DegDaySnow.values
    DegDayGlacier =     master['DegDayGlacier']/100           # Factor grado-d�a para glaciares(m/degday)
    DegDayGlacier = DegDayGlacier.values
    
    RCsnow =    master[[x for x in master.columns if 'RC_S' in x]]           # Snowmelt runoff coeff includes dry and wet years
    RCsnow = RCsnow.values
    RCp =      master[[x for x in master.columns if 'RC_P' in x]]           #  Rain runoff coeff includes dry and wet years
    RCp = RCp.values
    RCg=       master['RC_g']           #  Coeficiente de escorrent�a para glaciares en a�os secos y h�medos
    RCg = RCg.values
    X =     master['Recess_X']            # X for recession coefficient
    X = X.values
    Y =        master['Recess_Y']           # Y for recession coefficient
    Y = Y.values
    
    # dias de verano
    summerdays = master['summer']             # flag de d�as de verano
    summerdays = summerdays.values
            
    ##    Truncar ceros de punto flotante
    SCA[SCA <= 1e-4] = 0
    GCA[GCA <= 1e-4] = 0
          
    # experimental function by which variable time lags are used between 
    # elevation zones. this is imagined to be useful in basins where time lags
    # are extremely high, but has not been adequately proven. Therefore it is
    # recomended to be left at 'n' for forecasting purposes.
        
    #==========================================================================
    #                     Begin simulating daily flow rate
    #==========================================================================
        
    # compute time lag parameters for each elevation zone
    HighZone = max(hipso.index)
    
    # zonas de elevacion
    nZones = HighZone+1
        
    #Caudales
    #Inicializar caudal simulado.
    Qtot = np.zeros(len(Days))
    Qtot[0] = max(Qactual[0],0)
    
    # inicializar los coeficientes de recesion
    k=np.zeros(len(Days))
    k[0]=0.5
        
    #inicializar Qrain, Q snow, Q newsnow y Q glacial.
    Qrain = np.zeros((len(Days),nZones))
    Qsnow = np.zeros((len(Days),nZones))
    Qnewsnow = np.zeros((len(Days),nZones))
    Qglacial = np.zeros((len(Days),nZones))
    
    #################################
    #       Precipitaciones
    #################################
        
    #Inicializar precipitaciones
    PCR2MET = np.zeros((len(Days),nZones))
    #np.zeros momento de area*precipitacion pluviales
    apPluv = np.zeros(len(Days))

    #################################
    #             Nieve
    #################################
                    
    #Area total
    A = hipso['area'].values
    Atot = np.sum(A)
    
    # inicializar las variables de estado
    snowAcc = np.zeros((len(Days),nZones))
    baseflow_ = np.zeros(len(Days))
    baseflow_[:] = Qtot[0]/2
    
    #==========================================================================
    #                   algoritmos de simulacion 
    #--------------------------------------------------------------------------
    
    # begin simulating subsequent daily flows.
    loopCython.loop(0, Days, nZones, PCR2MET, Pbands, Tbands, Tcrit, snowAcc, A, summerdays, Qnewsnow, RCsnow, DegDaySnow, SCA, Qsnow, Qrain, RCp, Qglacial, hipso_glaciar, RCg, DegDayGlacier, GCA)
  
    #Sumar al area pluvial (se cambia en el siguiente if si es que la precipitacion es solida)
    apPluv = PCR2MET*(1 - SCA)*A
    apPluv = apPluv.sum(axis = 1)

    #Step back through and offset Qsnow and Qrain by Timelag
    # this code considers Snowmelt and precipitation to have separate timelags        
    tol = 1
    i = 1
    while (tol >= .2) & (i < 2e0):
        
        # calcular el caudal total simulado
        loopQtotalCython.loopQtotal(0, Days, nZones, apPluv, k, X, Qtot, Y, baseflow_, tls, tlr, Qsnow, Qnewsnow, Qglacial, Qrain)
        
        # calcular el nuevo flujo base a partir del caudal total
        BaseFlow_iter, tol = baseflow_eckhardt.baseflow(Qtot, alpha, beta, baseflow_)
        
        # calcular la tolerancia
        baseflow_ = BaseFlow_iter[:,0]
        i += 1
    # if tol > 0.9:
    #     print('El flujo base no converge, ajustar los parámetros alpha y beta')
    #     return
        
    # calcular el caudal total simulado
    loopQtotalCython.loopQtotal(0, Days, nZones, apPluv, k, X, Qtot, Y, baseflow_, tls, tlr, Qsnow, Qnewsnow, Qglacial, Qrain)

    # actualizar flujo base inicial
    baseflow_[0] = Qtot[0]       
    
    # fechas para plots
    dates = pd.date_range('2000-01-01',pd.to_datetime('2000-01-01')+datetime.timedelta(days=len(Days)-1), freq = '1d')

    #==========================================================================
    #                   Error calculation
    #==========================================================================
    
    if type_ == 'V':
            
        ####################################
        ##          Calibracion           ##
        ####################################
        calib_ini=41
        calib_fin=4839
        Qobs = Qactual[calib_ini:calib_fin][~np.isnan(Qactual[calib_ini:calib_fin])]
        Qsim = Qtot[calib_ini:calib_fin][~np.isnan(Qactual[calib_ini:calib_fin])]
        
        ####################################
        ##        Estadigrafos            ##
        ####################################
        n_se=NSE(nse,Qsim,Qobs)
        r2=np.corrcoef(Qsim,Qobs)[0,1]**2.
        print('==============================================')
        print('',Basin,years,'C')
        print('  Coeficiente R2 = ',r2)
        print('  N-SE = ',n_se)
        print('==============================================')
        
        ####################################
        ##         Validacion             ##
        ####################################
        Qobs = Qactual[calib_fin+1:][~np.isnan(Qactual[calib_fin+1:])]
        Qsim = Qtot[calib_fin+1:][~np.isnan(Qactual[calib_fin+1:])]
        
        ####################################
        ##        Estadigrafos            ##
        ####################################
        n_se=NSE(nse,Qsim,Qobs)
        r2=np.corrcoef(Qsim,Qobs)[0,1]**2.
        print('==============================================')
        print('',Basin,years,'V')
        print('  Coeficiente R2 = ',r2)
        print('  N-SE = ',n_se)
        print('==============================================')
        plt.close('all')        
                
        # =========================================================================
        #                              Plots                                                      
        #==========================================================================
              
        #plot settings 
        plot_ini = '2000-01-01'
        frequency = 270
        
        # fechas
        Days_xticks = [ x for x in pd.date_range(plot_ini,pd.to_datetime(plot_ini)+datetime.timedelta(days=len(Days)-1), freq = '1d').date]  
        rot = 15
        last_year = Days_xticks[-1].year 
        first_year = Days_xticks[0].year 
        
        # find the limits of the plots to properly scale the data
        # precpitaci�n y temperatura promedio
        Pmean=1000*np.sum(Pbands*A, axis = 1)/Atot
        Tmean=np.sum(Tbands*A, axis = 1) / Atot
                  
        # plot relative runoffs
        fig = plt.figure(figsize=(18 , 12))
        ax = fig.add_subplot(3,1,1)
        plt.plot(Days,Qactual,'k-', linewidth = 2)
        plt.plot(Days,Qtot,'r-', linewidth = 2)
        plt.title('Caudal real vs simulado: ' +str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        # plt.ylabel('Caudal ($m^3/s$)')
        plt.legend(['Q Real','Q Simulado'])
        plt.legend(['Q Simulado'])
            
        plt.axis([Days[0],Days[-1],0,1.5*max(max(Qtot),max(Qactual))])
        plt.grid()
        
        locs, labels = plt.xticks()  # Get the current locations and labels.
        plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
             
        ax1 = plt.subplot(3,1,2)
        plt.grid()
        ax1.plot(Days,Tmean,'r-', linewidth = 1)
        ylim_min = min(Tmean)
        ylim_max = max(Pmean)
        ax1.set_ylim(ylim_min, ylim_max)
        ax2 = ax1.twinx()
        ax2.bar(Days,Pmean, color = 'b', width = 15, bottom = 0, linewidth = 2)
        ax2.set_ylim(ylim_min, ylim_max)
        # plt.title('Precipitación y temperatura: '+str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        ax1.set_ylabel('Temperatura (°C)')
        ax2.set_ylabel('Precipitación (mm/día)')
        ax1.legend(['Temperatura'], loc = 'upper right')
        ax2.legend(['Precipitación'], loc = 'upper right', bbox_to_anchor=(1, 0.875))
            
        ax1.axis([Days[0],Days[-1],ylim_min, ylim_max])
        
        # Get the current locations and labels.
        start, end = ax1.get_xlim()
        # set  xticks
        ax1.xaxis.set_ticks(np.arange(start, end, frequency))
        ax1.set_xticklabels(Days_xticks[::frequency], rotation=rot)
        # plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
        
        # reformat the way this is expressed t o make code section 508 compliant for
        # software release on behalf of the US government.
        
        wSCAhi= np.sum(SCA*A, axis = 1) / Atot
            
        # now actually plot it.
        plt.subplot(3,1,3)
        ##        plot(Days,wSCAlow,'k-','LineWidth',2);
        plt.plot(Days,wSCAhi,'steelblue','LineWidth',2)
        # plt.title('Cobertura de nieve: '+str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        plt.ylabel('Fracción cubierta por nieve')
        # DEVELOP_SRM_BeoPEST.m:466
        plt.legend(['Fracción cubierta por nieve'], loc = 'upper right')
        plt.axis([Days[0],Days[-1],0,1])
        plt.grid()
        
        locs, labels = plt.xticks()  # Get the current locations and labels.
        plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
     
    else:
        plt.close('all')
        # =========================================================================
        #                              Plots                                                      
        #==========================================================================    
        
        # seleccionar el último año de simulación                
        # inicio del primer año hidrológico
        years = [x.year for x in dates]
        years = list(dict.fromkeys(years))
        plot_ini = pd.to_datetime(str(years[-2])+'-04-01')

        # Qactual
        Qactual = pd.DataFrame(Qactual, index = dates)
        Qactual = Qactual.loc[Qactual.index >= plot_ini]        
        
        # Qforecast
        Qfor = pd.DataFrame(Qtot, index = dates)
        Qfor = Qfor.loc[Qfor.index >= plot_ini]
        
        # fechas
        Days_xticks = [ x for x in pd.date_range(plot_ini,pd.to_datetime(plot_ini)+datetime.timedelta(days=len(Qfor)-1), freq = '1d').date]  
        Days = Days[-len(Qfor):]
        
        rot = 15
        last_year = Days_xticks[-1].year 
        first_year = Days_xticks[0].year 
        
        # find the limits of the plots to properly scale the data
        # precpitaci�n y temperatura promedio
        Pmean=1000*np.sum(Pbands*A, axis = 1)/Atot
        Tmean=np.sum(Tbands*A, axis = 1) / Atot

        Pmean = pd.DataFrame(Pmean, index = dates)
        Pmean = Pmean.loc[Pmean.index >= plot_ini]        

        Tmean = pd.DataFrame(Tmean, index = dates)
        Tmean = Tmean.loc[Tmean.index >= plot_ini]    
        
        # settings para plots
        frequency = 60
        
        # plot relative runoffs
        fig = plt.figure(figsize=(18 , 12))
        ax = fig.add_subplot(3,1,1)
        plt.plot(Days,Qactual.values,'k-', linewidth = 2)
        plt.plot(Days,Qfor.values,'r-', linewidth = 2)
        plt.title('Caudal real vs simulado: ' +str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        # plt.ylabel('Caudal ($m^3/s$)')
        plt.legend(['Q Real','Q Simulado'])
        plt.legend(['Q Simulado'])
            
        plt.axis([Days[0],Days[-1],0,1.5*max(max(Qtot),max(Qactual))])
        plt.grid()
        
        locs, labels = plt.xticks()  # Get the current locations and labels.
        plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
             
        ax1 = plt.subplot(3,1,2)
        plt.grid()
        ax1.plot(Days,Tmean.values,'r-', linewidth = 1)
        ylim_min = Tmean.min().values
        ylim_max = Pmean.max().values
        ax1.set_ylim(ylim_min, ylim_max)
        ax2 = ax1.twinx()
        ax2.bar(Days,Pmean.values[:,0], color = 'b', width = 15, bottom = 0, linewidth = 2)
        ax2.set_ylim(ylim_min, ylim_max)
        # plt.title('Precipitación y temperatura: '+str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        ax1.set_ylabel('Temperatura (°C)')
        ax2.set_ylabel('Precipitación (mm/día)')
        ax1.legend(['Temperatura'], loc = 'upper right')
        ax2.legend(['Precipitación'], loc = 'upper right', bbox_to_anchor=(1, 0.875))
            
        ax1.axis([Days[0],Days[-1],ylim_min, ylim_max])
        
        # Get the current locations and labels.
        start, end = ax1.get_xlim()
        # set  xticks
        ax1.xaxis.set_ticks(np.arange(start, end, frequency))
        _ = ax1.set_xticklabels(Days_xticks[::frequency], rotation=rot)
        # plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
        
        # reformat the way this is expressed t o make code section 508 compliant for
        # software release on behalf of the US government.
        
        wSCAhi = np.sum(SCA*A, axis = 1) / Atot
        wSCAhi = pd.DataFrame(wSCAhi, dates)
        wSCAhi = wSCAhi.loc[wSCAhi.index >= plot_ini]    

        # now actually plot it.
        plt.subplot(3,1,3)
        ##        plot(Days,wSCAlow,'k-','LineWidth',2);
        plt.plot(Days,wSCAhi.values[:,0],'steelblue','LineWidth',2)
        # plt.title('Cobertura de nieve: '+str(first_year)+'-'+str(last_year))
        # plt.xlabel('Days')
        plt.ylabel('Fracción cubierta por nieve')
        # DEVELOP_SRM_BeoPEST.m:466
        plt.legend(['Fracción cubierta por nieve'], loc = 'upper right')
        plt.axis([Days[0],Days[-1],0,1])
        plt.grid()
        
        locs, labels = plt.xticks()  # Get the current locations and labels.
        plt.xticks(Days[::frequency], Days_xticks[::frequency], rotation=rot)  # Set text labels and properties.
                
        # acortar los días al año de pronóstico
        Days = Days[-len(Qfor):]
                
        # calcular los caudales medios mensuales
        Qfor = Qfor.resample('MS').mean()
        Qfor.reset_index(inplace = True, drop = True)
        
        # graficar la curva de variación estacional histórica

        cve = pd.read_csv(os.path.join(root,'Inputs',r'CVE.csv'), skiprows = 1)
        fig, axis = plt.subplots(1,figsize=(8.9,4))
     
        axis.tick_params(axis='both', which='major', labelsize = 9)
        axis.tick_params(axis='both', which='minor', labelsize = 9)
        colores =  ['blue','magenta',  'yellow',  'cyan', 'purple', 'brown']
        
        # curva de variacion estaiconal historica
        cve.plot(ax = axis, color=colores, style='-', markersize=12, legend=False, linewidth = 3, logy=False)
                         
        # caudales medios mensuales pronosticados
        Qfor.plot(ax = axis, color='r', style='--', marker = 'D', markersize=12, legend=False, linewidth = 3, logy=False)
        
        axis.set_ylabel('Caudal $(m^3/s)$',  fontsize = 9)
        axis.set_ylim(bottom = 0)
        axis.grid(linestyle='-.')
        axis.legend(['Q5%','Q10%', 'Q20%','Q50%','Q85%', 'Q95%','Qpronóstico'], prop={'size': 9})
        axis.set_xticks(range(12)) 
        _ = axis.set_xticklabels(['Abr', 'May', 'Jun ', 'Jul', 'Ago', 'Sep', 'Oct',
                     'Nov', 'Dic', 'Ene', 'Feb', 'Mar'], fontsize = 9)
    
#%%    
    #==========================================================================
    #                   Save output for the simulated flow.
    #==========================================================================
    
    # guardar el SWE y caudales
    # SWE sim
    swe_sim = np.sum(snowAcc*A, axis = 1) / Atot
    swe_sim = pd.DataFrame(swe_sim, index = dates, columns = ['Equivalente en agua de nieve (m)']) # SWE en m    SWE_out = pd.DataFrame(snowAcc, index = dates, columns = ['Equivalente de agua en nieve (m)']) # SWE en m
    swe_sim.index.name = 'Fecha'
    Q_out = pd.DataFrame(Qtot, index = dates, columns = ['Caudal (m3/s)']) # en l/s
    Q_out.index.name = 'Fecha'
    swe_sim.to_csv(os.path.join(root,'Resultados','SWEsim_'+Basin+'.csv')) 
    Q_out.to_csv(os.path.join(root,'Resultados','Qsim_'+Basin+'.csv'))

    return None
    
# if __name__ == '__main__':
    # directorio de la cuenca
    # folder = os.path.abspath(os.path.join('.','01_Maipo','01_RMELA','Nieve'))
    # root = folder.replace('Nieve','SRM')
    # Basin = root.split(os.sep)[-2]
    # DEVELOP_SRM(root, Basin, type_ = 'V', alpha = 0.959, Tcrit = 1)
    