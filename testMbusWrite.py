#!/usr/bin/python3 -u

from __CORE__.modbusWrite import mbusWrite
   


# ///////////////////////////////////////////////////////////////////////////////////////////////////

# esto es lo que se tiene cuando el equipo que transmite el dato no es un tanque
dlgid = 'YCHTEST'

list_old_format = []

# cuando el equipo que transmite el dato es un tanque se tiene una lista con todos los equipos a los cuales se quiere transmitir
# list_old_format = [('YCHTEST', '2040', 'float', '2.0')]
# list_old_format = [('YCHTEST', '2032', 'float', '2.0'),('YCHTEST', '2033', 'float', '2.0')]
# list_old_format = [ ('YCHTEST', '2032', 'float', '0.00'), 
#                     ('YCHTEST', '2033', 'float', '1.78'),
#                     ('YCHTEST', '2034', 'float', '1.79'), 
#                     ('YCHTEST', '2035', 'float', '1.78'),
#                     ('YCHTEST', '2036', 'float', '1.79'), 
#                     ('YCHTEST', '2037', 'float', '1.79'), 
#                     ('YCHTEST', '2038', 'float', '1.78'),
#                     ('YCHTEST', '2039', 'float', '1.70'), 
#                     ('YCHTEST', '2040', 'float', '1.78'),
#                     ('YCHTEST', '2041', 'float', '0.00'), 
#                     ('YCHTEST', '2042', 'float', '1.78'),
#                     ('YCHTEST', '2043', 'float', '1.79'), 
#                     ('YCHTEST', '2044', 'float', '1.78'),
#                     ('YCHTEST', '2045', 'float', '1.79'), 
#                     ('YCHTEST', '2046', 'float', '1.79'), 
#                     ('YCHTEST', '2047', 'float', '1.78'),
#                     ('YCHTEST', '2048', 'float', '1.70'), 
#                     ('YCHTEST', '2049', 'float', '1.78')
#                     ]

list_old_format = [ ('SJREGTEST', '1935', 'interger', 101), 
                    ('SJREGTEST', '1934', 'interger', 101),
                    ('SJREGTEST', '1955', 'float', '1.79'), 
                    ('SJREGTEST', '1957', 'float', '1.78'),
                   
                    ]


# llamo a la funcion para escribir el key MODBUS de redis en cada ejecucion del for
for t in list_old_format:
    (dlgid, register, dataType, value) = t

    # mbusWrite(dlgid, None, None, register, dataType, value)
    mbusWrite(dlgid, register, dataType, value)

# # si no hay datos llamo a la funcion por si le queda en cola algo para transmitir
if not list_old_format:
    # print(dlgid)
    mbusWrite(dlgid,'','','','','')
