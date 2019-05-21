DROP TABLE IF EXISTS person_xref_incident;
DROP TABLE IF EXISTS person_xref_shift;
DROP TABLE IF EXISTS person_xref_event;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS person_status;
DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS event;
DROP TABLE IF EXISTS person;

CREATE TABLE person
(
    id TEXT PRIMARY KEY,
    fName TEXT,
    lName TEXT,
    title TEXT,
    resident TEXT
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
    person_id TEXT REFERENCES person(id),
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
    person_id TEXT REFERENCES person(id),
    shift_start TIME,
    shift_end TIME,
    shift_slot INTEGER,
    FOREIGN KEY (shift_start, shift_end, shift_slot) REFERENCES shift(tstart, tend, slot),
    PRIMARY KEY (person_id, shift_start, shift_end, shift_slot)
);

CREATE TABLE person_status
(
    status TEXT,
    date_change DATE,
    person_id TEXT REFERENCES person(id),
    PRIMARY KEY (status, date_change, person_id)
);

CREATE TABLE note
(
    time TIMESTAMP,
    note TEXT,
    person_id TEXT REFERENCES person(id),
    PRIMARY KEY (time, person_id)
);

CREATE TABLE event
(
    tstart TIME,
    tend TIME,
    type TEXT,
    PRIMARY KEY (tstart, tend, type)
);

CREATE TABLE person_xref_event
(
    tstart TIME,
    tend TIME,
    type TEXT,
    person_id TEXT REFERENCES person(id),
    FOREIGN KEY (tstart,tend,type) REFERENCES event(tstart,tend,type),
    PRIMARY KEY (tstart,tend,type,person_id)
);
