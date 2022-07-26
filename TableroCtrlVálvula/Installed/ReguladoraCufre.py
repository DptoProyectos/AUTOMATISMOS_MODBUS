#!/usr/aut_env/bin/python3.8
'''
ENVIO DE CONFIGURACION REMOTA PARA LOS TABLEROS DE CONTROL DE REGULADORAS

@author: Yosniel Cabrera

Version 1.0.3 27-04-2022
''' 
from datetime import datetime
from __CORE__.modbusWrite import mbusWrite

dlgid  = 'SJREG001'
#
########################################## CONTROLES WEB ##########################################
CONTROLES_WEB = False                                           # ENABLE para enviar los controles WEBs [True|False]

WEB_Mode = 102                                                  # Selección de modo [100 -> EMERGENCIA | 101 -> AUTOMATICO | 102 -REMOTO]
WEB_ActionValve = 101                                           # Accion sobre la bomba [100 -> CERRAR | 101 -> ABRIR]
WEB_LevelMin = 1.20                                             # Nivel minimo a mantener [VALUE]
WEB_LevelMax = 1.50                                             # Nivel maximo a mantener [VALUE]


########################################## REFERENCIAS REMOTAS ##########################################
REFERENCIAS_REMOTAS = False                                     # ENABLE para enviar las referencias remotas [True|False]

MainRef = 1.18                                                  # Referencia remota principal [VALUE]                                           
SecRef = 1.19                                                   # Referencia remota secundaria [VALUE]  


########################################## CONFIGURACIONES ##########################################
CONFIGURACIONES = True                                          # ENABLE para enviar las configuraciones [True|False]             

### CONTROL
tipoControl = 1                                                 # Tipo de control { 0-> [ OPEN if LevelRef <= MinLevel | CLOSE if LevelRef >= MaxLevel ] }   
                                                                # Tipo de control { 1-> [ OPEN if LevelRef >= MaxLevel | CLOSE if LevelRef <= MinLevel ] }
                                                                # Tipo de control { 4-> [ OPEN if LevelRef <= MinLevel | CLOSE if LevelRef >= MaxLevel ] } [1]

referencia = 1                                                  # Referencia para el control [ 0-> REMOTO, 1-> AI_0, 2-> AI_1, 3-> CNT_0, 4-> CNT_1 ]
Time2OpenValve = 60                                             # Tiempo en segundos que dura el proceso de apertura de valvula [VALUE]
Time2CloseValve = 90                                            # Tiempo en segundos que dura el proceso de cierre de valvula [VALUE]

# NOTA:
# 1- Lugo de un proceso de apertura se espera 30 minutos antes de atender cualquier cierre (Solo en modo AUTO) para evitar que las transiciones de presion debido a la apertura provoquen un cierre.


### ENTRADAS ANALOGICAS
#### AI0
AI0_Enab = True                                                 # ENABLE para el canal analogico [True|False]
AI0_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI0_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI0_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI0_Mmax = 15                                                   # Magnitud maxima del canal analogico [VALUE]    
AI0_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 
#
#### AI1
AI1_Enab = True                                                 # ENABLE para el canal analogico [True|False]
AI1_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI1_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI1_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI1_Mmax = 10                                                   # Magnitud maxima del canal analogico [VALUE] 
AI1_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 


















# ESCRITURA DE REIGSTROS
## CONTROLES WEB
if CONTROLES_WEB:
    mbusWrite(dlgid,'1934','interger',WEB_Mode)
    mbusWrite(dlgid,'1935','interger',WEB_ActionValve)
    mbusWrite(dlgid,'1955','float',WEB_LevelMin)
    mbusWrite(dlgid,'1957','float',WEB_LevelMax)
## REFERENCIAS REMOTAS
if REFERENCIAS_REMOTAS:
    mbusWrite(dlgid,'1962','float',MainRef)
    if SecRef: mbusWrite(dlgid,'2032','float',SecRef)

## CONFIGURACIONES
if CONFIGURACIONES:
    # GENERAL
    mbusWrite(dlgid,'2023','float',(datetime.now().hour))
    mbusWrite(dlgid,'2024','float',(datetime.now().minute))
    mbusWrite(dlgid,'2030','float',(datetime.now().day))
    mbusWrite(dlgid,'2027','float',(datetime.now().month))
    mbusWrite(dlgid,'2028','float',(datetime.now().year - 2000))
    # TIPO DE CONTROL
    mbusWrite(dlgid,'1961','interger',tipoControl)
    mbusWrite(dlgid,'1978','interger',referencia)
    mbusWrite(dlgid,'2133','interger',Time2OpenValve)
    mbusWrite(dlgid,'2134','interger',Time2CloseValve)
       
    ### ENTRADAS ANALOGICAS
    mbusWrite(dlgid,'1924','interger',int('{0}{1}11'.format(int(AI1_Enab == True),int(AI0_Enab == True)),2))
    mbusWrite(dlgid,'1968','interger',AI0_Imin)
    mbusWrite(dlgid,'1969','interger',AI0_Imax)
    mbusWrite(dlgid,'1942','float',AI0_Mmin)
    mbusWrite(dlgid,'1944','float',AI0_Mmax)
    mbusWrite(dlgid,'2043','float',AI0_Offset)
    mbusWrite(dlgid,'1970','interger',AI1_Imin)
    mbusWrite(dlgid,'1971','interger',AI1_Imax)
    mbusWrite(dlgid,'1946','float',AI1_Mmin)
    mbusWrite(dlgid,'1948','float',AI1_Mmax)
    mbusWrite(dlgid,'2045','float',AI1_Offset)
    
 







