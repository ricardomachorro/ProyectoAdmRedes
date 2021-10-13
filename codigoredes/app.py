from flask import Flask, render_template, url_for, request, redirect
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='ramv1357'
app.config['MYSQL_DB']='flaskRedes'
mysql=MySQL(app)

"""Direccionamiento paginas"""
@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/control_usuario_pagina")
def control_usuario_pagina():
    return render_template('controlUsuario.html')

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
    return render_template('configuracionAdministrador.html')

@app.route("/registro_pagina")
def registro_pagina():
    return render_template('registro.html')

@app.route("/nuevo_usuario_sistema")
def nuevo_usuario_sistema():
    return render_template('nuevoUsuarioSistema.html')

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
        correo=user[2]
        contra=user[3]
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
            print(tipoUsuario)
            if tipoUsuario==1:
                return  render_template('controlUsuario.html')
            elif tipoUsuario==2:
                return  render_template('pingUsuario.html')
            else:
                return  render_template('error.html')
        else:
            return  render_template('error.html')
    else:
        return  render_template('error.html')



        

@app.route('/delete')
def delete_contact():
    return 'delete'

if __name__=='__main__':
    app.run(port=3000,debug=True)
