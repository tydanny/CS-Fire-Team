import dbconnect

#Takes in incident id, time, category, and response.
def load_incident(id, time, category, response):
	i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s')" % (id, time, category, response))
	
#Takes in an incident id and a list of personnel who responded and where they came from.
def load_person_xref_incident(id, response):
	for r, s in response:
		i_query("INSERT INTO person_xref_incident (incident_id, person_id, origin) VALUES ('%s', '%s', '%s')" % (id, r, s))

#Loads a note if time is known
def load_note(person_id, note, time):
	i_query("INSERT INTO note (person_id, note, created_at) VALUES ('%s', '%s', '%s')" % (person_id, note, time))
	
def load_note(person_id, note):
	i_query("INSERT INTO note (person_id, note) VALUES ('%s', '%s')" % (person_id, note))
