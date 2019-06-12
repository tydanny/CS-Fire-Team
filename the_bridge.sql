DROP TABLE IF EXISTS person_xref_incident;
DROP TABLE IF EXISTS person_xref_event;
DROP TABLE IF EXISTS incident;
DROP TABLE IF EXISTS person_xref_class;
DROP TABLE IF EXISTS shift CASCADE;
DROP TABLE IF EXISTS person_status;
DROP TABLE IF EXISTS event CASCADE;
DROP TABLE IF EXISTS person CASCADE;
DROP TABLE IF EXISTS class CASCADE;

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
    person_id TEXT REFERENCES person(id),
    shift_start TIMESTAMP,
    shift_end TIMESTAMP,
    station TEXT,
    bonus TEXT,
    PRIMARY KEY (person_id, shift_start, shift_end)
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
    id TEXT,
    tstart TIMESTAMP,
    etype TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE person_xref_event
(
    event_id TEXT REFERENCES event(id),
    person_id TEXT REFERENCES person(id),
    duration NUMERIC(4,2),
    PRIMARY KEY (event_id,person_id)
);

CREATE TABLE class
(
    id TEXT,
    tstart TIMESTAMP,
    duration INTEGER,
    type TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE person_xref_class
(
    class_id TEXT REFERENCES class(id),
    person_id TEXT REFERENCES person(id),
    PRIMARY KEY (class_id,person_id)
);