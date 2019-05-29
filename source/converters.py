import sys
import pandas as pd
import lxml
from dbconnect import dbconnect

def convert_schedule(filepath):
  
  db = dbconnect()
  #This should be dynamic, and it should function fine.
  rep = pd.read_html(filepath)
  
  for index, row in rep[0].iterrows():
    
    tstart = row.loc['Start date'].replace('/','-') + ' ' + row.loc['Start time'] + ':00'
    tend = row.loc['End date'].replace('/','-') + ' ' + row.loc['End time'] + ':00'
    location = row.loc['On duty at']
    if(not db.get_shift(tstart, tend, location)):
        print('Loc: ', location, 'Start time: ', tstart, 'End time: ', tend)
        db.load_shift(tstart,tend,location)
    role = row.loc['On duty for']
    
    #Should work for all, since i believe psycopg2 returns a lsit even if there is only one entry.  
    #However, it will jsut take the first id if there are two people with the same name.
    person = db.get_person_from_name(row.loc['First name'], row.loc['Last name'])
    print(person)
    db.load_person_xref_shift(tstart, tend, location, person, role)
