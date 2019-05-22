import dbconnect

d = dbconnect()
d.connect()

#Loads a person.
def load_person(person_id, note, time):
	d.i_query("INSERT INTO person (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time))

#Takes in incident id, time, category, and response.
def load_incident(id, time, category, response):
	d.i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s');" % (id, time, category, response))

#Takes in an incident id and a list of personnel who responded and where they came from.
def load_person_xref_incident(id, response):
	for r, s in response:
		d.i_query("INSERT INTO person_xref_incident (incident_id, person_id, origin) VALUES ('%s', '%s', '%s');" % (id, r, s))

#Loads a note if time is known
def load_note(person_id, note, time):
	d.i_query("INSERT INTO note (person_id, note, created_at) VALUES ('%s', '%s', '%s');" % (person_id, note, time))

#Loads a note if time is not known
def load_note(person_id, note):
	d.i_query("INSERT INTO note (person_id, note) VALUES ('%s', '%s');" % (person_id, note))

#Loads a shift.  
def load_shift(tstart, tend, station):
	d.i_query("INSERT INTO shift (tstart, tend, station) VALUES ('%s', '%s', '%s');" % (tstart, tend, station))

#Loads a connection between a shift and a person.  "person" is a list of pairs or equivalent
def load_person_xref_shift(shift_start, shift_end, person):
	for p, r in person:
		d.i_query("INSERT INTO person_xref_shift (person_id, shift_start, shift_end, role) VALUES ('%s', '%s', '%s', '%s');" % (p, shift_start, shift_end, r))
	
#Loads a person_status change
def load_person_status(status, date_change, person_id):
	d.i_query("INSERT INTO person_status (status, date_change, person_id) VALUES ('%s', '%s', '%s');" % (status, date_change, person_id))

#Loads an event
def load_event(tstart, tend, etype):
	d.i_query("INSERT INTO event (tstart, tend, etype) VALUES ('%s', '%s', '%s');" % (tstart, tend, etype))

#Loads a person_xref_event.  Person_id is a LIST of all the ids for the people who worked an event.	
def load_person_xref_event(tstart, tend, etype, person_id):
	for p in people_id:
		d.i_query("INSERT INTO person_xref_event (tstart, tend, etype, person_id) VALUES ('%s', '%s', '%s', '%s');" % (tstart, tend, etype, p))
