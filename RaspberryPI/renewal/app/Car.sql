USE doraemon;


CREATE TABLE users (
  usr_id varchar(30) UNIQUE,
  usr_name varchar(20),
  token varchar(200)
);


CREATE TABLE drive (
  car_id varchar(30),
  pos_time datetime,
  fuel_efi double,
  speed int(11)
);

CREATE TABLE position (
  car_id varchar(30),
  pos_time datetime,
  pos_x double,
  pos_y double
);

CREATE TABLE record (
  car_id varchar(30),
  start_time datetime,
  fuel_efi float,
  speed int(11),
  rpm int(11),
  brk_num int(11),
  acl_num int(11),
  score int(11),
  distance float,
  end_time datetime
);

CREATE TABLE car (
  car_id varchar(30) NOT NULL,
  usr_id varchar(30) NOT NULL,
  car_name varchar(30) NOT NULL,
  volume varchar(30) NOT NULL,
  fuel varchar(30) NOT NULL,
  fuel_efi varchar(30) NOT NULL,
  PRIMARY KEY (car_id),
  KEY usr_id (usr_id),
  CONSTRAINT car_ibfk_1 FOREIGN KEY (usr_id) REFERENCES users (usr_id)
);