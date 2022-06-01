#!/usr/aut_env/bin/python3.8
'''
ENVIO DE CONFIGURACION REMOTA PARA LOS TABLEROS DE CONTROL

@author: Yosniel Cabrera

Version 1.0.1 06-01-2022 17:30
''' 
from datetime import datetime
from __CORE__.modbusWrite import mbusWrite

dlgid  = 'SJPERF001'
regAdd = '1952'
regValue = 0.1

#mbusWrite(dlgid,'1935','interger',100)
mbusWrite(dlgid,regAdd,'float',regValue)
   
