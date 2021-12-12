drop database if exists flaskRedes;
create database flaskRedes;
use flaskRedes;

create table Usuario (
IDUsuario int not null auto_increment,
Nombre varchar (255),
Contra varchar(255), 
Correo varchar(255),
Nivel varchar (255),
Activo varchar (255),
Actualizacion int,
primary key (IDUsuario));

insert  Usuario(Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values ('ricardo','1234','rick@gmail.com','Administrador','Activo',12);
insert  Usuario(Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values ('luis','345','luis@gmail.com','Normal','Activo',12);
insert  Usuario(Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values ('erick','123','erick@gmail.com','Normal','Activo',12);
insert  Usuario(Nombre,Contra,Correo,Nivel,Activo,Actualizacion) values ('pedro','456','pedro@gmail.com','Normal','Activo',12);

select * from Usuario;

create table UsuarioTopologia (
IDUsuarioTopologia int not null auto_increment,
Nombre varchar (255),
Contra varchar (255),
Nivel int,
primary key (IDUsuarioTopologia));

insert  UsuarioTopologia(Nombre,Contra,Nivel) values ('cisco','cisco',15);

select * from UsuarioTopologia;

delete from UsuarioTopologia where IDUsuarioTopologia>1;

create table Bitacora(
IDRegistro int not null auto_increment,
IDUsuario int,
Momento timestamp,
Descripcion text,
primary key (IDRegistro),
FOREIGN KEY (IDUsuario) REFERENCES Usuario(IDUsuario)
);

select * from Bitacora; 


select count(IDDispositivo) from Dispositivo where DireccionEncontrada='10.0.0.254';
select * from Dispositivo;
create table Dispositivo(
IDDispositivo int not null auto_increment,
NombreHost varchar(255),
DireccionEncontrada varchar(255),
Ubicacion varchar (255),
Contacto varchar(255),
Tipo varchar(255),
Estado varchar(255),
primary key (IDDispositivo)
);



create table Interfaz(
 IDInterfaz int not null auto_increment,
 IDDispositivo int,
 Nombre varchar(255),
 Estado varchar(255),
 PaquetesEnviados int,
 PaquetesRecibidos int,
 PaquetesDa int,
 MomentoRevision timestamp,
 primary key (IDInterfaz),
 foreign key (IDDispositivo) references  Dispositivo(IDDispositivo)
);
select * from Interfaz;

drop table Bitacora;
drop table Dispositivo;
drop table Interfaz;