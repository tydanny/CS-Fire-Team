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

INSERT INTO person_xref_incident (person_id, incident_id) VALUES ('1', 1);
INSERT INTO person_xref_incident (person_id, incident_id) VALUES ('7', 2);

INSERT INTO event (tstart, tend, etype) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'training-department');
INSERT INTO event (tstart, tend, etype) VALUES ('04-02-2019 02:00 PM', '04-02-2019 03:00 PM', 'work detail-weekly');
INSERT INTO event (tstart, tend, etype) VALUES ('04-03-2019 02:00 PM', '04-03-2019 03:00 PM', 'work detail-daily');
INSERT INTO event (tstart, tend, etype) VALUES ('04-04-2019 02:00 PM', '04-04-2019 03:00 PM', 'work detail-sunday');
INSERT INTO event (tstart, tend, etype) VALUES ('04-05-2019 02:00 PM', '04-05-2019 03:00 PM', 'work detail-fundraiser');
INSERT INTO event (tstart, tend, etype) VALUES ('04-06-2019 02:00 PM', '04-06-2019 03:00 PM', 'work detail-other');
INSERT INTO event (tstart, tend, etype) VALUES ('04-01-2019 02:00 PM', '04-01-2019 03:00 PM', 'training-other');

INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'training-department', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'training-department', '7');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('03-24-2019 09:30 AM', '03-24-2019 11:00 AM', 'training-department', '1234');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-02-2019 02:00 PM', '04-02-2019 03:00 PM', 'work detail-weekly', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-03-2019 02:00 PM', '04-03-2019 03:00 PM', 'work detail-daily', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-04-2019 02:00 PM', '04-04-2019 03:00 PM', 'work detail-sunday', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-05-2019 02:00 PM', '04-05-2019 03:00 PM', 'work detail-fundraiser', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-06-2019 02:00 PM', '04-06-2019 03:00 PM', 'work detail-other', '1');
INSERT INTO person_xref_event (tstart, tend, type, person_id) VALUES ('04-01-2019 02:00 PM', '04-01-2019 03:00 PM', 'training-other', '1');

INSERT INTO shift (tstart, tend, station) VALUES ('10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 1);

INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('1', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Fire Fighter');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('1234', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Engineer');
INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('7', '10-04-2018 6:00 AM', '10-04-2018 12:00 PM', 'Fire Fighter');
