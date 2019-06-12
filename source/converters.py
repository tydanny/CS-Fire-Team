import sys
import pandas as pd
import lxml
from source import dbconnect
import json

def convert_iar(file, deleteBeforeAddition=False, timeRangeStart=None, timeRangeEnd=None):
  
  db = dbconnect.dbconnect()

  #This should be dynamic, and it should function fine.
  rep = pd.read_html(file)

  #This contains the info for every shift that failed to load because the person id couldn't be found in the database.
  failures = []
  
  if(deleteBeforeAddition):
    db.delete_shift_range(timeRangeStart, timeRangeEnd)
  
  for index, row in rep[0].iterrows():
    
    tstart = row.loc['Start date'].replace('/','-') + ' ' + row.loc['Start time'] + ':00'
    tend = row.loc['End date'].replace('/','-') + ' ' + row.loc['End time'] + ':00'
    location = row.loc['On duty at']
    bonus = row.loc['On duty for']
    
    person = row.loc['First name'].split(' ')[0]
    
    sft = db.get_shift(person, tstart, tend)

    if(not sft):
      if(not db.get_person_id(person)):
        failures.append([person, tstart, tend])
      else:
        db.load_shift(tstart, tend, location, person, bonus)
    elif (sft[0][4] != bonus):
      db.update_bonus(tstart, tend, person, bonus)
      
  return failures
