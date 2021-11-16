from flask import Flask, render_template, url_for, request, redirect,session
from flask_mysqldb import MySQL
from conexionSSH import *

app=Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='ramv1357'
app.config['MYSQL_DB']='flaskRedes'
mysql=MySQL(app)

#Activacion RSA y SSH via telnet
@app.route("/ssh_rsa_activacion")
def ssh_rsa_activacion():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    for i in listaIP:
        conectarSSHandRSA(i)
    return redirect('/control_usuario_pagina')
    
"""Direccionamiento paginas"""
@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/ping_Usuario")
def ping_Usuario():
    return render_template('pingUsuario.html')

@app.route("/tracert_Usuario")
def tracert_Usuario():
    return render_template('tracertUsuario.html')

    
@app.route("/bitacora")
def ver_bitacora():
    return render_template('bitacora.html')

@app.route("/grafica")
def ver_grafica():
    return render_template('grafica.html')
    
@app.route("/paquetes")
def ver_paquetes():
    return render_template('controlPaquetes.html')

@app.route("/cambioSNPMDispositivo")
def cambio_SNPM_Dispositivo():
    return render_template('cambioSNPMDispositivo.html')
    
@app.route("/paquetesDispositivo")
def paquetes_dispositivo():
    return render_template('transitoDispositivo.html')


@app.route("/control_usuario_pagina")
def control_usuario_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from UsuarioTopologia where not IDUsuarioTopologia=1')
    data=cur.fetchall()
    return render_template('controlUsuario.html',usuarios=data)

@app.route ("/control_protocolos")
def control_protocolos():
    return render_template('configuracionProtocolos.html')

@app.route("/usuarios_sistema_pagina")
def usuarios_sistema_pagina():
    cur=mysql.connection.cursor()
    resultadoSelect=cur.execute('select * from Usuario where Nivel="Normal"')
    data=cur.fetchall()
    return render_template('usuarioSistema.html',usuarios=data)

@app.route("/control_snpm_pagina")
def control_snpm_pagina():
    return render_template('controlSNPM.html')

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


@app.route("/registro_pagina")
def registro_pagina():
    return render_template('registro.html')

@app.route("/nuevo_usuario_sistema")
def nuevo_usuario_sistema():
    return render_template('nuevoUsuarioSistema.html')
    
@app.route("/nuevo_usuario_topologia")
def nuevo_usuario_topologia():
    return render_template('nuevoUsuarioTopologia.html')

"""acciones de administracion usuario sistema"""
@app.route("/registro_nuevo_usuario_sistema",methods=['POST'])
def registro_nuevo_usuario_sistema():
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        cur=mysql.connection.cursor()
        cur.execute('insert into Usuario (Nombre,Contra,Correo,Nivel) values (%s,%s,%s,%s)',
        (nombreUsu,contraUsu,correoUsu,'Normal'))
        mysql.connection.commit()
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')

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

@app.route("/eliminar_usuario_sistema/<string:id>")
def eliminar_usuario_sistema(id):
    cur=mysql.connection.cursor()
    cur.execute('delete from Usuario where IDUsuario={0}'.format(id))
    mysql.connection.commit()
    return redirect('/usuarios_sistema_pagina')


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
        return redirect('/ping_Usuario')
    else:
        return  render_template('error.html')



@app.route("/registro_usuario", methods=['POST'])
def registro_usuario():
    if request.method=='POST':
        nombreUsu=request.form['nombre']
        correoUsu=request.form['correo']
        contraUsu=request.form['contra']
        codigoUsu=request.form['codigo']
        cur=mysql.connection.cursor()
        cur.execute('insert into Usuario (Nombre,Contra,Correo,Nivel) values (%s,%s,%s,%s)',
        (nombreUsu,contraUsu,correoUsu,'Administrador'))
        mysql.connection.commit()
        cur=mysql.connection.cursor()
        resultadoSelect=cur.execute("select * from Usuario where Nombre=%s and Contra=%s",
        (nombreUsu,contraUsu))
        detallesUsuario=cur.fetchall()
        for user in detalleUsuario:
            session["userID"]=user[0]
        return  render_template('controlUsuario.html')
    else:
        return  render_template('error.html')

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
            """print(tipoUsuario)"""
            
            if tipoUsuario==1:
                return  redirect('/control_usuario_pagina')
            elif tipoUsuario==2:
                return  render_template('pingUsuario.html')
            else:
                return  render_template('error.html')
        else:
            return  render_template('error.html')
    else:
        return  render_template('error.html')

#Metodo para cerrar sesion del usuario
@app.route('/salir_sesion')
def salir_sesion():
    sesion.clear()
    return render_template('index.html')

"""acciones de los usuarios topologia"""

@app.route("/registro_nuevo_usuario_topologia",methods=['POST'])
def registro_nuevo_usuario_topologia():
    if request.method=='POST':
        listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
        nombreUsu=request.form['nombre']
        nivelUsu=request.form['nivel']
        contraUsu=request.form['contra']
        for i in listaIP:
            crear_usuario_topologia_ssh(nombreUsu,contraUsu,nivelUsu,i)
        cur=mysql.connection.cursor()
        cur.execute('insert into UsuarioTopologia (Nombre,Contra,Nivel) values (%s,%s,%s)',
        (nombreUsu,contraUsu,nivelUsu))
        mysql.connection.commit()
        return redirect('/control_usuario_pagina')
    else:
        return render_template('error.html')

@app.route("/eliminar_usuario_topologia/<string:id>")
def eliminar_usuario_topologia(id):
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
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


@app.route("/guardar_cambio_usuario_topologia/<string:id>",methods=['POST'])
def guardar_cambio_usuario_topologia(id):
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
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

@app.route('/nueva_ruta_rip',methods=['POST'])
def nueva_ruta_rip():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    if request.method=='POST':
        ruta=request.form['rutaIP']
        for i in listaIP:
            crear_rutaRIP(ruta,i)
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')
        
@app.route('/nueva_ruta_ospf',methods=['POST'])
def nueva_ruta_ospf():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
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


@app.route('/nueva_ruta_eigrp',methods=['POST'])
def nueva_ruta_eigrp():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']
    if request.method=='POST':
        numAuto=request.form['autNum']
        direccionRed=request.form['direccionRed']
        wildcard=request.form['wildcard']
        for i in listaIP:
            crear_rutaEIGRP(numAuto,direccionRed,wildcard,i)
        return redirect('/usuarios_sistema_pagina')
    else:
        return render_template('error.html')


@app.route('/activar_rip_default')
def activar_rip_default():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_rip_default_ssh(i)
    for i in listaIP:
        quitar_menos_RIP_ssh(i)
    return redirect('/usuarios_sistema_pagina')

@app.route('/activar_ospf_default')
def activar_ospf_default():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_ospf_default_ssh(i)
    for i in listaIP:
        quitar_menos_OSPF_ssh(i)
    return redirect('/usuarios_sistema_pagina')
    
@app.route('/activar_eigrp_default')
def activar_eigrp_default():
    listaIP=['10.0.0.254','192.0.0.2','192.0.0.6']    
    for i in listaIP:
        activar_eigrp_default_ssh(i)
    for i in listaIP:
        quitar_menos_EIGRP_ssh(i)
    return redirect('/usuarios_sistema_pagina')


if __name__=='__main__':
    app.run(port=3000,debug=True)
