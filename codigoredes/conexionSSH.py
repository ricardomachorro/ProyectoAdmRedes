import paramiko,getpass,time,telnetlib


username="cisco"
password="cisco"
max_buffer=65535

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)
"""     
def conectarSSHandRSA(ip):
    user='cisco'
    password='cisco'
    tn=telnetlib.Telnet(ip)
    tn.read_until(b"Username:")
    tn.write(user.encode('ascii')+b"\n")
    print("paso")
    tn.write(password.encode('ascii')+b"\n")
    tn.write(b"enable\n")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"conf t\n")
    tn.write(b"enable secret 1234 \n")
    tn.write(b"ip ssh rsa keypair-name sshkey \n")
    tn.write(b"crypto key generate rsa usage-keys label sshkey modulus 1024 \n")
    tn.write(b"ip ssh v 2 \n")
    tn.write(b"ip ssh time-out 30\n")
    tn.write(b"ip ssh authentication-retries 3\n")
    tn.write(b"transport input ssh telnet\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")"""

#Crear una ruta rip con ip del router y direccion de ruta
def crear_rutaRIP(nombre_ruta,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("nuevaRedRIP.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==4:
                line=line.format(direccion=nombre_ruta)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
 
#Crear una ruta ospf con ip del router, numero del proceso, direccion de ruta, wildcard de la rutay area
def crear_rutaOSPF(procesoID,direccionRed,wildCard,areaID,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("nuevaRedOSPF.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                line=line.format(processIDOSPF=procesoID)
            elif contadorLineaArchivo==3:
                line=line.format(networkOSPF=direccionRed,wildcardOSPF=wildCard,areaIDOSPF=areaID)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
    
#Crear una ruta rip con ip del router,direccion de ruta, wildcard de la ruta y numero de ruta    
def crear_rutaEIGRP(numAuto,direccionRed,wildCard,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("nuevaRedEIGRP.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                line=line.format(numAutoEIGRP=numAuto)
            elif contadorLineaArchivo==3:
                line=line.format(direccionRedEIGRP=direccionRed,wildcardEIGRP=wildCard)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
 
#Crear un usuario dentro de la topologia con nombre, nivel de permiso, contra e ip del router donde se crea el usuario 
def crear_usuario_topologia_ssh(nombre_ssh,contra_ssh,nivel_ssh,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("nuevoUsuarioTopologia.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                line=line.format(nombre_dato_ssh=nombre_ssh,nivel_dato_ssh=nivel_ssh,contra_dato_ssh=contra_ssh)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
 
#ELimina un usuario del ip del router donde esta el usuario  
def eliminar_usuario_topologia_ssh(nombre_ssh,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("eliminarUsuarioTopologia.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                line=line.format(nombre_dato_ssh=nombre_ssh)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()


#Cambia un usuario dentro de la topologia con nombre, nivel de permiso, contra e ip del router donde estael usuario 
def cambiar_usuario_topologia_ssh(nombre_ssh,contra_ssh,nivel_ssh,ip):
    contadorLineaArchivo=0
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("cambiarUsuarioTopologia.txt","r") as file:
        for line in file:
            contadorLineaArchivo+=1
            if contadorLineaArchivo==2:
                line=line.format(nombre_dato_ssh=nombre_ssh,nivel_dato_ssh=nivel_ssh,contra_dato_ssh=contra_ssh)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()

#Activar rip defualt en router con ip especifico    
def activar_rip_default_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("activarRIPdefault.txt","r") as file:
        for line in file:
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()


#Descativar todos los protocolos default menos rip en un router con ip especifico  
def quitar_menos_RIP_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("desactivarMenosRIP.txt","r") as file:
        for line in file:
            print(line)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()


#Activar ospf default en router con ip especifico  
def activar_ospf_default_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("activarOSPFdefault.txt","r") as file:
        for line in file:
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()


#Descativar todos los protocolos default menos ospf en un router con ip especifico  
def quitar_menos_OSPF_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("desactivarMenosOSPF.txt","r") as file:
        for line in file:
            print(line)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()

#Activar eigrp default en router con ip especifico 
def activar_eigrp_default_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("activarEIGRPdefault.txt","r") as file:
        for line in file:
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()


#escativar todos los protocolos default menos eigrp en un router con ip especifico  
def quitar_menos_EIGRP_ssh(ip):
    connection=paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    connection.connect(ip,username=username,password=password,look_for_keys=False,allow_agent=False)
    new_connection=connection.invoke_shell()
    output=clear_buffer(new_connection)
    time.sleep(2)
    with open("desactivarMenosEIGRP.txt","r") as file:
        for line in file:
            print(line)
            new_connection.send(line.rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
