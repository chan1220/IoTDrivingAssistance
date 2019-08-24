CREATE DATABASE doraemon CHARACTER SET utf8;
USE doraemon;


CREATE TABLE users (
  usr_id      VARCHAR (30) UNIQUE,
  usr_name    VARCHAR(20),
  token       VARCHAR(200)
);


CREATE TABLE drive (
  car_id      VARCHAR(30),
  pos_time    DATETIME,
  fuel_efi    DOUBLE,
  speed       INT(11)
);

CREATE TABLE position (
  car_id      VARCHAR(30),
  pos_time    DATETIME,
  pos_x       DOUBLE,
  pos_y       DOUBLE
);

CREATE TABLE record (
  car_id      VARCHAR(30),
  start_time  DATETIME,
  fuel_efi    FLOAT,
  speed       INT(11),
  rpm         INT(11),
  brk_num     INT(11),
  acl_num     INT(11),
  score       INT(11),
  distance    FLOAT,
  end_time    DATETIME
);

CREATE TABLE code (
  car_id      VARCHAR(30) NOT NULL,
  code_time   DATETIME,
  code        VARCHAR(30) NOT NULL,
  description VARCHAR(150) NOT NULL
);


CREATE TABLE car (
  car_id      VARCHAR(30) NOT NULL,
  usr_id      VARCHAR(30) NOT NULL,
  car_name    VARCHAR(30) NOT NULL,
  volume      VARCHAR(30) NOT NULL,
  fuel        VARCHAR(30) NOT NULL,
  fuel_efi    VARCHAR(30) NOT NULL,
  PRIMARY KEY (car_id),
  KEY usr_id (usr_id),
  CONSTRAINT car_ibfk_1 FOREIGN KEY (usr_id) REFERENCES users (usr_id)
);

set sql_safe_updates=0;

select * from position;
select * from drive;
select * from record;

delete from position;
delete from car;
delete from record;
delete from drive;
delete from users;