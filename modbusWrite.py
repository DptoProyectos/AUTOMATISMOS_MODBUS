#!/usr/aut_env/bin/python3.8
'''
FUNCION PARA EL ENVIO DE REGISTROS MODBUS AL DATALOGGER

Created on 16 mar. 2020 

@author: Yosniel Cabrera

Version 1.0.0 16-12-2021 09:11
''' 

from datetime import datetime


def mbusWrite(dlgid='',register='',dataType='',value=''):
    '''
        FLOWCHART -> https://drive.google.com/file/d/191gir1No6tSEBDgU3e76ekZJqHQl5jET/view?usp=sharing
        
        funcion que implementa una cola en donde existe en buffer de transmisión que se puede llenar hasta cubrir el ancho de cirta ventana.
        el resto de los bytes que quedan por fuera de la ventana se insertan en una cola FIFO si no existen en la misma. En caso de que existan tanto en 
        el buffer de tx como en la cola serán actualizados.
        EX:
            mbusWrite(self.DLGID_CTRL,'2097','interger',105)
    '''
    # Dependencias
    import redis
    from spy_config import Config
    from spy_log import log

    # Definición de ventanas de buffers de transmisión
    windowsFirmNuevo = 8
    windowsFirmViejo = 3

    # parametros usados en el firmware nuevo
    MbusSlave = 2
    NumberOfReg2Read = 1    if dataType == 'interger' else 2
    dataTypeNew = 'I16'     if dataType == 'interger' else 'FLOAT'
    dataCodec = 'C1032'
    
    # parametros usados en el firmware viejo
    dataType = 'I'          if dataType == 'interger' else 'F'
   
    # funciones auxiliares
    def lst2str(list):
        '''
            Convierto de lista a string
              EX:
                string = lst2str(['print_log', True, 'DLGID_CTRL', 'MER001'])
                >> string = print_log,True,DLGID_CTRL,MER001
        '''
        my_str = str(list[0])
        n = 0
        for param in list:
            if n < (len(list)-1): 
                n += 1
                my_str = "{my_str},{list}".format(my_str=my_str, list=str(list[n]))
        return my_str

    def getRegistersInfo(redisKey):
        '''
            Obtiene la info de los registros del string almacenado en redisKey y la devuelve en un dict.
        '''
        try:
            RegistersInfo = rh.hget(dlgid,redisKey).decode()
            RegistersInfo = lst2str(RegistersInfo.split("["))
            RegistersInfo = lst2str(RegistersInfo.split("]"))
            lstRegistersInfo = RegistersInfo.split(",")
                    
            # limpio la lista lstLastBROADCAST de elementos vacios
            for element in lstRegistersInfo:
                if element == '': lstRegistersInfo.remove('') 

            if redisKey == 'MODBUS' or redisKey == 'lastMODBUS':
                # extraigo la informacion que contiene el formato del firmware viejo
                n = 0
                lstRegisters = []
                lstDataType = []
                lstValues = []
                for element in lstRegistersInfo:
                    lstRegisters.append(lstRegistersInfo[n])
                    lstDataType.append(lstRegistersInfo[n+1])
                    lstValues.append(lstRegistersInfo[n+2])
                    n += 3
                    if n >= len(lstRegistersInfo): break
                return dict(lstRegisters=lstRegisters,lstDataType=lstDataType,lstValues=lstValues)
            else:
                # extraigo la informacion que contiene el formato del firmware nuevo
                n = 0
                lstMbusSlave = []
                lstRegisters = []
                lstNumberOfReg2Read = []
                lstDataType = []
                lstdataCodec = []
                lstValues = []
                for element in lstRegistersInfo:
                    lstMbusSlave.append(lstRegistersInfo[n])
                    lstRegisters.append(lstRegistersInfo[n+1])
                    lstNumberOfReg2Read.append(lstRegistersInfo[n+2])
                    lstDataType.append(lstRegistersInfo[n+4])
                    lstdataCodec.append(lstRegistersInfo[n+5])
                    lstValues.append(lstRegistersInfo[n+6])
                    n += 7
                    if n >= len(lstRegistersInfo): break

                return dict(lstMbusSlave=lstMbusSlave,lstRegisters=lstRegisters,lstNumberOfReg2Read=lstNumberOfReg2Read,lstDataType=lstDataType,lstdataCodec=lstdataCodec,lstValues=lstValues)
        except:
            return False

    def makeFrame2Send(RegistersInfo):
        '''
            # le entra un diccionario con los datos de los registros y devulve el frame a escribir para el envio de los registros modbus al datalogger con el firmware nuevo o viejo según la info que se le pase en el dict.
        '''
        try:
            # formato para el firmware nuevo
            n = 0
            format4FirmwNew = ''
            for register in RegistersInfo['lstRegisters']:
                if n == 0: 
                    format4FirmwNew = "[{0},{1},{2},16,{3},{4},{5}]".format(RegistersInfo['lstMbusSlave'][n],register,RegistersInfo['lstNumberOfReg2Read'][n],RegistersInfo['lstDataType'][n],RegistersInfo['lstdataCodec'][n],RegistersInfo['lstValues'][n])
                else: 
                    format4FirmwNew = "{0}[{1},{2},{3},16,{4},{5},{6}]".format(format4FirmwNew,RegistersInfo['lstMbusSlave'][n],register,RegistersInfo['lstNumberOfReg2Read'][n],RegistersInfo['lstDataType'][n],RegistersInfo['lstdataCodec'][n],RegistersInfo['lstValues'][n])
                n += 1
            return format4FirmwNew
        except:
            # formato para el firmware viejo
            n = 0
            format4FirmwOld = ''
            for register in RegistersInfo['lstRegisters']:
                if n == 0: 
                    format4FirmwOld = "[{0},{1},{2}]".format(register,RegistersInfo['lstDataType'][n],RegistersInfo['lstValues'][n])
                else: 
                    format4FirmwOld = "{0}[{1},{2},{3}]".format(format4FirmwOld,register,RegistersInfo['lstDataType'][n],RegistersInfo['lstValues'][n])
                n += 1
            return format4FirmwOld

    def scrollWindows(RegistersInfo,win):
        '''
            toma el diccionario de entrada y le pasa una ventana deslizante para obtener dos diccionarios a la salida. Uno que esté dentro de la ventana y otro que queda fueraa de la misma
        '''
        try:
            # Formato para firmwares nuevos
            reg2send  = dict(lstMbusSlave = [], lstRegisters = [], lstNumberOfReg2Read = [], lstDataType = [], lstdataCodec = [], lstValues= [])
            reg2save  = dict(lstMbusSlave = [], lstRegisters = [], lstNumberOfReg2Read = [], lstDataType = [], lstdataCodec = [], lstValues= [])
            n = 0
            for register in RegistersInfo['lstRegisters']:
                if n < win:
                    reg2send['lstMbusSlave'].append(RegistersInfo['lstMbusSlave'][n])
                    reg2send['lstRegisters'].append(register)
                    reg2send['lstNumberOfReg2Read'].append(RegistersInfo['lstNumberOfReg2Read'][n])
                    reg2send['lstDataType'].append(RegistersInfo['lstDataType'][n])
                    reg2send['lstdataCodec'].append(RegistersInfo['lstdataCodec'][n])
                    reg2send['lstValues'].append(RegistersInfo['lstValues'][n])
                else:
                    reg2save['lstMbusSlave'].append(RegistersInfo['lstMbusSlave'][n])
                    reg2save['lstRegisters'].append(register)
                    reg2save['lstNumberOfReg2Read'].append(RegistersInfo['lstNumberOfReg2Read'][n])
                    reg2save['lstDataType'].append(RegistersInfo['lstDataType'][n])
                    reg2save['lstdataCodec'].append(RegistersInfo['lstdataCodec'][n])
                    reg2save['lstValues'].append(RegistersInfo['lstValues'][n])
                n += 1
        except:
            # Formato para firmwares viejos
            reg2send  = dict(lstRegisters = [], lstDataType = [], lstValues= [])
            reg2save  = dict(lstRegisters = [], lstDataType = [], lstValues= [])
            n = 0
            for register in RegistersInfo['lstRegisters']:
                if n < win:
                    reg2send['lstRegisters'].append(register)
                    reg2send['lstDataType'].append(RegistersInfo['lstDataType'][n])
                    reg2send['lstValues'].append(RegistersInfo['lstValues'][n])
                else:
                    reg2save['lstRegisters'].append(register)
                    reg2save['lstDataType'].append(RegistersInfo['lstDataType'][n])
                    reg2save['lstValues'].append(RegistersInfo['lstValues'][n])
                n += 1
        return reg2send,reg2save
        
    def writeFrameIn(Frame2SendReg,redisKey):
        '''
            escribo el redisKey con el buffer o el tailFIFO el Frame2SendReg bajo ciertas condiciones.
        '''
        if redisKey == 'BROADCAST':
            if Frame2SendReg: 
                rh.hset(dlgid,redisKey,Frame2SendReg)
        elif redisKey == 'lastBROADCAST':
            if Frame2SendReg:
                rh.hset(dlgid,redisKey,Frame2SendReg)  
            else:
                rh.hdel(dlgid,redisKey) 
        elif redisKey == 'MODBUS':
            if Frame2SendReg: 
                rh.hset(dlgid,redisKey,Frame2SendReg)
        elif redisKey == 'lastMODBUS':
            if Frame2SendReg:
                rh.hset(dlgid,redisKey,Frame2SendReg)  
            else:
                rh.hdel(dlgid,redisKey)

    def appEndReg(RegistersInfo,Desable):
        '''
            añado al final de la cola el registro actual si Desable is False
        '''
        if not Desable:
            try:
                # anado los valores nuevos que se quieren poner para el formato del firmware nuevo
                RegistersInfo['lstMbusSlave'].append(MbusSlave)
                RegistersInfo['lstRegisters'].append(register)
                RegistersInfo['lstNumberOfReg2Read'].append(NumberOfReg2Read)
                RegistersInfo['lstDataType'].append(dataTypeNew)
                RegistersInfo['lstdataCodec'].append(dataCodec)
                RegistersInfo['lstValues'].append(value)
            except:
                # anado los valores nuevos que se quieren poner para el formato del firmware viejo
                RegistersInfo['lstRegisters'].append(register)
                RegistersInfo['lstDataType'].append(dataType)
                RegistersInfo['lstValues'].append(value)
        return RegistersInfo

    def IsExist(redisKey):
        '''
            se detecta si existe el redisKey devolviendo true or false
        '''
        if rh.hexists(dlgid,redisKey) == 1: return True
        else: return False

    def IsRedisConnected(host='192.168.0.8', port='6379', db='0'):
        '''
            se conecta con la RedisDb y devuelve el objeto rh asi como el estado de la conexion
        '''
        try:
            rh = redis.Redis(host, port, db)
            return True,rh
        except Exception as err_var:
            log(module=__name__, function='__init__', dlgid=dlgid, msg='Redis init ERROR !!')
            log(module=__name__, function='__init__', dlgid=dlgid, msg='EXCEPTION {}'.format(err_var))
            return False,''

    def IsNull(key):
        '''
            detecta si key tiene el valor NUL. En caso de que lo tenga ejecuta una limpieza
        '''
        try:
            if rh.hget(dlgid,key).decode() == 'NUL':
                if key == 'BROADCAST':
                    if rh.exists(dlgid,'MODBUS'): rh.hdel(dlgid,'MODBUS')
                    if rh.exists(dlgid,'lastMODBUS'): rh.hdel(dlgid,'lastMODBUS')
                elif key == 'MODBUS':
                    if rh.exists(dlgid,'BROADCAST'): rh.hdel(dlgid,'BROADCAST')
                    if rh.exists(dlgid,'lastBROADCAST'): rh.hdel(dlgid,'lastBROADCAST')
                return True
            else:
                return False
        except:
            return True

    def IsExisting(key):
        '''
            verifica si existe key. Restorna True en caso positivo y False en caso negativo
        '''
        try:
            if rh.hexists(dlgid,key):
                return True
            else:
                return False
        except:
            return False

    def updateReg(RegistersInfo):
        '''
            Actualiza el RegistersInfo que se le pasa como parametro en caso de que el registro actual este contenido en el mismo.
            Se devuelve el diccionario actualizado y un parametro adicional que dice si se realizo actualizacion o no
        '''
        if register in RegistersInfo['lstRegisters']:
            registerIndex = RegistersInfo['lstRegisters'].index(register)               # obtengo la ubicacion del registro a actualizar
            try:
                # para los firmwares nuevos
                RegistersInfo['lstMbusSlave'][registerIndex] = MbusSlave
                RegistersInfo['lstNumberOfReg2Read'][registerIndex] = NumberOfReg2Read
                RegistersInfo['lstdataCodec'][registerIndex] = dataCodec
                RegistersInfo['lstDataType'][registerIndex] = dataTypeNew
                RegistersInfo['lstValues'][registerIndex] = value
            except:
                # para los firmwares viejos
                RegistersInfo['lstDataType'][registerIndex] = dataType
                RegistersInfo['lstValues'][registerIndex] = value
            Updated = True
        else:
            Updated = False
        return RegistersInfo, Updated

    # main program
    #redisConnection,rh = IsRedisConnected(host=Config['REDIS']['host'], port=Config['REDIS']['port'], db=Config['REDIS']['db'])
    redisConnection,rh = IsRedisConnected()
    if redisConnection:
        if register:
            # para firmwares nuevos
            if IsExist('BROADCAST'):                                                                                
                
                if IsNull('BROADCAST'):
                    
                    if IsExisting('lastBROADCAST'):
                        
                        dictLastBROADCAST = getRegistersInfo('lastBROADCAST')                                       
                        
                        dictLastBROADCAST,IsUpdated = updateReg(dictLastBROADCAST)                                  
                        
                        dictLastBROADCAST = appEndReg(dictLastBROADCAST,IsUpdated)                                  
                        
                        RegistersInfo2Send, RegistersInfo2Save = scrollWindows(dictLastBROADCAST,windowsFirmNuevo)        
                        
                        Frame2SendRegFirmwNew = makeFrame2Send(RegistersInfo2Send)                                  
                        
                        Frame2SaveRegFirmwNew = makeFrame2Send(RegistersInfo2Save)                                  
                        
                        writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST')                                              
                        
                        writeFrameIn(Frame2SaveRegFirmwNew,'lastBROADCAST') 

                    else:
                        
                        Frame2SendRegFirmwNew = makeFrame2Send(dict(lstMbusSlave=[MbusSlave],lstRegisters=[register],lstNumberOfReg2Read=[NumberOfReg2Read],lstDataType=[dataTypeNew],lstdataCodec=[dataCodec],lstValues=[value]))
                        
                        writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST')                                             
                else:
                    
                    if IsExisting('lastBROADCAST'):
                        
                        dictBROADCAST = getRegistersInfo('BROADCAST')                                               
                        
                        dictBROADCAST,IsUpdatedBROADCAST = updateReg(dictBROADCAST)                                 
                        
                        if not IsUpdatedBROADCAST:
                            
                            dictLastBROADCAST = getRegistersInfo('lastBROADCAST')                                   
                            
                            dictLastBROADCAST,IsUpdatedlastBroadCast = updateReg(dictLastBROADCAST)                 
                            
                            dictLastBROADCAST = appEndReg(dictLastBROADCAST,IsUpdatedlastBroadCast)
                            
                            Frame2SaveRegFirmwNew = makeFrame2Send(dictLastBROADCAST)
                            
                            writeFrameIn(Frame2SaveRegFirmwNew,'lastBROADCAST') 
                        
                        else:
                            
                            Frame2SendRegFirmwNew = makeFrame2Send(dictBROADCAST)
                            
                            writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST') 
                    
                    else:
                        
                        dictBROADCAST = getRegistersInfo('BROADCAST')
                        
                        dictBROADCAST,IsUpdatedBROADCAST = updateReg(dictBROADCAST)
                        
                        if not IsUpdatedBROADCAST:
                            
                            if len(dictBROADCAST['lstRegisters']) < windowsFirmNuevo:
                                
                                dictBROADCAST = appEndReg(dictBROADCAST,IsUpdatedBROADCAST)
                                
                                Frame2SendRegFirmwNew = makeFrame2Send(dictBROADCAST)
                                
                                writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST')   
                            
                            else:
                                
                                Frame2SaveRegFirmwNew = makeFrame2Send(dict(lstMbusSlave=[MbusSlave],lstRegisters=[register],lstNumberOfReg2Read=[NumberOfReg2Read],lstDataType=[dataTypeNew],lstdataCodec=[dataCodec],lstValues=[value]))
                                
                                writeFrameIn(Frame2SaveRegFirmwNew,'lastBROADCAST')   
                        
                        else:
                            
                            Frame2SendRegFirmwNew = makeFrame2Send(dictBROADCAST)
                            
                            writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST') 
            
            # para fimrwares viejos
            if IsExist('MODBUS'): 
                
                if IsNull('MODBUS'):
                    
                    if IsExisting('lastMODBUS'):
                        
                        dictlastMODBUS = getRegistersInfo('lastMODBUS')                                             
                        
                        dictlastMODBUS,IsUpdated = updateReg(dictlastMODBUS)                                        
                        
                        dictlastMODBUS = appEndReg(dictlastMODBUS,IsUpdated)                                        
                        
                        RegistersInfo2Send, RegistersInfo2Save = scrollWindows(dictlastMODBUS,windowsFirmViejo)           
                        
                        Frame2SendRegFirmwOld = makeFrame2Send(RegistersInfo2Send)                                  
                        
                        Frame2SaveRegFirmwOld = makeFrame2Send(RegistersInfo2Save)                                  
                        
                        writeFrameIn(Frame2SendRegFirmwOld,'MODBUS')                                                 
                        
                        writeFrameIn(Frame2SaveRegFirmwOld,'lastMODBUS')                                            
                    
                    else:
                        
                        Frame2SendRegFirmwOld = makeFrame2Send(dict(lstRegisters=[register],lstDataType=[dataType],lstValues=[value]))
                        
                        writeFrameIn(Frame2SendRegFirmwOld,'MODBUS')                                                
                
                else:
                    
                    if IsExisting('lastMODBUS'):
                        
                        dictMODBUS = getRegistersInfo('MODBUS')                                                     
                        
                        dictMODBUS,IsUpdatedMODBUS = updateReg(dictMODBUS)                                          
                        
                        if not IsUpdatedMODBUS:
                            
                            dictLastMODBUS = getRegistersInfo('lastMODBUS')                                         
                            
                            dictLastMODBUS,IsUpdatedLastMODBUS = updateReg(dictLastMODBUS)                          
                            
                            dictLastMODBUS = appEndReg(dictLastMODBUS,IsUpdatedLastMODBUS)
                            
                            Frame2SaveRegFirmwOld = makeFrame2Send(dictLastMODBUS)
                            
                            writeFrameIn(Frame2SaveRegFirmwOld,'lastMODBUS') 
                        
                        else:
                            
                            Frame2SendRegFirmwOld = makeFrame2Send(dictMODBUS)
                            
                            writeFrameIn(Frame2SendRegFirmwOld,'MODBUS') 
                    
                    else:
                        
                        dictMODBUS = getRegistersInfo('MODBUS')
                        
                        dictMODBUS,IsUpdatedMODBUS = updateReg(dictMODBUS)
                        
                        if not IsUpdatedMODBUS:
                            
                            if len(dictMODBUS['lstRegisters']) < windowsFirmViejo:
                                
                                dictMODBUS = appEndReg(dictMODBUS,IsUpdatedMODBUS)
                                
                                Frame2SendRegFirmwOld = makeFrame2Send(dictMODBUS)
                                
                                writeFrameIn(Frame2SendRegFirmwOld,'MODBUS')   
                            
                            else:
                                
                                Frame2SaveRegFirmwOld = makeFrame2Send(dict(lstRegisters=[register],lstDataType=[dataTypeNew],lstValues=[value]))
                                
                                writeFrameIn(Frame2SaveRegFirmwOld,'lastMODBUS')   
                        
                        else:
                            
                            Frame2SendRegFirmwOld = makeFrame2Send(dictMODBUS)
                            
                            writeFrameIn(Frame2SendRegFirmwOld,'MODBUS') 
                 
        else:
            # para firmwares nuevos
            if IsExist('BROADCAST'):  
                
                if IsNull('BROADCAST'):
                    
                    if IsExisting('lastBROADCAST'):
                        
                        RegistersInfo = getRegistersInfo('lastBROADCAST')                                           
                        
                        RegistersInfo2Send, RegistersInfo2Save = scrollWindows(RegistersInfo,windowsFirmNuevo)            
                        
                        Frame2SendRegFirmwNew = makeFrame2Send(RegistersInfo2Send)                                  
                        
                        Frame2SaveRegFirmwNew = makeFrame2Send(RegistersInfo2Save)                                  
                        
                        writeFrameIn(Frame2SendRegFirmwNew,'BROADCAST')                                              
                        
                        writeFrameIn(Frame2SaveRegFirmwNew,'lastBROADCAST')                                         
            
            # para firmwares viejos
            if IsExist('MODBUS'): 
                
                if IsNull('MODBUS'):
                    
                    if IsExisting('lastMODBUS'):
                        
                        RegistersInfo = getRegistersInfo('lastMODBUS')                                              
                        
                        RegistersInfo2Send, RegistersInfo2Save = scrollWindows(RegistersInfo,windowsFirmViejo)            
                        
                        Frame2SendRegFirmwOld = makeFrame2Send(RegistersInfo2Send)                                  
                        
                        Frame2SaveRegFirmwOld = makeFrame2Send(RegistersInfo2Save)                                  
                        
                        writeFrameIn(Frame2SendRegFirmwOld,'MODBUS')                                                 
                        
                        writeFrameIn(Frame2SaveRegFirmwOld,'lastMODBUS')                                            






'''
mbusWrite('YCHTESTT','2030','interger',30)
mbusWrite('YCHTESTT','2031','float',31)
mbusWrite('YCHTESTT','2032','float',32)
mbusWrite('YCHTESTT','2033','float',33)
mbusWrite('YCHTESTT','2034','float',34)
mbusWrite('YCHTESTT','2035','float',35)
mbusWrite('YCHTESTT','2036','float',36)
mbusWrite('YCHTESTT','2037','float',37)
mbusWrite('YCHTESTT','2038','float',38)
mbusWrite('YCHTESTT','2039','float',39)
mbusWrite('YCHTESTT','2040','float',40)
mbusWrite('YCHTESTT','2041','float',41)
mbusWrite('YCHTESTT','2042','float',42)
mbusWrite('YCHTESTT','2043','float',43)
mbusWrite('YCHTESTT','2044','float',44)
mbusWrite('YCHTESTT','2045','float',45)
mbusWrite('YCHTESTT','2046','float',46)
mbusWrite('YCHTESTT','2047','float',47)
mbusWrite('YCHTESTT','2048','float',48)
mbusWrite('YCHTESTT','2049','float',49)
mbusWrite('YCHTESTT','2050','float',50)'''
#mbusWrite('YCHTESTT','','float',10.2)
  
