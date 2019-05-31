DROP TABLE IF EXISTS person_xref_incident;
DROP TABLE IF EXISTS person_xref_shift;
DROP TABLE IF EXISTS person_xref_event;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS shift;
DROP TABLE IF EXISTS person_status;
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
    PRIMARY KEY (person_id, incident_id)
);

CREATE TABLE shift
(
    tstart TIMESTAMP,
    tend TIMESTAMP,
    station TEXT,
    PRIMARY KEY (tstart, tend, station)
);

CREATE TABLE person_xref_shift
(
    person_id TEXT REFERENCES person(id),
    shift_start TIMESTAMP,
    shift_end TIMESTAMP,
    station TEXT,
    role TEXT,
    FOREIGN KEY (shift_start, shift_end, station) REFERENCES shift(tstart, tend, station),
    PRIMARY KEY (person_id, shift_start, shift_end, station)
);

CREATE TABLE person_status
(
    status TEXT,
    date_change TIMESTAMP,
    person_id TEXT REFERENCES person(id),
    note TEXT,
    PRIMARY KEY (status, date_change, person_id)
);

CREATE TABLE event
(
    tstart TIMESTAMP,
    tend TIMESTAMP,
    etype TEXT,
    PRIMARY KEY (tstart, tend, etype)
);

CREATE TABLE person_xref_event
(
    tstart TIMESTAMP,
    tend TIMESTAMP,
    type TEXT,
    person_id TEXT REFERENCES person(id),
    FOREIGN KEY (tstart,tend,type) REFERENCES event(tstart,tend,etype),
    PRIMARY KEY (tstart,tend,type,person_id)
);
