import paramiko,getpass,time


username="cisco"
password="cisco"
max_buffer=65535

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

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
                		
