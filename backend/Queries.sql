select * from rover_app_owner;
select * from rover_app_sitter;
select * from rover_app_pet;
select * from rover_app_stay;
select * from rover_app_stay_pets;

select * from rover_app_owner o where o.owner_name = 'Shelli K.';
select * from rover_app_sitter s where s.sitter_name = 'Lauren B.';

select * from rover_app_sitter s where s.id = 196;

select s.sitter_name, st.*
from rover_app_sitter s,
     rover_app_stay st
where s.id = st.sitter_id
  and s.id = 138
 ; 
 
select s.*
from rover_app_sitter s,
     rover_app_stay   st
where s.id = st.sitter_id
  and s.id = 138
; 
 
select s.id,
       s.sitter_name,
	   count(1)
from rover_app_sitter s,
     rover_app_stay st
where s.id = st.sitter_id
  group by s.id, s.sitter_name
 order by 3 desc
 ; 


delete from rover_app_stay_pets;
delete from rover_app_stay;
delete from rover_app_pet;
delete from rover_app_owner;
delete from rover_app_sitter;
commit;