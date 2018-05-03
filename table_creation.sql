create table customer(
fname varchar(10) not null ,
lname varchar(10) not null,
mobileNo numeric(10) not null,
vehicle_number varchar(13) primary key,
vehicle_type char(1) not null
);

create table special(
vehicle_number varchar(13) primary key
);

create table parking_slot(
parking_slot_id varchar(10) primary key,
floor_no numeric(2) not null,
parking_type char(1) not null,
isOccupied char(1) not null
);
alter table parking_slot
alter isOccupied set default 'N';

create table slot(
parking_slot_id varchar(10),
vehicle_number varchar(13) not null,
entry_date_time timestamp default CURRENT_TIMESTAMP,
primary key(parking_slot_id,vehicle_number)
);
alter table slot
add constraint fk1 foreign key(vehicle_number) references customer(vehicle_number) on delete cascade;
alter table slot
add constraint fk2 foreign key(parking_slot_id) references parking_slot(parking_slot_id) on delete cascade;


create table parking_slip(
slip_id int auto_increment ,
parking_slot_id varchar(10) ,
vehicle_number varchar(13),
t_entry timestamp not null,
t_exit timestamp default CURRENT_TIMESTAMP,
basic_cost numeric (5,2),
discount numeric(5,2) default 0,
total numeric(5,2),
primary key(slip_id)
);
alter table parking_slip
add constraint check (parking_slot_id  in (select parking_slot_id from parking_slot));
alter table parking_slip
add constraint check (vehicle_number  in (select vehicle_number from customer));



create table rate(
vehicle_type char(1) primary key,	
basic_cost numeric(5,2) unique
);