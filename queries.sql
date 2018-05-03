-- all the customers who have parked their vehicle
select * 
from customer;

-- all special customers

	select * 
	from customer
	where vehicle_number in(
	select vehicle_number 
	from special);

-- all not so special customers

select * 
from customer
where vehicle_number not in(
select vehicle_number 
from special);

-- show all available paring slots
select * 
from parking_slot
where isOccupied = 'N';

-- all available slots on a particular floor
select *
from parking_slot
where floor_no = 0 and isOccupied = 'N';

-- all slots on a particular floor
select * 
from parking_slot
where floor_no = 0;

-- basic cost of parking per hour
select * 
from rate;



