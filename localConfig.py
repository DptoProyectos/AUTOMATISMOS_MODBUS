#!/usr/aut_env/bin/python3.8
'''
ENVIO DE CONFIGURACION REMOTA PARA LOS TABLEROS DE CONTROL

@author: Yosniel Cabrera

Version 1.0.1 06-01-2022 17:30
''' 
from datetime import datetime
from modbusWrite import mbusWrite

dlgid  = 'YCHTESTT'
#
## CONTROLES WEB
CONTROLES_WEB = False                                           # ENABLE para enviar los controles WEBs [True|False]
WEB_Mode = 100                                                  # Selección de modo [100 -> EMERGENCIA | 101 -> AUTOMATICO | 102 -REMOTO]
WEB_ActionPump = 101                                            # Accion sobre la bomba [100 -> APAGAR | 101 -> PRENDER]
WEB_LevelMin = 0.5                                              # Nivel minimo a mantener [VALUE]
WEB_LevelMax = 1.5                                              # Nivel maximo a mantener [VALUE]
WEB_Frequency = 50                                              # Frecuencia de trabajo [VALUE]
WEB_UpDownPressure = 0.6                                        # Consigna que se quiere mantener por iteraciones exponenciales [VALUE]
#
## REFERENCIAS REMOTAS
REFERENCIAS_REMOTAS = False                                     # ENABLE para enviar las referencias remotas [True|False]
MainRef = 1.18                                                  # Referencia remota principal [VALUE]                                           
SecRef = 1.19                                                   # Referencia remota secundaria [VALUE]  
#
## CONFIGURACIONES
CONFIGURACIONES = True                                          # ENABLE para enviar las configuraciones [True|False]             
### GENERAL                                                     # Se establecen las fecha y horas actuales tomadas del servidor'''
### CONTROL
tipoControl = 0                                                 # Tipo de control [0->NIVELES LLENADO,1->NIVELES VACIADO,2->EXTERNO,3->CONSIGNA CONT]
referencia = 0                                                  # Referencia a tomar para el control [0->REMOTO,1->AI_0,2->AI_1,3->CNT_0,4->CNT_1]
### ENTRADAS ANALOGICAS
#### AI0
AI0_Enab = True                                                 # ENABLE para el canal analogico [True|False]
AI0_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI0_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI0_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI0_Mmax = 10                                                   # Magnitud maxima del canal analogico [VALUE]    
AI0_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 
#### AI1
AI1_Enab = True                                                 # ENABLE para el canal analogico [True|False]
AI1_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI1_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI1_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI1_Mmax = 10                                                   # Magnitud maxima del canal analogico [VALUE] 
AI1_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 
#
### ENTRADAS DE PULSOS
#### CNT0
#....
#### CNT1
#....
#
### SALIDAS ANALOGIAS
#....
#
### TEMPORIZADORES
#....
#
### REFERENCIA REMOTA
#### AJUSTE DE MEDIDA
Ref1Fact = 1.0                                                  # Factor de multiplicacion para el dato que viene de la referencia remota 1 [VALUE]
Ref1OffSet = 0.0                                                # Valor de OffSet para el dato que viene de la referencia remota 1 [VALUE]                                          
Ref2Fact = 1.0                                                  # Factor de multiplicacion para el dato que viene de la referencia remota 2 [VALUE]
Ref2OffSet = 0.0                                                # Valor de OffSet para el dato que viene de la referencia remota 2 [VALUE]
#### VALIDACION DE DATO
Ref1MinValue = -0.1                                             # Valor minimo hasta el cual se considera valida la referencia remota 1 [VALUE]
Ref1MaxValue = 15.1                                             # Valor maximo hasta el cual se considera valida la referencia remota 1 [VALUE]
Ref2MinValue = -0.1                                             # Valor minimo hasta el cual se considera valida la referencia remota 2 [VALUE]
Ref2MaxValue = 15.1                                             # Valor maximo hasta el cual se considera valida la referencia remota 2 [VALUE]


























































# ESCRITURA DE REIGSTROS
## CONTROLES WEB
if CONTROLES_WEB:
    mbusWrite(dlgid,'1934','interger',WEB_Mode)
    mbusWrite(dlgid,'1935','interger',WEB_ActionPump)
    mbusWrite(dlgid,'1955','float',WEB_LevelMin)
    mbusWrite(dlgid,'1957','float',WEB_LevelMax)
    mbusWrite(dlgid,'1959','float',WEB_Frequency)
    mbusWrite(dlgid,'1936','float',WEB_UpDownPressure)
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
    # REFERENCIA REMOTA
    mbusWrite(dlgid,'2055','float',Ref1Fact)
    mbusWrite(dlgid,'2047','float',Ref1OffSet)
    mbusWrite(dlgid,'2057','float',Ref2Fact)
    mbusWrite(dlgid,'2049','float',Ref2OffSet)
    mbusWrite(dlgid,'2035','float',Ref1MinValue)
    mbusWrite(dlgid,'2037','float',Ref1MaxValue)
    mbusWrite(dlgid,'2039','float',Ref2MinValue)
    mbusWrite(dlgid,'2041','float',Ref2MaxValue)
 







