drop database if exists flaskredes;
create database flaskRedes;
use flaskRedes;

create table Usuario (
IDUsuario int not null auto_increment,
Nombre varchar (255),
Contra varchar(255), 
Correo varchar(255),
Nivel varchar (255),
primary key (IDUsuario));

insert  Usuario(Nombre,Contra,Correo,Nivel) values ('ricardo','1234','rick@gmail.com','Administrador');
insert  Usuario(Nombre,Contra,Correo,Nivel) values ('luis','345','luis@gmail.com','Normal');
insert  Usuario(Nombre,Contra,Correo,Nivel) values ('erick','123','erick@gmail.com','Normal');
insert  Usuario(Nombre,Contra,Correo,Nivel) values ('pedro','456','pedro@gmail.com','Normal');

select * from usuario;

create table UsuarioTopologia (
IDUsuarioTopologia int not null auto_increment,
Nombre varchar (255),
Contra varchar (255),
Nivel int,
primary key (IDUsuarioTopologia));

insert  UsuarioTopologia(Nombre,Contra,Nivel) values ('cisco','cisco',15);

select * from UsuarioTopologia;

create table Dispositivo(
IDDispositivo int not null auto_increment,
NombreHost varchar(255),
Responsable int,
Ubicacion varchar (255),
Contacto varchar(255),
Tipo varchar(255),
primary key (IDDispositivo),
FOREIGN KEY (Responsable) REFERENCES Usuario(IDUsuario)
);


