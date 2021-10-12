from flask import Flask, render_template, url_for, request
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
    return render_template('usuarioSistema.html')

@app.route("/control_snpm_pagina")
def control_snpm_pagina():
    return render_template('controlSNPM.html')

@app.route("/configuracion_admi_pagina")
def configuracion_admi_pagina():
    return render_template('configuracionAdministrador.html')

@app.route("/registro_pagina")
def registro_pagina():
    return render_template('registro.html')


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
