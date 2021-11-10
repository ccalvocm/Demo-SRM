# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 09:24:41 2021

@author: Carlos
"""
def loopQtotal(FirstDay, Days, nZones, apPluv, k, X, Qtot, Y, BaseFlow_, tls, tlr, Qsnow, Qnewsnow, Qglacial, Qrain):
    def sign(x):
        if x > 0:
            return 1.
        elif x < 0:
            return -1.
        elif x == 0:
            return 0.
        else:
            return x
    
    for i in range(FirstDay,(len(Days) - 1)):
    #calculating the recession coefficient 
    #Correcci�n del coeficiente dependiendo de las lluvias torrenciales, es 4 si el umbral es mayor que 6
        corr_fac=1.0 + 3*max(sign(apPluv[i] - 0.06),0)
        k[i + 1]=min(X[i]*(corr_fac*Qtot[i]) ** (- Y[i]),0.95)
        
        #Calculate Qtotal by adding the Snow and Rain flows with timelags.
        # Aquí tengo que cambiar las ecuaciones para el predictivo
        Qtot[i + 1]=BaseFlow_[i + 1]
        for j in range(0,nZones):
            
            ##sumar Q deshielo al flujo base
            if i > tls:
                Qtot[i + 1] = Qtot[i + 1] + Qsnow[i + 1 - tls,j] + Qnewsnow[i + 1 - tls,j] + Qglacial[i + 1 - tls,j]
                
            ##sumar Q lluvia al flujo base
            if i > tlr:
                Qtot[i + 1] = Qtot[i + 1] + Qrain[i + 1 - tlr,j]
        
        # coeficientes de recesion
        Qtot[i + 1]=Qtot[i + 1]*(1 - k[i + 1]) + Qtot[i]*k[i + 1]  
    return None