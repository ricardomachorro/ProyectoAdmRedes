from flask import Flask, render_template, url_for, request, redirect,session,jsonify
from flask_mysqldb import MySQL
from conexionSSH import *
from telnetConexionRSAProtocolos import *
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import MySQLdb
import time
from datetime import datetime
from SNPMprueba import *
from collections import namedtuple
from imagenCreacion import *
DatosInterfaz = namedtuple('DatosInterfaz', ['nombre','paquetes_enviados', 'paquetes_recibidos','paquetes_perdidos','paquetes_dam'])
TablaRouters = namedtuple('TablaRouters', ['nombre','ubicacion', 'contacto'])
TablaInterfaces = namedtuple('TablaInterfaces', ['nombre','nombre_router', 'estado'])
#def print_date_time():
#    print(time.strftime("%A, %d. %B %Y %I:%M;%S %p"))

#scheduler.add_job(func=print_date_time,trigger="interval",seconds=60)

def inicioScheduler():
    i=0

scheduler=BackgroundScheduler({'apscheduler.timezone':'UTC'})
scheduler.add_job(func=inicioScheduler,trigger="interval",seconds=900,id="protocolo")
scheduler.add_job(func=inicioScheduler,trigger="interval",seconds=900,id="interfaces")
atexit.register(lambda:scheduler.shutdown())
scheduler.start()


app=Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='ramv1357'
app.config['MYSQL_DB']='flaskRedes'
mysql=MySQL(app)

def ingresarBitacora(mensaje):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    tiempoActual=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    cur=db.cursor()
    cur.execute('insert into Bitacora (IDUsuario,Momento,Descripcion) values (%s,%s,%s)',
    (session["userID"],tiempoActual,mensaje))
    db.commit()
    db.close()

def ingresarBitacoraAuxiliar(mensaje,identificador):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    tiempoActual=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    cur=db.cursor()
    cur.execute('insert into Bitacora (IDUsuario,Momento,Descripcion) values (%s,%s,%s)',
    (identificador,tiempoActual,mensaje))
    db.commit()
    db.close()




def guardar_router_BD(nombreHost,localizacion,contacto,ip):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute('insert into Dispositivo (NombreHost,Ubicacion,Contacto,Tipo,Estado,DireccionEncontrada) values (%s,%s,%s,%s,%s,%s)',
    (nombreHost,localizacion,contacto,"Router","Activo",ip))
    db.commit()
    listaInterfaces=get_estado_interfaces_router(ip)
    listaPaquetesEntrada=get_paquetes_entrada_interfaces(ip)
    listaPaquetesSalida=get_paquetes_salida_interfaces(ip)
    listaPaquetesDam=get_paquetes_dam_interfaces(ip)
    cur=db.cursor()
    cur.execute("select IDDispositivo from Dispositivo where DireccionEncontrada ='"+ip+"' ")
    IDDispositivo=cur.fetchone()[0]
    db.commit()
    tiempoActual=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    for i in listaInterfaces.keys():
        cur=db.cursor()
        cur.execute('insert into Interfaz (IDDispositivo,Nombre,Estado,PaquetesEnviados,PaquetesRecibidos,PaquetesDa,MomentoRevision) values (%s,%s,%s,%s,%s,%s,%s)',
        (IDDispositivo,i,listaInterfaces[i],listaPaquetesSalida[i],listaPaquetesEntrada[i],listaPaquetesDam[i],tiempoActual))
        db.commit()
    db.close()

def actualizar_router_BD_Activo(nombreHost,localizacion,contacto,ip):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute("update Dispositivo set NombreHost=%s , Ubicacion=%s , Contacto=%s, Estado=%s where DireccionEncontrada='"+ip+"' ",
    (nombreHost,localizacion,contacto,"Activo"))
    db.commit()
    db.close()
    
def actualizar_router_BD_Activo_Normal(nombreHost,localizacion,contacto,ip):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute("update Dispositivo set NombreHost=%s , Ubicacion=%s , Contacto=%s, Estado=%s  where DireccionEncontrada='"+ip+"' ",
    (nombreHost,localizacion,contacto,"Activo"))
    db.commit()
    db.close()

def actualizar_router_BD_Inactivo(ip):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute("update Dispositivo set Estado=%s where DireccionEncontrada='"+ip+"' ",
    ("Inactivo"))
    db.commit()
    db.close()

def cambioDatosRouter(nombre,localizacion,contacto,ip):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute("select * from Dispositivo where DireccionEncontrada ='"+ip+"' ")
    datosRouter=cur.fetchone()
    nombreSQL=datosRouter[1]
    ubicacionSQL=datosRouter[3]
    contactoSQL=datosRouter[4]
    db.commit()
    db.close()
    contadorDiferencias=0
    if nombre!=nombreSQL:
        contadorDiferencias=contadorDiferencias+1
    if localizacion!=ubicacionSQL:
        contadorDiferencias=contadorDiferencias+1
    if contacto!=contactoSQL:
        contadorDiferencias=contadorDiferencias+1
    if contadorDiferencias>0:
        return 1
    else:
        return 0
        
def cambioInterfaz(nombre,estado,idDispositivo):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    cur=db.cursor()
    cur.execute("select * from Interfaz where IDDispositivo ="+str(idDispositivo)+" and Nombre='"+nombre+"'")
   
    estadoSQL=cur.fetchone()[3]
    
    db.commit()
    db.close()
    if int(estadoSQL)!=estado:
        return 1
    else:
        return 0

def alertasInterfaces(idUsuario):
    db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
    lista_routers=traer_routers()
    for i in lista_routers:
        
        cur=db.cursor()
        print(i.management_ip)
        busquedaSecuencia="select count(IDDispositivo) from Dispositivo where DireccionEncontrada ='"+i.management_ip+"' "
        cur.execute(busquedaSecuencia)
        num_of_items=cur.fetchone()[0]
        db.commit()
        if num_of_items==0:
            nombreHost=retornar_nombreHost(i.management_ip)
            localizacion=retornar_Localizacion(i.management_ip)
            contacto=retornar_Contacto(i.management_ip)
            guardar_router_BD(nombreHost,localizacion,contacto,i.management_ip)
    
    cur=db.cursor()
    cur.execute("update Dispositivo set Estado='Inactivo'")
    db.commit()
    
    
    
    for router in lista_routers:
        nombreHost=retornar_nombreHost(router.management_ip)
        localizacion=retornar_Localizacion(router.management_ip)
        contacto=retornar_Contacto(router.management_ip)
        if cambioDatosRouter(nombreHost,localizacion,contacto,router.management_ip)==1:
            ingresarBitacoraAuxiliar("El router "+router.destination_host+" se actualizo con los siguiente datos Nombre:"+nombreHost+",Localizacion:"+localizacion+",Contacto:"+contacto,idUsuario)
        actualizar_router_BD_Activo(nombreHost,localizacion,contacto,router.management_ip)
        
        listaInterfaces=get_estado_interfaces_router(router.management_ip)
        listaPaquetesEntrada=get_paquetes_entrada_interfaces(router.management_ip)
        listaPaquetesSalida=get_paquetes_salida_interfaces(router.management_ip)
        listaPaquetesDam=get_paquetes_dam_interfaces(router.management_ip)
        cur=db.cursor()
        cur.execute("select IDDispositivo from Dispositivo where DireccionEncontrada ='"+router.management_ip+"' ")
        IDDispositivo=cur.fetchone()[0]
        db.commit()    
        tiempoActual=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')  
        for i in listaInterfaces.keys():
            if cambioInterfaz(i,listaInterfaces[i],IDDispositivo)==1:
                ingresarBitacoraAuxiliar("La interfaz "+i+" del dispositivo "+router.destination_host+" cambio al estado "+str(listaInterfaces[i])+"",idUsuario)
            cur=db.cursor()
            cur.execute("update Interfaz set Estado="+str(listaInterfaces[i])+",PaquetesEnviados="+str(listaPaquetesSalida[i])+", PaquetesRecibidos="+str(listaPaquetesEntrada[i])+",PaquetesDa="+str(listaPaquetesDam[i])+", MomentoRevision='"+str(tiempoActual)+"'  where Nombre='"+i+"' and IDDispositivo="+str(IDDispositivo))
            db.commit()
            
    db.close()    
    print("interfaces ok")

#Ping resultado
"""@app.route("/ping_resultado",methods=['POST'])
def ping_resultado():
    if request.method=='POST':
        direccion=request.form["pingDireccion"]
        resultado=hacer_ping(direccion)
        print(resultado)
        return jsonify ({"resultado":resultado})
    return render_template('pingUsuario.html')"""

#Activacion RSA y SSH via telnet
@app.route("/ssh_rsa_activacion")
def ssh_rsa_activacion():
    """listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']"""
    scheduler.remove_job("protocolo")
    scheduler.remove_job("interfaces")
    scheduler.add_job(func=inicioScheduler,trigger="interval",seconds=900,id="protocolo")
    scheduler.add_job(func=inicioScheduler,trigger="interval",seconds=900,id="interfaces")
    activar_SSH_and_RSA()
    ingresarBitacora("El usuario activo RSA y SSH")
    return redirect('/control_usuario_pagina')
    
"""Direccionamiento paginas"""
#Pagina principal
@app.route("/")
def Index():
    return render_template('index.html')

#Direccionameinto pagina de Ping
@app.route("/ping_Usuario")
def ping_Usuario():
    return render_template('pingUsuario.html')

#Direccionamiento pagina de tracert
@app.route("/tracert_Usuario")
def tracert_Usuario():
    return render_template('tracertUsuario.html')

#Datos usuario normal
@app.route("/datos_usuario_pagina_principal")
def datos_usuario_pagina_principal():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    nombre=""
    correo=""
    contra=""
    for user in detallesUsuario:
        nombre=user[1]
        contra=user[2]
        correo=user[3]
    return render_template("paginaPrincipalUsuarioNormal.html",nombre=nombre,contra=contra,correo=correo)

#Direccionamiento para la parte de la bitacora
@app.route("/bitacora")
def ver_bitacora():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Bitacora')
    data=cur.fetchall()
    #print(data)
    return render_template('bitacora.html',registros=data)

#Direccionamiento para la parte de la parte de graficos
@app.route("/grafica")
def ver_grafica():
    hacer_imagen()
    dicIDdispositivos=dict()
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Dispositivo')
    dispositivos=cur.fetchall()
    tablaRouters=[]
    tablaInterfaces=[]
    for dispositivo in dispositivos:
        IDdispositivo=dispositivo[0]
        nombreHost=dispositivo[1]
        ubicacion=dispositivo[3]
        contacto=dispositivo[4]
        dicIDdispositivos[IDdispositivo]=nombreHost
        tablaRouters.append(TablaRouters(nombreHost, ubicacion, contacto))
    cur=mysql.connection.cursor()
    cur.execute('select * from Interfaz')
    interfaces=cur.fetchall()
    for interfaz in interfaces :
        nombreInterfaz=interfaz[2]
        nombreRouter=dicIDdispositivos[interfaz[1]]
        estado=""
        if interfaz[3]=="1":
            estado="levantado"
        else:
            estado="apagado"
        tablaInterfaces.append(TablaInterfaces (nombreInterfaz,nombreRouter, estado))
    return render_template('grafica.html',tablaRouters=tablaRouters,tablaInterfaces=tablaInterfaces)

#Direccionamiento para la parte de la parte de graficos
@app.route("/graficaNormal")
def ver_graficaNormal():
    hacer_imagen()
    dicIDdispositivos=dict()
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Dispositivo')
    dispositivos=cur.fetchall()
    tablaRouters=[]
    tablaInterfaces=[]
    for dispositivo in dispositivos:
        IDdispositivo=dispositivo[0]
        nombreHost=dispositivo[1]
        ubicacion=dispositivo[3]
        contacto=dispositivo[4]
        dicIDdispositivos[IDdispositivo]=nombreHost
        tablaRouters.append(TablaRouters(nombreHost, ubicacion, contacto))
    cur=mysql.connection.cursor()
    cur.execute('select * from Interfaz')
    interfaces=cur.fetchall()
    for interfaz in interfaces :
        nombreInterfaz=interfaz[2]
        nombreRouter=dicIDdispositivos[interfaz[1]]
        estado=""
        if interfaz[3]=="1":
            estado="levantado"
        else:
            estado="apagado"
        tablaInterfaces.append(TablaInterfaces (nombreInterfaz,nombreRouter, estado))
    return render_template('graficaNormal.html',tablaRouters=tablaRouters,tablaInterfaces=tablaInterfaces)



#Direccionamiento para la parte de control de paquetes    
@app.route("/paquetes")
def ver_paquetes():
    listaRouters=traer_routers()
    return render_template('controlPaquetes.html',routers=listaRouters)


#Direccionamiento para la parte de dispositvos con SNPM
@app.route("/cambio_SNPM_Dispositivo/<string:ip>")
def cambio_SNPM_Dispositivo(ip):
    nombreHost=retornar_nombreHost(ip)
    localizacion=retornar_Localizacion(ip)
    contacto=retornar_Contacto(ip)
    return render_template('cambioSNPMDispositivo.html',regresoNombreHost=nombreHost,regresoLocalizacion=localizacion,regresoContacto=contacto,ipDestino=ip)

#Direccionamiento para guardar datos del snmp
@app.route("/guardar_datos_SNPM_Dispositivo/<string:ip>",methods=['POST'])
def guardar_datos_SNPM_Dispositivo(ip):
    if request.method=='POST':
        nombreHost=request.form['nombreHost']
        ubicacion=request.form['ubicacion']
        contacto=request.form['contacto']
        set_nombreHost(ip,nombreHost)
        set_Localizacion(ip,ubicacion)
        set_Contacto(ip,contacto)
        ingresarBitacora("El dispositivo con ip:"+ip+" se le actuliazo sus datos con el siguiente formato nombre host="+nombreHost+" ubicacion:"+ubicacion+",contacto:"+contacto)
        return redirect('/control_snpm_pagina')
    else:
        return render_template('error.html')


#Direccionamiento para la parte de paquetes de un dispositivo en especial    
@app.route("/paquetesDispositivo/<string:ip>")
def paquetes_dispositivo(ip):
    listaInterfaces=get_estado_interfaces_router(ip)
    datosSalidaInterfaces=[]
    for interfaz in listaInterfaces.keys():
        ipRouter2=traer_ip_interfaz_conectado(ip,interfaz)
        interfaz2=traer_router_interfaz_conectado(ip,interfaz)
        if ipRouter2=="":
            pass
        else:
            nombreHost=retornar_nombreHost(ipRouter2)
            listaPaquetesEntrada=get_paquetes_entrada_interfaces(ipRouter2)
            listaPaquetesSalida=get_paquetes_salida_interfaces(ip)            
            paquetesEntradaActual=listaPaquetesEntrada[interfaz2]
            paquetesSalidaActual=listaPaquetesSalida[interfaz]
            db=MySQLdb.connect("localhost","root","ramv1357","flaskRedes")
            cur=db.cursor()
            cur.execute("select IDDispositivo from Dispositivo where DireccionEncontrada ='"+ip+"' ")
            IDDispositivo1=cur.fetchone()[0]
            db.commit()
            cur=db.cursor()
            cur.execute("select IDDispositivo from Dispositivo where NombreHost ='"+nombreHost+"' ")
            IDDispositivo2=cur.fetchone()[0]
            cur=db.cursor()
            cur.execute("select PaquetesRecibidos from Interfaz where IDDispositivo ="+str(IDDispositivo2)+" and Nombre='"+interfaz2+"'")
            paquetesEntradaBD=cur.fetchone()[0]
            db.commit()
            cur=db.cursor()
            cur.execute("select PaquetesEnviados from Interfaz where IDDispositivo ="+str(IDDispositivo1)+" and Nombre='"+interfaz+"'")
            paquetesSalidaBD=cur.fetchone()[0]
            db.commit()
            db.close()
            #print(paquetesSalidaActual)
            #print(paquetesSalidaBD)
            #print(paquetesEntradaActual)
            #print(paquetesEntradaBD)
            paquetesPerdidos=(paquetesSalidaActual-paquetesSalidaBD)-(paquetesEntradaActual-paquetesEntradaBD)
            paquetesEntrada=get_paquetes_entrada_interfaces(ip)[interfaz]
            paquetesSalida=get_paquetes_salida_interfaces(ip)[interfaz]
            paquetesDan=get_paquetes_dam_interfaces(ip)[interfaz]
            datosSalidaInterfaces.append(DatosInterfaz(interfaz,paquetesSalida, paquetesEntrada,paquetesPerdidos,paquetesDan))
            print(paquetesPerdidos)
            
    return render_template('transitoDispositivo.html',interfacesPagina=datosSalidaInterfaces)

#Direccionamiento para la parte de los usaurios dentro de la topologia
@app.route("/control_usuario_pagina")
def control_usuario_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from UsuarioTopologia where not IDUsuarioTopologia=1')
    data=cur.fetchall()
    return render_template('controlUsuario.html',usuarios=data)


#Direccionamiento para la parte de control de protocolos
@app.route ("/control_protocolos")
def control_protocolos():
    return render_template('configuracionProtocolos.html')


#Direccionamiento para la parte de la los usaurios dentro del sistema
@app.route("/usuarios_sistema_pagina")
def usuarios_sistema_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where Nivel="Normal" and Activo="Activo"')
    data=cur.fetchall()
    return render_template('usuarioSistema.html',usuarios=data)


#Direccionamiento para la parte de control de SNPM
@app.route("/control_snpm_pagina")
def control_snpm_pagina():
    listaRouters=traer_routers()
    return render_template('controlSNPM.html',routers=listaRouters)


#Direccionamiento para la configuracion de datos del administrador y del sistema en general(activar RSA,SSH y tiempo de actualizacion topologia)
@app.route("/configuracion_admi_pagina")
def configuracion_admi_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    nombre=""
    correo=""
    contra=""
    for user in detallesUsuario:
        nombre=user[1]
        contra=user[2]
        correo=user[3]
    return render_template('configuracionAdministrador.html',nombreUsuario=nombre,correoUsuario=correo,contraUsuario=contra)

#Direccionamiento para la parte de control de usuarios normal
@app.route("/configuracion_usuario_pagina")
def configuracion_usuario_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    nombre=""
    correo=""
    contra=""
    for user in detallesUsuario:
        nombre=user[1]
        contra=user[2]
        correo=user[3]
    return render_template('configuracionUsuarioNormal.html',nombreUsuario=nombre,correoUsuario=correo,contraUsuario=contra)

#Direccionamiento para la parte de control de SNPM
@app.route("/registro_pagina")
def registro_pagina():
    return render_template('registro.html')


#Direccionamiento para la pagina donde se crea un nuevo usuario del sistema
@app.route("/nuevo_usuario_sistema")
def nuevo_usuario_sistema():
    return render_template('nuevoUsuarioSistema.html')


#Direccionamiento para la pagina donde se crea un nuevo usuario del sistema   
@app.route("/nuevo_usuario_topologia")
def nuevo_usuario_topologia():
    return render_template('nuevoUsuarioTopologia.html')

"""acciones de administracion usuario sistema"""

#Registro de un nuevo usuario normal en el sistema
@app.route("/registro_nuevo_usuario_sistema",methods=['POST'])
def registro_nuevo_usuario_sistema():
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        cur.execute('insert into Usuario (Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values (%s,%s,%s,%s,%s,%s)',
        (nombreUsu,contraUsu,correoUsu,'Normal','Activo',12))
        mysql.connection.commit()
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')


#Cargar datos apra el cambio de datos de usaurio
@app.route("/cambiar_usuario_sistema/<string:id>")
def cambiar_usuario_sistema(id):
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where IDUsuario={0}'.format(id))
    detallesUsuario=cur.fetchall()
    nombre=""
    correo=""
    contra=""
    for user in detallesUsuario:
        nombre=user[1]
        correo=user[3]
        contra=user[2]
    return render_template('cambioUsuarioSistema.html',idUsuario=id,nombreUsuario=nombre,correoUsuario=correo,contraUsuario=contra)



#Guardar cambios de un usuario dentro del sistema
@app.route("/guardar_cambio_usuario_sistema/<string:id>",methods=['POST'])
def guardar_cambio_usuario_sistema(id):
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        cur.execute('update Usuario set Nombre=%s , Contra=%s , Correo=%s where IDUsuario={0}'.format(id),
        (nombreUsu,correoUsu,contraUsu))
        mysql.connection.commit()
        return redirect('/usuarios_sistema_pagina')
    else:
        return  render_template('error.html')


#ELiminar el usuario del sistema
@app.route("/eliminar_usuario_sistema/<string:id>")
def eliminar_usuario_sistema(id):
    cur=mysql.connection.cursor()
    cur.execute('delete from Usuario where IDUsuario={0}'.format(id))
    mysql.connection.commit()
    return redirect('/usuarios_sistema_pagina')


#Guardar cambios de un usuario administrador dentro del sistema
@app.route("/guardar_cambios_configuracion_administrador", methods=['POST'])
def guardar_cambios_configuracion_administrador():
    
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        cur.execute('update Usuario set Nombre=%s , Contra=%s , Correo=%s where IDUsuario={0}'.format(session["userID"]),
        (nombreUsu,contraUsu,correoUsu))
        mysql.connection.commit()
        return redirect('/usuarios_sistema_pagina')
    else:
        return  render_template('error.html')


#Guardar cambios de un usuario normal dentro del sistema
@app.route("/guardar_cambios_configuracion_normal", methods=['POST'])
def guardar_cambios_configuracion_normal():
    
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        cur.execute('update Usuario set Nombre=%s , Contra=%s , Correo=%s where IDUsuario={0}'.format(session["userID"]),
        (nombreUsu,contraUsu,correoUsu))
        mysql.connection.commit()
        ingresarBitacora("Cambio datos del usaurio con el ID:"+str(session["userID"])+" por los siguientes Nombre:"+nombreUsu+",Correo:"+correoUsu+",Contra:"+contraUsu)
        return redirect('/datos_usuario_pagina_principal')
        #return redirect('/ping_Usuario')
    else:
        return  render_template('error.html')


#Registro de usuario administrador
@app.route("/registro_usuario", methods=['POST'])
def registro_usuario():
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        codigoUsu=request.form['codigo']
        cur=mysql.connection.cursor()
        cur.execute('insert into Usuario (Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values (%s,%s,%s,%s,%s,%s)',
        (nombreUsu,contraUsu,correoUsu,'Administrador','Activo',12))
        mysql.connection.commit()
        cur=mysql.connection.cursor()
        resultadoSelect=cur.execute("select * from Usuario where Nombre=%s and Contra=%s",
        (nombreUsu,contraUsu))
        detallesUsuario=cur.fetchall()
        for user in detallesUsuario:
            session["userID"]=user[0]
        mensaje="Registro del usaurio con los siguientes datos (ID:"+str(session["userID"])+",Nombre:"+nombreUsu+",Correo:"+correoUsu+",Contra:"+contraUsu+")"
        ingresarBitacora(mensaje)
        return  render_template('controlUsuario.html')
    else:
        return  render_template('error.html')


#Metodo ingreso de usuario
@app.route('/ingreso_usuario',methods=['POST'])
def ingreso_usuario():
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        resultadoSelect=cur.execute('select * from Usuario where Nombre=%s and Contra=%s',
        (nombreUsu,contraUsu))
        tipoUsuario=0
        if resultadoSelect==1:
            detallesUsuario=cur.fetchall()
            for user in detallesUsuario:
                if user[4]=='Administrador':
                    tipoUsuario=1
                elif user[4]=='Normal':
                    tipoUsuario=2
                session["userID"]=user[0]
          
            
            if tipoUsuario==1:
                ingresarBitacora("Ingreso del usuario con el ID:"+str(session["userID"]))
                return  redirect('/control_usuario_pagina')
            elif tipoUsuario==2:
                ingresarBitacora("Ingreso del usuario con el ID:"+str(session["userID"]))
                return redirect('/datos_usuario_pagina_principal')
                #return  render_template('pingUsuario.html')
            else:
                return  render_template('error.html')
        else:
            return  render_template('error.html')
    else:
        return  render_template('error.html')

#Metodo para cerrar sesion del usuario
@app.route('/salir_sesion')
def salir_sesion():
    session.clear()
    return render_template('index.html')

"""acciones de los usuarios topologia"""
#Registro de usaurio dentro de la topologia
@app.route("/registro_nuevo_usuario_topologia",methods=['POST'])
def registro_nuevo_usuario_topologia():
    if request.method=='POST':
        #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
        listaIP=traer_ip_routers()
        nombreUsu=request.form['nombre']
        nivelUsu=request.form['nivel']
        contraUsu=request.form['contra']
        for i in listaIP:
            crear_usuario_topologia_ssh(nombreUsu,contraUsu,nivelUsu,i)
        cur=mysql.connection.cursor()
        cur.execute('insert into UsuarioTopologia (Nombre,Contra,Nivel) values (%s,%s,%s)',
        (nombreUsu,contraUsu,nivelUsu))
        mysql.connection.commit()
        ingresarBitacora("Se registro un nuevo usuario en la topologia con los siguientes datos Nombre:"+NombreUsu+",Nivel:"+str(nivelUsu)+",Contra:"+contraUsu)
        return redirect('/control_usuario_pagina')
    else:
        return render_template('error.html')


#Eliminar usuario de la topologia
@app.route("/eliminar_usuario_topologia/<string:id>")
def eliminar_usuario_topologia(id):
    #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    listaIP=traer_ip_routers()
    cur=mysql.connection.cursor()
    cur.execute('select Nombre from UsuarioTopologia where IDUsuarioTopologia={0}'.format(id))
    records=cur.fetchall()
    nombreUsuario=""
    for row in records:
        nombreUsuario=row[0]
    print(nombreUsuario)
    for i in listaIP:
        eliminar_usuario_topologia_ssh(nombreUsuario,i)
    cur=mysql.connection.cursor()
    cur.execute('delete from UsuarioTopologia where IDUsuarioTopologia={0}'.format(id))
    mysql.connection.commit()
    return redirect('/control_usuario_pagina')


#Cargar datos del usaurio topologia
@app.route("/cambiar_usuario_topologia/<string:id>")
def cambiar_usuario_topologia(id):
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from UsuarioTopologia where IDUsuarioTopologia={0}'.format(id))
    detallesUsuario=cur.fetchall()
    nombre=""
    contra=""
    nivel=0
    for user in detallesUsuario:
        nombre=user[1]
        contra=user[2]
        nivel=user[3]
        
    return render_template('cambioUsuarioTopologia.html',idUsuario=id,nombreUsuario=nombre,contraUsuario=contra,nivelUsuario=nivel)

#Guardar cambios de un usuario de la topologia
@app.route("/guardar_cambio_usuario_topologia/<string:id>",methods=['POST'])
def guardar_cambio_usuario_topologia(id):
    #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    listaIP=traer_ip_routers()
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from UsuarioTopologia where IDUsuarioTopologia={0}'.format(id))
    detallesUsuario=cur.fetchall()
    nombre=""
    contra=""
    nivel=0
    for user in detallesUsuario:
        nombre=user[1]
        contra=user[2]
        nivel=user[3]
    if request.method=='POST':
        nivelUsuNuevo=request.form['nivelNuevo']
        contraUsuNuevo=request.form['contraNueva']
        for i in listaIP:
            cambiar_usuario_topologia_ssh(nombre,contraUsuNuevo,nivelUsuNuevo,i)
        cur=mysql.connection.cursor()
        cur.execute('update UsuarioTopologia set Contra=%s, Nivel=%s where IDUsuarioTopologia={0}'.format(id),
        (contraUsuNuevo,nivelUsuNuevo))
        mysql.connection.commit()
        return redirect('/control_usuario_pagina')
    else:
        return  render_template('error.html')


"""acciones de los protocolos"""     

#Cambiar configuracion del tiempo de actualizacion de topologia
@app.route('/actualizar_tiempo_topologia',methods=['POST'])
def actulizar_tiempo_topologia():
    if request.method=='POST':
        valorTiempo=request.form['selector_tiempo_actualizacion']
        print(valorTiempo)
        #print(type(valorTiempo))
        cur=mysql.connection.cursor()
        sql_sequence='update Usuario set Actualizacion='+valorTiempo+' where IDUsuario={0}'
        cur.execute(sql_sequence.format(session["userID"]))
        mysql.connection.commit()
        return redirect('/control_usuario_pagina')
    else:
        return redirect('error.html')



   
#Crear una nueva ruta rip
@app.route('/nueva_ruta_rip',methods=['POST'])
def nueva_ruta_rip():
    #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    listaIP=traer_ip_routers()
    if request.method=='POST':
        ruta=request.form['rutaIP']
        for i in listaIP:
            crear_rutaRIP(ruta,i)
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')

#Crear una nueva ruta ospf
@app.route('/nueva_ruta_ospf',methods=['POST'])
def nueva_ruta_ospf():
    #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    listaIP=traer_ip_routers()
    if request.method=='POST':
        processID=request.form['processID']
        direccionRed=request.form['direccionRed']
        wildcard=request.form['wildcard']
        areaID=request.form['areaID']
        for i in listaIP:
            crear_rutaOSPF(processID,direccionRed,wildcard,areaID,i)
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')

#Crear una nueva ruta eigrp
@app.route('/nueva_ruta_eigrp',methods=['POST'])
def nueva_ruta_eigrp():
    #listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    listaIP=traer_ip_routers()
    if request.method=='POST':
        numAuto=request.form['autNum']
        direccionRed=request.form['direccionRed']
        wildcard=request.form['wildcard']
        for i in listaIP:
            crear_rutaEIGRP(numAuto,direccionRed,wildcard,i)
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')

#Activar RIP default
@app.route('/activar_rip_default')
def activar_rip_default():
    """listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_rip_default_ssh(i)
    for i in listaIP:
        quitar_menos_RIP_ssh(i)"""
    scheduler.remove_job("protocolo")
    scheduler.remove_job("interfaces")
    activar_protocolo_default(1)
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select Actualizacion from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    tiempo=10
    for user in detallesUsuario:
        tiempo=user[0]
    tiempo_espera=tiempo*60
    
    scheduler.add_job(func=activar_protocolo_default,args=[1],trigger="interval",seconds=tiempo_espera,id="protocolo")
    
    scheduler.add_job(func=alertasInterfaces,args=[session["userID"]],trigger="interval",seconds=210,id="interfaces")
    
     
    return redirect('/usuarios_sistema_pagina')

#Activar OSPF default
@app.route('/activar_ospf_default')
def activar_ospf_default():
    """listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_ospf_default_ssh(i)
    for i in listaIP:
        quitar_menos_OSPF_ssh(i)"""
    scheduler.remove_job("protocolo")
    scheduler.remove_job("interfaces")
    activar_protocolo_default(2)  
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select Actualizacion from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    tiempo=10
    for user in detallesUsuario:
        tiempo=user[0]
    tiempo_espera=tiempo*60
    
    scheduler.add_job(func=activar_protocolo_default,args=[2],trigger="interval",seconds=tiempo_espera,id="protocolo") 
    scheduler.add_job(func=alertasInterfaces,args=[session["userID"]],trigger="interval",seconds=210,id="interfaces")
    return redirect('/usuarios_sistema_pagina')

#Activar eigrp defualt
@app.route('/activar_eigrp_default')
def activar_eigrp_default():
    """listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_eigrp_default_ssh(i)
    for i in listaIP:
        quitar_menos_EIGRP_ssh(i)"""
    scheduler.remove_job("protocolo")
    scheduler.remove_job("interfaces")
    activar_protocolo_default(3)
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select Actualizacion from Usuario where IDUsuario={0}'.format(session["userID"]))
    mysql.connection.commit()
    detallesUsuario=cur.fetchall()
    tiempo=10
    for user in detallesUsuario:
        tiempo=user[0]
    tiempo_espera=tiempo*60
    
    scheduler.add_job(func=activar_protocolo_default,args=[3],trigger="interval",seconds=tiempo_espera,id="protocolo")
    scheduler.add_job(func=alertasInterfaces,args=[session["userID"]],trigger="interval",seconds=210,id="interfaces")
    return redirect('/usuarios_sistema_pagina')


if __name__=='__main__':
    app.run(port=3000,debug=True)
