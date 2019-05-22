import dbconnect

#Takes in incident id, time, category, and response.
def load_incident(id, time, category, response):
	i_query("INSERT INTO incident (id, tstamp, category, response) VALUES ('%s', '%s', '%s', '%s')" % (id, time, category, response))
	
#Takes in an incident id and a list of personnel who responded and where they came from.
def load_person_xref_incident(id, response):
	for r, s in response:
		i_query("INSERT INTO person_xref_incident (incident_id, person_id, origin) VALUES ('%s', '%s', '%s')" % (id, r, s))
