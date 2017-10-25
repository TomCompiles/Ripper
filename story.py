from adt.characters import *
from adt.items import *
from adt.locations import *
from classes.Location import Location
from classes.Player import *
from classes.Time import *

from modules.parser import *

# from .game import characters,locations,player
# This module controls the story....

def nextEvent(time, day):

    if time == 17 and day == "Wednesday":
        krills["people"].remove(krill)
        print("Krill has been killed by a higher power, maybe someone with a keyboard??")
        clark["dialogue"].pop()
        clark["dialogue"].append("I didn't see nuttin!!!!")

    if time == 17 and day == "Friday":
        krills["people"].append(krill)
        print("Krill has been brought back to life!")

    if time == 17 and day == "Saturday":
        krills["inventory"].append(beer)
        print("Krill the new lord and saviour has restocked his beer")

class Narrative(object):
    #This class makes sure time_events happen at the right time in the story

    def __init__(self,time,display_manager,location_manager,player):
        self.time_manager = time
        self.display_manager = display_manager
        self.location_manager = location_manager
        self.time_events = []
        self.location_events = []
        self.item_events = []

        self.player = player

    def check_time_event(self):
        pass #Given an instance of the time_manager, check if there are any time_events due to run and run them
        current_week = self.time_manager.get_week()
        current_day = self.time_manager.get_day()
        current_time = self.time_manager.get_time()

        for event in self.time_events:
            if current_week > event["week"]: #If it is a week past when the event was due
                self.call_time_event(event)  # It definetly needs to be called
            elif (current_week == event["week"]) and current_day > event["day"]: # If it is later in the week
                self.call_time_event(event)  # The event is late and needs to be called
            # Else if it is the same week and day as the event, but the time for it has passed, call the event
            elif (current_week == event["week"] and current_day == event["day"] and current_time > event["time"]):
                self.call_time_event(event)
            else:
                pass

    

    def add_time_event(self, week, day, time, callback):
        event = {
            "week": week,
            "day": day,
            "time": time,
            "callback" : callback,
            "finished": False
        }
        self.time_events.append(event)
        
    def call_time_event(self, event):
        #remove the event from the list of time_events, as it has now been called
        self.time_events.remove(event)
        callback = event["callback"]
        context = {
            "display" : self.display_manager,
            "time" : self.time_manager,
            "locations" : self.location_manager
        }
        callback(context)
        
    def check_location_event(self):
        player_location = self.player.getLocation()
        
        for event in self.location_events:
            if event["location"] == player_location:
                self.call_location_event(event)
    
    def add_location_event(self,location,callback):
        if not location is Location:
            location = self.location_manager.get_location(location["name"])

        event = {
            "location" : location,
            "callback" : callback
        }
        self.location_events.append(event)
    
    def call_location_event(self, event):
        #remove the event from the list of location_events, as it has now been called
        self.location_events.remove(event)
        callback = event["callback"]
        context = {
            "display" : self.display_manager,
            "location" : self.location_manager,
            "player" : self.player
        }
        callback(context)

    

