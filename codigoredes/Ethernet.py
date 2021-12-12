from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from collections import namedtuple
import operator
from ipaddress import IPv4Address


Router = namedtuple('Router', ['destination_host', 'management_ip'])




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
def comandos_router_telnet(ip):

    device = {
        'device_type': 'cisco_ios_telnet',
        'host': ip,
         'username':'cisco',
        'password': 'cisco'
    }
    
    commands=['conf t',
    'enable secret 1234',
     "crypto key generate rsa 1024",
    #'ip ssh rsa keypair-name sshkey',
    #'crypto key generate rsa usage-keys label sshkey modulus 1024',
    'ip ssh v 2',
    'ip ssh authentication-retries 3',
    'line vty 0 15',
    'login local',
    'transport input ssh',
    'exit',
    'exit'
    ]
    
    try:
       
        with ConnectHandler(**device) as telnet:
            telnet.enable()
            resultado=telnet.send_config_set(commands)
            telnet.disconnect()
            #return telnet.send_command('show cdp neighbors detail', use_textfsm=True)
            return resultado  
    except NetmikoAuthenticationException:
        print('Authentication error')
    except NetmikoTimeoutException:
        print('Timeout error')
    except Exception as e:
        print(e)   
    
#Funcion para activar SSH y RSA con RIP provisional        


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
            #print(vecinos)
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
            #print(pila_routers)
            rutas_para_router_vecino=[]
            print("paso 3")
            for i in lista_rutas:
                posicionDiv=i.find("/")
                ruta=i[0:posicionDiv]
                rutas_para_router_vecino.append(ruta)
                normal_crear_RIP(ruta,router_analisar.management_ip)
            print("paso 4")
            for vecino in vecinos:               
                crear_conexion_RIP(router_analisar.management_ip,vecino['management_ip'],rutas_para_router_vecino)
                 
        print(routers_visitados)
        for router in routers_visitados:
            comandos_router_telnet(router.management_ip)       
                  
            
        
    except Exception as e:
        print(e)

   
if __name__ == '__main__':
    activar_SSH_and_RSA()
    
    
    
