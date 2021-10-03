# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 08:59:20 2021

@author: ccalvo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 08:54:54 2021

@author: ccalvo
"""

def loop(FirstDay, Days, nZones, PCR2MET, Pbands, Tbands, Tcrit, snowAcc, A, summerdays, Qnewsnow, RCsnow, DegDaySnow, SCA, Qsnow, Qrain, RCp, Qglacial, hipso_glaciar,RCg, DegDayGlacier,  GCA ):
    for i in range(FirstDay,len(Days) - 1):
           for j in range(0,nZones):
               # actualizar el SWE
               snowAcc[i+1,j] = snowAcc[i,j]
               #precipitacion de cada zona
               PCR2MET[i,j]=Pbands[i,j]
               # Tratar la precipitacion nueva como nieve o lluvia
               if Tbands[i,j] < Tcrit:
                   #Acumula nieve y corrige la precipitacion liquida calculada anteriormente
                   snowAcc[i+1,j] = snowAcc[i+1,j] + 1.5*Pbands[i,j] #SWE en m
                   PCR2MET[i,j]=0
                   if summerdays[i] == 1:
                       Qnewsnow[i + 1,j]=max(RCsnow[i,j]*DegDaySnow[i]*Tbands[i,j]*(1 - SCA[i,j])*A[j]/86400,0) #en m3/s
                       snowAcc[i+1,j] = max(snowAcc[i+1,j]-DegDaySnow[i]*Tbands[i,j], 0) # en m/d
               # La precipitacion se trata por zonas para cuencas con un desnivel mayor a 500m seg�n  Martinec (2008):
               # suprimo el if innecesario de la temperatura de fusi�n con un maxmin
               #De acuerdo a Martinec (2008) p. 22, los Rc y DD debiesen depender de j
               if Tbands[i,j] > 0:
                   Qsnow[i + 1,j]=min(snowAcc[i+1,j]*A[j] / 86_400,RCsnow[i,j]*DegDaySnow[i]*Tbands[i,j]*SCA[i,j]*A[j] / 86_400)
                   ##          con derretimiento, como funciona el WinSRM
                   snowAcc[i+1,j] = max(0, snowAcc[i+1,j] - DegDaySnow[i]*Tbands[i,j]) #SWE en cm
                   #Q lluvia
                   Qrain[i + 1,j]=RCp[i,j]*PCR2MET[i,j]*A[j] / 86_400
                   ##              Q glacial
                   Qglacial[i + 1,j]=max(hipso_glaciar[j]*RCg[i]*DegDayGlacier[i]*Tbands[i,j]*(1 - GCA[i,j]) / 86_400,0)    
    return None