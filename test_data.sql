DELETE FROM person_xref_incident WHERE 1=1;
DELETE FROM person_xref_event WHERE 1=1;
DELETE FROM person_status WHERE 1 = 1;
DELETE FROM person_xref_shift WHERE 1=1;
DELETE FROM shift WHERE 1=1;
DELETE FROM event WHERE 1=1;
DELETE FROM note WHERE 1=1;
DELETE FROM incident WHERE 1=1;
DELETE FROM person WHERE 1 = 1;

INSERT INTO person (id, fname, lname, title, resident) VALUES ('1', 'James', 'Fire', 'Officer', 'Non-Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('7', 'John', 'Doe', 'Fire Fighter', 'Resident');
INSERT INTO person (id, fname, lname, title, resident) VALUES ('1234', 'Jenny', 'Smokes', 'Fire Fighter', 'Resident');

INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '01-01-2010', '1');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '04-03-2015', '7');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '05-10-2019', '1234');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Inactive', '11-13-2010', '7');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Active', '02-09-2016', '7');
INSERT INTO person_status (status, date_change, person_id) VALUES ('Medical', '08-20-2018', '1');

INSERT INTO note (note, person_id) VALUES ('Sprained ankle while on duty', '1');

INSERT INTO incident (id, tstamp, category, response) VALUES (1, '02-03-2019 17:56', 'Car Accident', '1 minute 30 seconds');
INSERT INTO incident (id, tstamp, category, response) VALUES (2, '05-30-2015 22:36', 'Sturcture Fire', '6 minutes 23 seconds');

INSERT INTO person_xref_incident (person_id, incident_id, origin) VALUES ('1', (select id from incident where category='Car Accident'), 'Station 1');
INSERT INTO person_xref_incident (person_id, incident_id, origin) VALUES ('7', (select id from incident where category='Car Accident'), 'Station 1');

INSERT INTO event (tstart, tend, type) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'Training');
INSERT INTO event (tstart, tend, type) VALUES ('09-18-2019 02:00 PM', '09-18-2019 03:00 PM', 'Weekly');

INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'Training', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'Training', '7');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'Training', '1234');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('09-18-2019 02:00 PM', '09-18-2019 03:00 PM', 'Weekly', '1');

INSERT INTO shift (tstart, tend, station, role) VALUES ('10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 1, 'Fire Fighter');

INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('1', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('1234', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end) VALUES ('7', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM');
