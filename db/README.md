# Add Zip Nodes to the database

You can use DB Browser for SQLite to insert zip nodes into a temp database. Let's call it zip_hazard_temp. After a successful
bulk insert, you can extract the data into zip_hazard table which is a zip code and hazard id table with the corresponding Boolean value. 
    
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_hurricane_flag', aff_hurricane_flag from zip_hazard_temp where aff_hurricane_flag is not null;
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_wildfire_flag', aff_wildfire_flag from zip_hazard_temp where aff_wildfire_flag is not null;
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_air_health_sensitive_flag', aff_air_health_sensitive_flag from zip_hazard_temp where aff_air_health_sensitive_flag is not null;
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_deadly_heat_flag', aff_deadly_heat_flag from zip_hazard_temp where aff_deadly_heat_flag is not null;
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_record_heat_flag', aff_record_heat_flag from zip_hazard_temp where aff_record_heat_flag is not null;
    insert into zip_hazard (zip, hazard, value) select zip_code, 'aff_air_health_flag', aff_air_health_flag from zip_hazard_temp where aff_air_health_flag is not null;