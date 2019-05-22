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
    fname TEXT,
    lname TEXT,
    title TEXT,
    resident TEXT
);

CREATE TABLE incident
(
    id INTEGER PRIMARY KEY,
    tstamp TIMESTAMP,
    category TEXT,
    response INTERVAL
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
    PRIMARY KEY (tstart, tend, date, slot)
);

CREATE TABLE person_xref_shift
(
    person_id TEXT REFERENCES person(id),
    shift_start TIME,
    shift_end TIME,
    date DATE,
    shift_slot INTEGER,
    FOREIGN KEY (shift_start, shift_end, date, shift_slot) REFERENCES shift(tstart, tend, date, slot),
    PRIMARY KEY (person_id, shift_start, shift_end, date, shift_slot)
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    person_id TEXT REFERENCES person(id),
    PRIMARY KEY (created_at, person_id)
);

CREATE TABLE event
(
    tstart TIME,
    tend TIME,
    date DATE,
    type TEXT,
    PRIMARY KEY (tstart, tend, type, date)
);

CREATE TABLE person_xref_event
(
    tstart TIME,
    tend TIME,
    type TEXT,
    date DATE,
    person_id TEXT REFERENCES person(id),
    FOREIGN KEY (tstart,tend,type, date) REFERENCES event(tstart,tend,type, date),
    PRIMARY KEY (tstart,tend,type,person_id)
);
