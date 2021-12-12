from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from collections import namedtuple
import operator
from ipaddress import IPv4Address


Router = namedtuple('Router', ['destination_host', 'management_ip'])
#Hacer ping
#Traer router vecinos via telnet
def hacer_ping(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': '10.0.0.254',
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
       
        with ConnectHandler(**device) as telnet:
            resultado=telnet.send_command('ping '+ip, use_textfsm=True)
            telnet.disconnect()  
            return resultado
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)



#Traer interfaz conectada a otra interfaz
def traer_router_interfaz_conectado(ipRouter1,interfaz):
    try:
        listaRouters=traer_router_vecinos(ipRouter1)
        interfazConectada=""
        for router in listaRouters:
            if router["local_port"]==interfaz:
                interfazConectada=router["remote_port"]
                break
        return interfazConectada
    except Exception as e:
        print(e)

#Traer direccion router conectada una interfaz
def traer_ip_interfaz_conectado(ipRouter1,interfaz):
    try:
        listaRouters=traer_router_vecinos(ipRouter1)
        ipRetorno=""
        for router in listaRouters:
            if router["local_port"]==interfaz:
                ipRetorno=router["management_ip"]
                break
        return ipRetorno
    except Exception as e:
        print(e)



#Traer ip rutas routers
def traer_ip_routers():
    try:
        routers_disponibles=traer_routers()
        lista_ip=[]
        for router in routers_disponibles:
            lista_ip.append(router.management_ip)
        return lista_ip
    except Exception as e:
        print(e)

#Eliminar OSPF default
def eliminar_ospf_default(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'username':'cisco',
        'password': 'cisco'
        }
    
    commands=['en',
        'conf t',
        'no router ospf 1',
        'exit'
     ]
    
    try:
        
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            while contador < len(commands):
                telnet.send_command_timing(commands[contador])
                contador=contador+1                          
            telnet.disconnect()    
    except Exception as e:
        print(e)

#Eliminar EIGRP default
def eliminar_EIGRP_default(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'username':'cisco',
        'password': 'cisco'
        }
    
    commands=['en',
        'conf t',
        'no router eigrp 1',
        'exit'
     ]
    
    try:
        
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            
            while contador < len(commands):
                telnet.send_command_timing(commands[contador])
                
                contador=contador+1                          
            telnet.disconnect()      
    except Exception as e:
        print(e)


#Eliminar RIP default
def eliminar_RIP_default(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
        'username':'cisco',
        'password': 'cisco'
        }
    
    commands=['en',
        'conf t',
        'no router rip',
        'exit'
     ]
    
    try:
          
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            while contador < len(commands):
                telnet.send_command_timing(commands[contador])
                contador=contador+1                          
            telnet.disconnect()      
    except Exception as e:
        print(e)

#Eliminar  OSPF y EIGRP default
def excluir_menos_RIP():
    try:
        routers_disponibles=traer_routers()
        for router in routers_disponibles:
            eliminar_ospf_default(router.management_ip)
            eliminar_EIGRP_default(router.management_ip)
    except Exception as e:
        print(e)

#Eliminar  RIP y EIGRP default
def excluir_menos_OSPF():
    try:
        routers_disponibles=traer_routers()
        #print("6")
        for router in routers_disponibles:
            eliminar_EIGRP_default(router.management_ip)
            eliminar_RIP_default(router.management_ip)
        #print("7")
    except Exception as e:
        print(e)

#Eliminar  RIP y OSPF default
def excluir_menos_EIGRP():
    try:
        routers_disponibles=traer_routers()
        for router in routers_disponibles:
            eliminar_ospf_default(router.management_ip)
            eliminar_RIP_default(router.management_ip)
    except Exception as e:
        print(e)

#Traer routers

def traer_routers():
    try:
        main_router=Router('R1','10.0.0.254')
        routers_visitados = [main_router]
        pila_routers=[main_router]
        
        while pila_routers:
            lista_rutas=[]
            router_analisar=pila_routers.pop()
            
            vecinos=traer_router_vecinos(router_analisar.management_ip)
            
            lista_interfaces=traer_tabla_enrutamiento(router_analisar.management_ip)
            for interface in lista_interfaces:
                if interface['protocol']=='C':
                    lista_rutas.append(interface['network']+"/"+interface['mask'] )
            lista_id_routers=list(map(operator.attrgetter('destination_host'),routers_visitados))
            
            for vecino in vecinos:
                if vecino['destination_host'] not in lista_id_routers:
                    pila_routers.append(Router(vecino['destination_host'], vecino['management_ip']))
                    routers_visitados.append(Router(vecino['destination_host'], vecino['management_ip']))
                      
        return routers_visitados
    except Exception as e:
        print(e)


#Hacer conexion de router vecinos con ethernet 
def crear_conexion_RIP(ip,ip_router_agregar,lista_rutas):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    commands=['en',
    'telnet',
    'cisco',
    'cisco',
    'conf t',
    'router rip',
    'version 2',
    'no auto-summary',
    'network',
    'exit',
    'exit',
    'exit'
    ]
    
    try:
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            #print(ip)
            #print(ip_router_agregar)
            #print(lista_rutas)
            while contador < len(commands):
                #print(contador)
                if contador==1:
                    telnet.send_command_timing(commands[contador]+" "+ip_router_agregar)
                elif contador== 8:
                    for i in lista_rutas:
                        telnet.send_command_timing(commands[contador]+" "+i)
                else:
                    telnet.send_command_timing(commands[contador])
                contador=contador+1                          
            telnet.disconnect()     
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)

#Hacer conexion de router vecinos con ethernet 
def crear_conexion_OSPF(ip,ip_router_agregar,lista_rutas,lista_mascaras):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    commands=['en',
    'telnet',
    'cisco',
    'cisco',
    'conf t',
    'router ospf 1',
    'network',
    'exit',
    'exit',
    'exit'
    ]
    
    try:
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            #print(ip)
            #print(ip_router_agregar)
            #print(lista_rutas)
            while contador < len(commands):
                #print(contador)
                if contador==1:
                    telnet.send_command_timing(commands[contador]+" "+ip_router_agregar)
                elif contador== 6:
                    contador_mascara=0
                    for i in lista_rutas:
                        wildcard=str(IPv4Address(int(IPv4Address._make_netmask(lista_mascaras[contador_mascara])[0])^(2**32-1)))
                        telnet.send_command_timing(commands[contador]+" "+i+" "+wildcard+" area 0" )
                        contador_mascara=contador_mascara+1
                else:
                    telnet.send_command_timing(commands[contador])
                contador=contador+1                          
            telnet.disconnect()         
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)

#Hacer conexion de router vecinos con ethernet 
def crear_conexion_EIGRP(ip,ip_router_agregar,lista_rutas,lista_mascaras):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    commands=['en',
    'telnet',
    'cisco',
    'cisco',
    'conf t',
    'router eigrp 1',
    'network',
    'exit',
    'exit',
    'exit'
    ]
    
    try:
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            #print(ip)
            #print(ip_router_agregar)
            #print(lista_rutas)
            while contador < len(commands):
                #print(contador)
                if contador==1:
                    telnet.send_command_timing(commands[contador]+" "+ip_router_agregar)
                elif contador== 6:
                    contador_mascara=0
                    for i in lista_rutas:
                        wildcard=str(IPv4Address(int(IPv4Address._make_netmask(lista_mascaras[contador_mascara])[0])^(2**32-1)))
                        telnet.send_command_timing(commands[contador]+" "+i+" "+wildcard )
                        contador_mascara=contador_mascara+1
                else:
                    telnet.send_command_timing(commands[contador])
                contador=contador+1                          
            telnet.disconnect()     
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)



#crear normal con RIP
def normal_crear_RIP(nombre_ruta,ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
        with ConnectHandler(**device) as telnet:
            contadorLineaArchivo=0
            comandos=[]
            with open("nuevaRedRIP.txt","r") as file:
                for line in file:
                    contadorLineaArchivo+=1
                    if contadorLineaArchivo==4:
                        line=line.format(direccion=nombre_ruta)
                    #print(line)
                    comandos.append(line)
                telnet.send_config_set(comandos)
                    
            telnet.disconnect()       
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)

#crear normal con OSPF
def normal_crear_OSPF(nombre_ruta,ip,areaID,wildCard,procesoID):
    
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
        with ConnectHandler(**device) as telnet:
            contadorLineaArchivo=0
            comandos=[]
            with open("nuevaRedOSPF.txt","r") as file:
                for line in file:
                    contadorLineaArchivo+=1
                    if contadorLineaArchivo==2:
                        line=line.format(processIDOSPF=procesoID)
                    elif contadorLineaArchivo==3:
                        line=line.format(networkOSPF=nombre_ruta,wildcardOSPF=wildCard,areaIDOSPF=areaID)
                    #print(line)
                    comandos.append(line)
                telnet.send_config_set(comandos)
                    
            telnet.disconnect()        
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)


#crear normal con EIGRP
def normal_crear_EIGRP(nombre_ruta,ip,wildCard,numAuto):
    
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
        with ConnectHandler(**device) as telnet:
            contadorLineaArchivo=0
            comandos=[]
            with open("nuevaRedEIGRP.txt","r") as file:
                for line in file:
                    contadorLineaArchivo+=1
                    if contadorLineaArchivo==2:
                        line=line.format(numAutoEIGRP=numAuto)
                    elif contadorLineaArchivo==3:
                        line=line.format(direccionRedEIGRP=nombre_ruta,wildcardEIGRP=wildCard)
                    #print(line)
                    comandos.append(line)
                telnet.send_config_set(comandos)
                    
            telnet.disconnect()      
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)


#Traer tabla de enrutamiento con telnet
def traer_tabla_enrutamiento(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
       
        with ConnectHandler(**device) as telnet:
            resultado=telnet.send_command('show ip route', use_textfsm=True)
            telnet.disconnect()  
            return resultado
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)



#Traer router vecinos via telnet
def traer_router_vecinos(ip):
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    try:
       
        with ConnectHandler(**device) as telnet:
            resultado=telnet.send_command('show cdp neighbors detail', use_textfsm=True)
            telnet.disconnect()  
            return resultado
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)

#Funcion para los comandos del SSH y RSA con telnet 
def rsa_ssh_router(ip):

    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    commands=['en',
    'conf t',
    'ip ssh rsa keypair-name sshkey',
    'crypto key generate rsa usage-keys label sshkey modulus 1024',
    'ip ssh v 2',
    'ip ssh time-out 30',
    'ip ssh authentication-retries 3',
    'username cisco privilege 15 password cisco',
    'line vty 0 15',
    'login local',
    'transport input telnet ssh',
    'exit',
    'exit'
    ]
    
    try:
       
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            contador=0
            while contador < len(commands):
                telnet.send_command_timing(commands[contador])
                contador=contador+1
            #return telnet.send_command('show cdp neighbors detail', use_textfsm=True)
            telnet.disconnect()  
             
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)   


    
#Funcion para activar un protocolo por default 1 para RIP, 2 para OSPF y 3 para EIGRP      


def activar_protocolo_default(num_protocolo):
    try:
        main_router=Router('R1','10.0.0.254')
        routers_visitados = [main_router]
        pila_routers=[main_router]
        while pila_routers:
            lista_rutas=[]
            router_analisar=pila_routers.pop()
            print(router_analisar)
            vecinos=traer_router_vecinos(router_analisar.management_ip)
            print("paso 1")
            lista_interfaces=traer_tabla_enrutamiento(router_analisar.management_ip)
            for interface in lista_interfaces:
                if interface['protocol']=='C':
                    lista_rutas.append(interface['network']+"/"+interface['mask'] )
            lista_id_routers=list(map(operator.attrgetter('destination_host'),routers_visitados))
            print("paso 2")
            for vecino in vecinos:
                if vecino['destination_host'] not in lista_id_routers:
                    pila_routers.append(Router(vecino['destination_host'], vecino['management_ip']))
                    routers_visitados.append(Router(vecino['destination_host'], vecino['management_ip']))
            print(pila_routers)
            rutas_para_router_vecino=[]
            mascaras_para_router_vecino=[]
            print("paso 3")
            #print(lista_rutas)
            for i in lista_rutas:
                posicionDiv=i.find("/")
                ruta=i[0:posicionDiv]
                mascara=i[posicionDiv+1:]
                rutas_para_router_vecino.append(ruta)
                mascaras_para_router_vecino.append(mascara)
                if num_protocolo==1:
                    normal_crear_RIP(ruta,router_analisar.management_ip)
                elif num_protocolo==2:
                    wildcard=str(IPv4Address(int(IPv4Address._make_netmask(mascara)[0])^(2**32-1)))
                    normal_crear_OSPF(ruta,router_analisar.management_ip,0,wildcard,1)
                elif num_protocolo==3:
                    wildcard=str(IPv4Address(int(IPv4Address._make_netmask(mascara)[0])^(2**32-1)))
                    normal_crear_EIGRP(ruta,router_analisar.management_ip,wildcard,1)
                #normal_crear_RIP(ruta,router_analisar.management_ip)
            print("paso 4")
            for vecino in vecinos:
                if num_protocolo==1:
                    crear_conexion_RIP(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino)
                elif num_protocolo==2:
                    crear_conexion_OSPF(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino,mascaras_para_router_vecino)  
                elif num_protocolo==3:
                    crear_conexion_EIGRP(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino,mascaras_para_router_vecino)            
                #crear_conexion_RIP(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino)
        print("paso 5")                
        if num_protocolo==1:
            excluir_menos_RIP()
        elif num_protocolo==2:
            excluir_menos_OSPF()
        elif num_protocolo==3:
            excluir_menos_EIGRP()         
            
        
    except Exception as e:
        print(e)


#Funcion para activar SSH y RSA
def activar_SSH_and_RSA():
    try:
        main_router=Router('R1','10.0.0.254')
        routers_visitados = [main_router]
        pila_routers=[main_router]
        while pila_routers:
            lista_rutas=[]
            router_analisar=pila_routers.pop()
            print(router_analisar)
            vecinos=traer_router_vecinos(router_analisar.management_ip)
            print("paso 1")
            lista_interfaces=traer_tabla_enrutamiento(router_analisar.management_ip)
            for interface in lista_interfaces:
                if interface['protocol']=='C':
                    lista_rutas.append(interface['network']+"/"+interface['mask'] )
            lista_id_routers=list(map(operator.attrgetter('destination_host'),routers_visitados))
            print("paso 2")
            for vecino in vecinos:
                if vecino['destination_host'] not in lista_id_routers:
                    pila_routers.append(Router(vecino['destination_host'], vecino['management_ip']))
                    routers_visitados.append(Router(vecino['destination_host'], vecino['management_ip']))
            print(pila_routers)
            rutas_para_router_vecino=[]
            mascaras_para_router_vecino=[]
            print("paso 3")
            #print(lista_rutas)
            for i in lista_rutas:
                posicionDiv=i.find("/")
                ruta=i[0:posicionDiv]
                mascara=i[posicionDiv+1:]
                rutas_para_router_vecino.append(ruta)
                mascaras_para_router_vecino.append(mascara)
                normal_crear_RIP(ruta,router_analisar.management_ip)
                
                #normal_crear_RIP(ruta,router_analisar.management_ip)
            print("paso 4")
            for vecino in vecinos:
                crear_conexion_RIP(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino)
                
        print("paso 5")                
        for router in routers_visitados:
            print(router.management_ip)
            rsa_ssh_router(router.management_ip)         
            
        
    except Exception as e:
        print(e)

     
if __name__ == '__main__':
    #activar_SSH_and_RSA()
    #activar_protocolo_default(2)
    #print(traer_routers())
    print(traer_ip_interfaz_conectado("192.0.0.2","FastEthernet1/0"))
    
