INSERT INTO person (id, fname, lname, title, resident) VALUES ('1', 'James', 'Fire', 'Officer', 'Non-Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('7', 'John', 'Doe', 'Fire Fighter', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('1234', 'Jenny', 'Smokes', 'Fire Fighter', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('12347', 'Ty', 'Christensen', 'Admin', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('12349', 'Hannah', 'Levy', 'Admin', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('12346', 'Heidi', 'Hufford', 'Admin', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('12348', 'Brad', 'Helliwell', 'Admin', 'Resident');

INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2010', '1');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '05-10-2019', '1234');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '04-03-2015', '7');
INSERT INTO person_status (status, date_change, person_id, note) VALUES ('Disability Leave', '11-13-2018', '7', 'Broke ankle while on duty');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '03-10-2019', '7');
INSERT INTO person_status (status, date_change, person_id, note) VALUES ('Disability Leave', '04-10-2019', '7', 'Broke ankle while on duty');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Retired', '08-20-2018', '1');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2019', '12347');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2019', '12349');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2010', '12346');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2019', '12348');

INSERT INTO incident (id, tstamp, category, response) VALUES (1, '02-03-2019 17:56', 'Car Accident', '1 minute 30 seconds');
INSERT INTO incident (id, tstamp, category, response) VALUES (2, '05-30-2015 22:36', 'Sturcture Fire', '6 minutes 23 seconds');

INSERT INTO person_xref_incident (person_id, incident_id) VALUES ('1', 1);
INSERT INTO person_xref_incident (person_id, incident_id) VALUES ('7', 2);

INSERT INTO event (id, tstart, tend, etype) VALUES ('-0', '03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'training-department');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-1', '04-02-2019 02:00 PM', '04-02-2019 03:00 PM', 'WORDK DEATIL');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-2', '04-03-2019 02:00 PM', '04-03-2019 03:00 PM', 'work detail-daily');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-3', '04-04-2019 02:00 PM', '04-04-2019 03:00 PM', 'work detail-sunday');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-4', '04-05-2019 02:00 PM', '04-05-2019 03:00 PM', 'work detail-fundraiser');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-5', '04-06-2019 02:00 PM', '04-06-2019 03:00 PM', 'work detail-other');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-6', '04-01-2019 02:00 PM', '04-01-2019 03:00 PM', 'training-other');
INSERT INTO event (id, tstart, tend, etype) VALUES ('-7', '04-02-2019 02:00 PM', '04-02-2019 03:00 PM', 'business-meeting');

INSERT INTO person_xref_event (event_id, person_id) VALUES ('-0', '1');

INSERT INTO shift (tstart, tend, station) VALUES ('10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Station 1');
INSERT INTO shift (tstart, tend, station) VALUES ('10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Station 4');

INSERT INTO person_xref_shift (person_id, shift_start, shift_end, station, role) VALUES ('1', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Station 1', 'Fire Fighter');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end, station, role) VALUES ('1234', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Station 1', 'Engineer');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end, station, role) VALUES ('7', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Station 4', 'Fire Fighter');
