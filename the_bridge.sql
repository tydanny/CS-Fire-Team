DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS person_status;
DROP TABLE IF EXISTS certification;
DROP TABLE IF EXISTS person_xref_incident;

CREATE TABLE person
(
    id TEXT PRIMARY KEY,
    name TEXT,
    title TEXT,
    resident BOOLEAN
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
    person_id INTEGER REFERENCES person(id)
    PRIMARY KEY (tstart, tend, slot, person_id)
);

CREATE TABLE person_xref_shift
(
    person_id TEXT REFERENCES person(id),
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
    person_id TEXT REFERENCES person(id)
    PRIMARY KEY (status, date, person_id)
);

CREATE TABLE note
(
    time TIMESTAMP,
    note TEXT,
    person_id TEXT REFERENCES person(id)
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
    FOREIGN KEY (time,type) REFERENCES event(time,type)
    PRIMARY KEY (tstart,tend,type,person_id)
);
