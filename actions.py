# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.forms import FormAction
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import requests
import json

class CovidForm(FormAction):

    print("** inside CovidForm")

    def name(self) -> Text:
        return "Covid_Form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return["count_type", "location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        print(">> inside slot_mappings")

        return {
            "count_type": [self.from_entity(
                entity="count_type", 
                intent="count_type"),
                self.from_text()],
            "location": [self.from_entity(
                entity="location",
                intent="location"),
                self.from_text()],  #self.from_text will ensure that it accepts any input from user
                                    # which will later be validated by custom code.
        }

    @staticmethod
    def count_type_db() -> List[Text]:
        return [
            "confirmed",
            "active",
            "deaths",
        ]

    def validate_count_type(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        
        print(">> inside validate_count_type")

        if value.lower() in self.count_type_db():
            return {"count_type": value}
        else:
            dispatcher.utter_message(template="utter_wrong_count_type")
            return {"count_type": None}
        

    @staticmethod
    def input_db() -> Dict[str, List]:
        return{'location': ["maharashtra", "tamil nadu", "delhi", "telangana",
            "rajasthan", "kerala", "uttar pradesh", "andhra pradesh", "madhya pradesh",
            "karnataka", "gujarat", "haryana", "jammu and kashmir", "punjab",
            "best bengal", "odisha", "bihar", "uttarakhand", "assam", "chandigarh",
            "himachal pradesh", "ladakh", "andaman and nicobar islands", "chhattisgarh",
            "goa", "puducherry", "jharkhand", "manipur", "mizoram", "arunachal pradesh",
            "dadra and nagar haveli", "tripura", "daman and diu", "lakshadweep",
            "meghalaya", "nagaland", "sikkim"],
            'count_type': ["confirmed", "active", "deaths"]}


    def validate_location(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        print(">> inside validate_location")
        print("location pulled from intent", value)
        if value.lower() in self.input_db()['location']:
            return {"location": value}
        else:
            # find the closest answer by some measure (edit distance?)
            choices = self.input_db()['location']
            answer = process.extractOne(value.lower(), choices, scorer=fuzz.token_sort_ratio)

            print("@@",answer)

            if answer[1] < 60:
                dispatcher.utter_message(template="utter_wrong_location")
                return {"location": None}
            else:
                return {"location": answer[0]}


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:

        print(">> inside submit")
        # loc = tracker.get_slot('location')
        # cnt_type = tracker.get_slot('count_type')

        # message = "Received input location as -> {} and count_type as {}".format(loc, cnt_type)

        # dispatcher.utter_message(text=message)

        return []

class ActionResults(Action):

    print("** inside ActionResults")

    def name(self):
        return "action_results"

    
    @staticmethod
    def input_db() -> Dict[str, List]:
        return{'location': ["Maharashtra", "Tamil Nadu", "Delhi", "Telangana",
            "Rajasthan", "Kerala", "Uttar Pradesh", "Andhra Pradesh", "Madhya Pradesh",
            "Karnataka", "Gujarat", "Haryana", "Jammu and Kashmir", "Punjab",
            "West Bengal", "Odisha", "Bihar", "Uttarakhand", "Assam", "Chandigarh",
            "Himachal Pradesh", "Ladakh", "Andaman and Nicobar Islands", "Chhattisgarh",
            "Goa", "Puducherry", "Jharkhand", "Manipur", "Mizoram", "Arunachal Pradesh",
            "Dadra and Nagar Haveli", "Tripura", "Daman and Diu", "Lakshadweep",
            "Meghalaya", "Nagaland", "Sikkim"],
            'count_type': ["confirmed", "active", "deaths"]}


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(">> inside run")

        loc = tracker.get_slot('location')

        print("fetched slot value is :", loc)

        if loc.lower() in self.input_db()['location']:
            loc = loc
        else:
            # find the closest answer by some measure (edit distance?)
            choices = self.input_db()['location']
            answer = process.extractOne(loc.lower(), choices, scorer=fuzz.token_sort_ratio)

            print(answer)
            
            if answer[1] < 60:
                dispatcher.utter_message(template="utter_wrong_location")
                return {"location": None}
            else:
                loc = answer[0]

        cnt_type = tracker.get_slot('count_type')
        count = 99999

        response = requests.get("https://api.covid19india.org/data.json").json()

        if loc.lower() == "india":
            message = "the total confirmed number of cases is {}".format(response["statewise"][0]["confirmed"])
        else:
            for mdata in response["statewise"]:
                if mdata["state"].lower() == loc.lower():
                    count = (mdata[cnt_type])

            message = "{} cases in {} are {}".format(cnt_type, loc, count)

        dispatcher.utter_message(text=message)

        return []


class ActionSlotRefresh(Action):

    def name(self):
        return "action_slot_refresh"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


