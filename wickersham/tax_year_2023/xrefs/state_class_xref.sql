drop table if exists state_class_xref;

CREATE TABLE [state_class_xref] 
(
    [Code]	VARCHAR(512),
    [Description ]	VARCHAR(512)
);

INSERT INTO [state_class_xref] ([Code], [Description ]) VALUES
	('G1', 'Oil and Mineral Gas Reserves '),
	('G2', 'Real Property Other Mineral Reserves '),
	('J1', 'Real & Tangible Personal, Utility Water Systems '),
	('J2', 'Gas Companies '),
	('J3', 'Electric Companies '),
	('J4', 'Telephone Companies '),
	('J5', 'Railroads '),
	('J6', 'Pipelines '),
	('J7', 'Major Cable Television Systems ');