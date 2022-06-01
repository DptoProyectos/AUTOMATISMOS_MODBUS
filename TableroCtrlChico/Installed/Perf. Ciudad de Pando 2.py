#!/usr/aut_env/bin/python3.8
'''
ENVIO DE CONFIGURACION REMOTA PARA LOS TABLEROS DE CONTROL CHICO

@author: Yosniel Cabrera

Version 1.0.5 09-05-2022
''' 
from datetime import datetime
from modbusWrite import mbusWrite


dlgid  = 'CCPERF005'

#
########################################## CONTROLES WEB ##########################################
CONTROLES_WEB = False                                           # ENABLE para enviar los controles WEBs [True|False]

WEB_Mode = 100                                                  # Selección de modo [ 100 -> EMERGENCIA | 101 -> AUTOMATICO | 102 -> REMOTO | 103 -> TIMER ]
WEB_ActionPump = 101                                            # Accion sobre la bomba [ 100 -> APAGAR | 101 -> PRENDER ]
WEB_LevelMin = 0.5                                              # Nivel minimo a mantener [VALUE]
WEB_LevelMax = 1.5                                              # Nivel maximo a mantener [VALUE]
WEB_Frequency = 50                                              # Frecuencia de trabajo [VALUE]
WEB_UpDownPressure = 0.6                                        # Consigna que se quiere mantener por iteraciones exponenciales [VALUE]


########################################## REFERENCIAS REMOTAS ##########################################
REFERENCIAS_REMOTAS = False                                     # ENABLE para enviar las referencias remotas [True|False]

MainRef = 1.18                                                  # Referencia remota principal [VALUE]                                           
SecRef = 1.19                                                   # Referencia remota secundaria [VALUE]  


########################################## CONFIGURACIONES ##########################################
CONFIGURACIONES = True                                          # ENABLE para enviar las configuraciones [True|False]             

### CONTROL
tipoControl = 0                                                 # Tipo de control [0->NIVELES LLENADO,1->NIVELES VACIADO,2->EXTERNO,3->CONSIGNA CONT]
referencia = 0                                                  # Referencia a tomar para el control [0->REMOTO,1->AI_0,2->AI_1,3->CNT_0,4->CNT_1,5->BOYAS CONECTADAS EN CNT0 Y CNT1]


### ENTRADAS ANALOGICAS
#### AI0
AI0_Enab = True                                                # ENABLE para el canal analogico [True|False]
AI0_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI0_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI0_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI0_Mmax = 10                                                   # Magnitud maxima del canal analogico [VALUE]    
AI0_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 
#
#### AI1
AI1_Enab = False                                                # ENABLE para el canal analogico [True|False]
AI1_Imin = 4                                                    # Corriente minima del canal analogico [VALUE]
AI1_Imax = 20                                                   # Corriente maxima del canal analogico [VALUE]
AI1_Mmin = 0                                                    # Magnitud minima del canal analogico [VALUE]
AI1_Mmax = 10                                                   # Magnitud maxima del canal analogico [VALUE] 
AI1_Offset = 0                                                  # Offset para la medición del canal analógico [VALUE] 

### ENTRADAS DE PULSOS
#### CNT0
CNT0_timeOn = 10                                                # tiempo en On para decir que es válido [VALUE]
CNT0_timeOff = 100                                              # tiempo en Off para decir que es válido [VALUE]
CNT0_magpp = 0.010                                              # equivalencia de cada pulsos contra la unidad que se quiere medir [VALUE]
#
#### CNT1
CNT1_timeOn = 10                                                # tiempo en On para decir que es válido [VALUE]
CNT1_timeOff = 100                                              # tiempo en Off para decir que es válido [VALUE]
CNT1_magpp = 0.010                                              # equivalencia de cada pulsos contra la unidad que se quiere medir [VALUE]

### SALIDAS ANALOGIAS
AO0_Mmin = 0                                                    # valor minimo de la magnitud a escalar en la salida [VALUE]
AO0_Mmax = 50                                                   # valor maximo de la magnitud a escalar en la salida [VALUE]
AO0_OutMmin = 0                                                 # valor minimo de la señal de salida [VALUE]
AO0_OutMmax = 50                                                # valor maximo de la señal de salida [VALUE]

### TEMPORIZADORES
#### Temporizador 1
T1_Enable = True                                                # ENABLE para el temporizador 1 [True|False]
T1_StartHour = 15                                               # Hora de arranque de la bomba [VALUE]
T1_StartMin = 50                                                # Minuto de arranque de la bomba [VALUE]
T1_StopHour = 15                                                # Hora de apagado de la bomba [VALUE]
T1_StopMin = 55                                                 # Minuto de apagado de la bomba [VALUE]
T1_weekMon = True                                               # Activacion del timer los lunes [True|False]
T1_weekTues = True                                              # Activacion del timer los martes [True|False]
T1_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T1_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T1_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T1_weekSat = True                                               # Activacion del timer los sabado [True|False]
T1_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 2
T2_Enable = False                                               # ENABLE para el temporizador 2 [True|False]
T2_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T2_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T2_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T2_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T2_weekMon = True                                               # Activacion del timer los lunes [True|False]
T2_weekTues = True                                              # Activacion del timer los martes [True|False]
T2_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T2_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T2_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T2_weekSat = True                                               # Activacion del timer los sabado [True|False]
T2_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 3
T3_Enable = False                                               # ENABLE para el temporizador 3 [True|False]
T3_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T3_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T3_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T3_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T3_weekMon = True                                               # Activacion del timer los lunes [True|False]
T3_weekTues = True                                              # Activacion del timer los martes [True|False]
T3_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T3_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T3_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T3_weekSat = True                                               # Activacion del timer los sabado [True|False]
T3_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 4
T4_Enable = False                                               # ENABLE para el temporizador 4 [True|False]
T4_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T4_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T4_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T4_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T4_weekMon = True                                               # Activacion del timer los lunes [True|False]
T4_weekTues = True                                              # Activacion del timer los martes [True|False]
T4_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T4_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T4_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T4_weekSat = True                                               # Activacion del timer los sabado [True|False]
T4_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 5
T5_Enable = False                                               # ENABLE para el temporizador 5 [True|False]
T5_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T5_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T5_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T5_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T5_weekMon = True                                               # Activacion del timer los lunes [True|False]
T5_weekTues = True                                              # Activacion del timer los martes [True|False]
T5_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T5_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T5_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T5_weekSat = True                                               # Activacion del timer los sabado [True|False]
T5_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 6
T6_Enable = False                                               # ENABLE para el temporizador 6 [True|False]
T6_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T6_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T6_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T6_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T6_weekMon = True                                               # Activacion del timer los lunes [True|False]
T6_weekTues = True                                              # Activacion del timer los martes [True|False]
T6_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T6_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T6_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T6_weekSat = True                                               # Activacion del timer los sabado [True|False]
T6_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador 7
T7_Enable = False                                               # ENABLE para el temporizador 7 [True|False]
T7_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
T7_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
T7_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
T7_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
T7_weekMon = True                                               # Activacion del timer los lunes [True|False]
T7_weekTues = True                                              # Activacion del timer los martes [True|False]
T7_weekWend = True                                              # Activacion del timer los miercoles [True|False]
T7_weekThurs = True                                             # Activacion del timer los jueves [True|False]
T7_weekFrid = True                                              # Activacion del timer los viernes [True|False]
T7_weekSat = True                                               # Activacion del timer los sabado [True|False]
T7_weekSund = True                                              # Activacion del timer los domingo [True|False]
#
#### Temporizador encendido diario (Daily Start)
DS_Enable = False                                               # ENABLE para el temporizador de encendido diario [True|False]
DS_StartHour = 6                                                # Hora de arranque de la bomba [VALUE]
DS_StartMin = 30                                                # Minuto de arranque de la bomba [VALUE]
DS_StopHour = 23                                                # Hora de apagado de la bomba [VALUE]
DS_StopMin = 30                                                 # Minuto de apagado de la bomba [VALUE]
DS_weekMon = True                                               # Activacion del timer los lunes [True|False]
DS_weekTues = True                                              # Activacion del timer los martes [True|False]
DS_weekWend = True                                              # Activacion del timer los miercoles [True|False]
DS_weekThurs = True                                             # Activacion del timer los jueves [True|False]
DS_weekFrid = True                                              # Activacion del timer los viernes [True|False]
DS_weekSat = True                                               # Activacion del timer los sabado [True|False]
DS_weekSund = True                                              # Activacion del timer los domingo [True|False]

### REFERENCIA REMOTA
#### AJUSTE DE MEDIDA
Ref1Fact = 1.0                                                  # Factor de multiplicacion para el dato que viene de la referencia remota 1 [VALUE]
Ref1OffSet = 0.0                                                # Valor de OffSet para el dato que viene de la referencia remota 1 [VALUE]                                          
Ref2Fact = 1.0                                                  # Factor de multiplicacion para el dato que viene de la referencia remota 2 [VALUE]
Ref2OffSet = 0.0                                                # Valor de OffSet para el dato que viene de la referencia remota 2 [VALUE]
#
#### VALIDACION DE DATO
Ref1MinValue = -0.1                                             # Valor minimo hasta el cual se considera valida la referencia remota 1 [VALUE]
Ref1MaxValue = 15.1                                             # Valor maximo hasta el cual se considera valida la referencia remota 1 [VALUE]
Ref2MinValue = -0.1                                             # Valor minimo hasta el cual se considera valida la referencia remota 2 [VALUE]
Ref2MaxValue = 15.1                                             # Valor maximo hasta el cual se considera valida la referencia remota 2 [VALUE]

### PROTECCIONES
Prot1_Enable = False                                            # ENABLE para la protección 1 [True|False]
Prot1_Stop = 1.0                                                # valor por debajo del cual se activa la protección 1 [VALUE]
Prot1_Ref = 0                                                   # Tipo de referencia [0->REMOTO,1->AI_0,2->AI_1,3->CNT_0,4->CNT_1]
Prot1_Recover = 1.5                                             # valor por arriba del cual se restablece la proteccion




######################################################################################################################################
#############################################################LOGIC####################################################################
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
    mbusWrite(dlgid,'2023','interger',(datetime.now().hour))
    mbusWrite(dlgid,'2024','interger',(datetime.now().minute))
    mbusWrite(dlgid,'2030','interger',(datetime.now().day))
    mbusWrite(dlgid,'2027','interger',(datetime.now().month))
    mbusWrite(dlgid,'2028','interger',(datetime.now().year - 2000))
    # TIPO DE CONTROL
    mbusWrite(dlgid,'1961','interger',tipoControl)
    mbusWrite(dlgid,'1978','interger',referencia)
    ### ENTRADAS ANALOGICAS
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
    
    ### ENTRADAS DE PULSOS
    mbusWrite(dlgid,'1950','interger',CNT0_timeOn)
    mbusWrite(dlgid,'1951','interger',CNT0_timeOff)
    mbusWrite(dlgid,'1952','float',CNT0_magpp)
    mbusWrite(dlgid,'1966','interger',CNT1_timeOn)
    mbusWrite(dlgid,'1967','interger',CNT1_timeOff)
    mbusWrite(dlgid,'1964','float',CNT1_magpp)
    
    ### SALIDAS ANALOGIAS
    mbusWrite(dlgid,'1974','float',AO0_Mmin)
    mbusWrite(dlgid,'1976','float',AO0_Mmax)
    mbusWrite(dlgid,'1972','interger',AO0_OutMmin)
    mbusWrite(dlgid,'1973','interger',AO0_OutMmax)
    
    ### TEMPORIZADORES
    mbusWrite(dlgid,'1982','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T1_Enable == True),int(T2_Enable == True),int(T3_Enable == True),int(T4_Enable == True),int(T5_Enable == True),int(T6_Enable == True),int(T7_Enable == True),int(DS_Enable == True)),2))
    mbusWrite(dlgid,'1983','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T1_weekMon == True),int(T1_weekTues == True),int(T1_weekWend == True),int(T1_weekThurs == True),int(T1_weekFrid == True),int(T1_weekSat == True),int(T1_weekSund == True),0),2))
    mbusWrite(dlgid,'1984','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T2_weekMon == True),int(T2_weekTues == True),int(T2_weekWend == True),int(T2_weekThurs == True),int(T2_weekFrid == True),int(T2_weekSat == True),int(T2_weekSund == True),0),2))
    mbusWrite(dlgid,'1985','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T3_weekMon == True),int(T3_weekTues == True),int(T3_weekWend == True),int(T3_weekThurs == True),int(T3_weekFrid == True),int(T3_weekSat == True),int(T3_weekSund == True),0),2))
    mbusWrite(dlgid,'1986','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T4_weekMon == True),int(T4_weekTues == True),int(T4_weekWend == True),int(T4_weekThurs == True),int(T4_weekFrid == True),int(T4_weekSat == True),int(T4_weekSund == True),0),2))
    mbusWrite(dlgid,'1987','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T5_weekMon == True),int(T5_weekTues == True),int(T5_weekWend == True),int(T5_weekThurs == True),int(T5_weekFrid == True),int(T5_weekSat == True),int(T5_weekSund == True),0),2))
    mbusWrite(dlgid,'1988','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T6_weekMon == True),int(T6_weekTues == True),int(T6_weekWend == True),int(T6_weekThurs == True),int(T6_weekFrid == True),int(T6_weekSat == True),int(T6_weekSund == True),0),2))
    mbusWrite(dlgid,'1989','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(T7_weekMon == True),int(T7_weekTues == True),int(T7_weekWend == True),int(T7_weekThurs == True),int(T7_weekFrid == True),int(T7_weekSat == True),int(T7_weekSund == True),0),2))
    mbusWrite(dlgid,'1990','interger',int('{7}{6}{5}{4}{3}{2}{1}{0}'.format(int(DS_weekMon == True),int(DS_weekTues == True),int(DS_weekWend == True),int(DS_weekThurs == True),int(DS_weekFrid == True),int(DS_weekSat == True),int(DS_weekSund == True),0),2))
    mbusWrite(dlgid,'1991','interger',T1_StartHour)
    mbusWrite(dlgid,'1992','interger',T1_StartMin)
    mbusWrite(dlgid,'1993','interger',T1_StopHour)
    mbusWrite(dlgid,'1994','interger',T1_StopMin)
    mbusWrite(dlgid,'1995','interger',T2_StartHour)
    mbusWrite(dlgid,'1996','interger',T2_StartMin)
    mbusWrite(dlgid,'1997','interger',T2_StopHour)
    mbusWrite(dlgid,'1998','interger',T2_StopMin)
    mbusWrite(dlgid,'1999','interger',T3_StartHour)
    mbusWrite(dlgid,'2000','interger',T3_StartMin)
    mbusWrite(dlgid,'2001','interger',T3_StopHour)
    mbusWrite(dlgid,'2002','interger',T3_StopMin)
    mbusWrite(dlgid,'2003','interger',T4_StartHour)
    mbusWrite(dlgid,'2004','interger',T4_StartMin)
    mbusWrite(dlgid,'2005','interger',T4_StopHour)
    mbusWrite(dlgid,'2006','interger',T4_StopMin)
    mbusWrite(dlgid,'2007','interger',T5_StartHour)
    mbusWrite(dlgid,'2008','interger',T5_StartMin)
    mbusWrite(dlgid,'2009','interger',T5_StopHour)
    mbusWrite(dlgid,'2010','interger',T5_StopMin)
    mbusWrite(dlgid,'2011','interger',T6_StartHour)
    mbusWrite(dlgid,'2012','interger',T6_StartMin)
    mbusWrite(dlgid,'2013','interger',T6_StopHour)
    mbusWrite(dlgid,'2014','interger',T6_StopMin)
    mbusWrite(dlgid,'2015','interger',T7_StartHour)
    mbusWrite(dlgid,'2016','interger',T7_StartMin)
    mbusWrite(dlgid,'2017','interger',T7_StopHour)
    mbusWrite(dlgid,'2018','interger',T7_StopMin)
    mbusWrite(dlgid,'2019','interger',DS_StartHour)
    mbusWrite(dlgid,'2020','interger',DS_StartMin)
    mbusWrite(dlgid,'2021','interger',DS_StopHour)
    mbusWrite(dlgid,'2022','interger',DS_StopMin)

    
    # REFERENCIA REMOTA
    mbusWrite(dlgid,'2055','float',Ref1Fact)
    mbusWrite(dlgid,'2047','float',Ref1OffSet)
    mbusWrite(dlgid,'2057','float',Ref2Fact)
    mbusWrite(dlgid,'2049','float',Ref2OffSet)
    mbusWrite(dlgid,'2035','float',Ref1MinValue)
    mbusWrite(dlgid,'2037','float',Ref1MaxValue)
    mbusWrite(dlgid,'2039','float',Ref2MinValue)
    mbusWrite(dlgid,'2041','float',Ref2MaxValue)

    ### PROTECCIONES
    mbusWrite(dlgid,'1925','interger',int('{2}{1}{0}'.format(int(AI0_Enab == True),int(AI1_Enab == True),int(Prot1_Enable == True)),2))
    mbusWrite(dlgid,'2059','float',Prot1_Stop)
    mbusWrite(dlgid,'1979','interger',Prot1_Ref)
    mbusWrite(dlgid,'2061','float',Prot1_Recover)
    







