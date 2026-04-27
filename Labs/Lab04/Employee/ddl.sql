CREATE TABLE IF NOT EXISTS employee
	(
		ID		varchar(7),
		person_name 	varchar(40),
		street	varchar(25),
		city    varchar(20),
		state	varchar(2),

		primary key(ID)
	);
	CREATE TABLE IF NOT EXISTS company
	(
		company_name	varchar(30),
		city	varchar(20),
		state varchar(2),
		primary key(company_name)
	);
	CREATE TABLE IF NOT EXISTS works
	(
		ID 	varchar(7),
		company_name	varchar(30),
		salary 	numeric(6,0),
		primary key(ID, company_name),
		foreign key(ID) references employee,
		foreign key(company_name) references company
	);
	