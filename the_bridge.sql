DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS person_status;
DROP TABLE IF EXISTS certification;
DROP TABLE IF EXISTS person_xref_incident;

CREATE TABLE person
(
    id serial PRIMARY KEY,
    name TEXT,
    title TEXT
);

CREATE TABLE incident
(
    id serial PRIMARY KEY,
    tstamp TIMESTAMP,
    category TEXT,
    response INTEGER
);

CREATE TABLE person_xref_incident
(
    person_id INTEGER REFERENCES person(id),
    incident_id INTEGER REFERENCES incident(id),
    origin TEXT,
    PRIMARY KEY (person_id, incident_id)
);

CREATE TABLE shift
(
    tstart TIME,
    tend TIME,
    date DATE,
    slot INTEGER,
    station INTEGER,
    role TEXT,
    PRIMARY KEY (tstart, tend, slot)
);

CREATE TABLE person_xref_shift
(
    person_id INTEGER REFERENCES person(id),
    shift_start TIME,
    shift_end TIME,
    shift_slot INTEGER,
    FOREIGN KEY (shift_start, shift_end, shift_slot) REFERENCES shift(shift_start, shift_end, shift_slot),
    PRIMARY KEY (person_id, shift_start, shift_end, shift_slot)
);

CREATE TABLE person_status
(
    status TEXT,
    date DATE,
    PRIMARY KEY (status, date)
);