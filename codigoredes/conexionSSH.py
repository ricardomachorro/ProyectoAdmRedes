import paramiko,getpass,time


username="cisco"
password="cisco"
max_buffer=65535

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

def crear_rutaRIP(nombre_ruta):
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
            new_connection.send(line,rstrip()+"\n")
            time.sleep(2)
            output=new_connection.recv(max_buffer)
            output=clear_buffer(new_connection)
    new_connection.close()
