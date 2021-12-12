
  
from pysnmp import hlapi    

#Seccion de get
def construct_object_types(listOfOids):
    objectTypes=[]
    for oid in listOfOids:
        objectTypes.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return objectTypes 

def fetch(handler,count):
    res=[]
    
    for i in range (count):
        try:
            error_indication,error_status,error_index,var_binds=next(handler)
            #print(error_status)
            if not error_indication and not error_status:
                items={}
                
                for var_bind in var_binds:
                    items[str(var_bind[0])]=cast(var_bind[1])
                
                res.append(items)
                
            else:
                raise RuntimeError('Got SNMP error:{0}'.format(error_indication)) 
             
        except StopIteration:
            break   
    return res

def cast(val):
    try:
        return int(val)
    except (ValueError,TypeError):
        try:
            return float(val)
        except (ValueError,TypeError):
            try:
                return str(val)
            except (ValueError,TypeError):
                pass
    return val              
       

def get(target,oids,port=161,engine=hlapi.SnmpEngine(),context=hlapi.ContextData()):
    credentials=hlapi.UsmUserData('admin',authKey='12345678',privKey='12345678',
    authProtocol=hlapi.usmHMACSHAAuthProtocol,privProtocol=hlapi.usmDESPrivProtocol)
    handler=hlapi.getCmd(engine,credentials,hlapi.UdpTransportTarget((target,port)),context,*construct_object_types(oids))
    return fetch(handler,1)[0]



   
def retornar_nombreHost(ipDestino):
    dicNombreHost=get(ipDestino,['1.3.6.1.2.1.1.5.0'])
    return dicNombreHost['1.3.6.1.2.1.1.5.0']

def retornar_Localizacion(ipDestino):
    dicLocalizacion=get(ipDestino,['1.3.6.1.2.1.1.6.0'])
    return dicLocalizacion['1.3.6.1.2.1.1.6.0']

def retornar_Contacto(ipDestino):
    dicContacto=get(ipDestino,['1.3.6.1.2.1.1.4.0'])
    return dicContacto['1.3.6.1.2.1.1.4.0']
    
#Fin seccion get


#Seccion set

def set(target,value_pairs,port=161,engine=hlapi.SnmpEngine(),context=hlapi.ContextData()):
    
    credentials=hlapi.UsmUserData('admin',authKey='12345678',privKey='12345678',
    authProtocol=hlapi.usmHMACSHAAuthProtocol,privProtocol=hlapi.usmDESPrivProtocol)
    handler=hlapi.setCmd(engine,credentials,hlapi.UdpTransportTarget((target,port)),context,*construct_value_pairs(value_pairs))
   
    return fetch(handler,1)[0]
    
def construct_value_pairs(list_of_pairs):
    pairs=[]
    for key, value in list_of_pairs.items():
        pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key),value))
    return pairs
    
    
def set_nombreHost(ipDestino,nombreHost):
    set(ipDestino, {'1.3.6.1.2.1.1.5.0':nombreHost}) 

def set_Localizacion(ipDestino,lugar):
    set(ipDestino, {'1.3.6.1.2.1.1.6.0':lugar}) 

def set_Contacto(ipDestino,lugar):
    set(ipDestino, {'1.3.6.1.2.1.1.4.0':lugar})   

#Seccion get bulk

def get_bulk(target,oids,count,start_from=0,port=161,engine=hlapi.SnmpEngine(),context=hlapi.ContextData()):
    credentials=hlapi.UsmUserData('admin',authKey='12345678',privKey='12345678',
    authProtocol=hlapi.usmHMACSHAAuthProtocol,privProtocol=hlapi.usmDESPrivProtocol)
    handler=hlapi.bulkCmd(engine,credentials,hlapi.UdpTransportTarget((target,port)),context,start_from,count,*construct_object_types(oids))
    
    return fetch(handler,count)


def get_bulk_auto(target,oids,count_oid,start_from=0,port=161,engine=hlapi.SnmpEngine(),context=hlapi.ContextData()):
    credentials=hlapi.UsmUserData('admin',authKey='12345678',privKey='12345678',
    authProtocol=hlapi.usmHMACSHAAuthProtocol,privProtocol=hlapi.usmDESPrivProtocol)
    count=get(target,[count_oid],port,engine,context)[count_oid]
    return get_bulk(target,oids,count,start_from,port,engine,context)
    
#Seccion interfaces
def get_estado_interfaces_router(direccionIp):
    info=get_bulk_auto(direccionIp,['1.3.6.1.2.1.2.2.1.2','1.3.6.1.2.1.2.2.1.7'],'1.3.6.1.2.1.2.1.0')
    diccInterfaces=dict()
    for dato in info:
        print(dato)
        valores=list(dato.values())
        if valores[0]!='Null0':
            diccInterfaces[valores[0]]=valores[1]
    return diccInterfaces

#Paquestes entrada
def get_paquetes_entrada_interfaces(direccionIp):
    info=get_bulk_auto(direccionIp,['1.3.6.1.2.1.2.2.1.2','1.3.6.1.2.1.2.2.1.11'],'1.3.6.1.2.1.2.1.0')
    diccInterfaces=dict()
    for dato in info:
        valores=list(dato.values())
        if valores[0]!='Null0':
            diccInterfaces[valores[0]]=valores[1]
    return diccInterfaces      

#Paquetes salida
def get_paquetes_salida_interfaces(direccionIp):
    info=get_bulk_auto(direccionIp,['1.3.6.1.2.1.2.2.1.2','1.3.6.1.2.1.2.2.1.17'],'1.3.6.1.2.1.2.1.0')
    diccInterfaces=dict()
    for dato in info:
        valores=list(dato.values())
        if valores[0]!='Null0':
            diccInterfaces[valores[0]]=valores[1]
    return diccInterfaces                          

#Paquetes dañados
def get_paquetes_dam_interfaces(direccionIp):    
    info=get_bulk_auto(direccionIp,['1.3.6.1.2.1.2.2.1.2','1.3.6.1.2.1.2.2.1.14'],'1.3.6.1.2.1.2.1.0') 
    diccInterfaces=dict()
    for dato in info:
        valores=list(dato.values())
        if valores[0]!='Null0':
            diccInterfaces[valores[0]]=valores[1]
    return diccInterfaces      
     
if __name__ == '__main__':
    print(get_paquetes_salida_interfaces('192.0.0.2'))
     
   




