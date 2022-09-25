create database examen;
use examen;

create table carrera(
	codigoCarrera int not null primary key,
    nombre varchar(100),
    duracion varchar(20)
);

create table estudiante(
	DNI int not null primary key,
    apellidos varchar(50),
    nombres varchar(50),
    fecNacimiento datetime,
    sexo char(20),
    codigoCarrera int,
    foreign key (codigoCarrera) references carrera (codigoCarrera)
);

create table curso(
	codigoCurso int not null primary key,
    nombre varchar(50),
    credito int,
    codigoCarrera int,
    foreign key (codigoCarrera) references carrera (codigoCarrera)
);

create table matricula(
	codigoMatricula int not null primary key,
    DNI int,
    codigoCurso int,
    foreign key (DNI) references estudiante (DNI),
    foreign key (codigoCurso) references curso (codigoCurso)
);

