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

import requests
import json

class CovidForm(FormAction):

    def name(self) -> Text:
        return "Covid_Form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return["count_type", "location"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

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
        
        if value.lower() in self.count_type_db():
            return {"count_type": value}
        else:
            dispatcher.utter_message(template="utter_wrong_count_type")
            return {"count_type": None}
        

    @staticmethod
    def location_db() -> List[Text]:
        return [
            "maharashtra",
            "tamil nadu",
            "delhi",
            "telangana",
            "rajasthan",
            "kerala",
            "uttar pradesh",
            "andhra pradesh",
            "madhya pradesh",
            "karnataka",
            "gujarat",
            "haryana",
            "jammu and kashmir",
            "punjab",
            "best bengal",
            "odisha",
            "bihar",
            "uttarakhand",
            "assam",
            "chandigarh",
            "himachal pradesh",
            "ladakh",
            "andaman and nicobar islands",
            "chhattisgarh",
            "goa",
            "puducherry",
            "jharkhand",
            "manipur",
            "mizoram",
            "arunachal pradesh",
            "dadra and nagar haveli",
            "tripura",
            "daman and diu",
            "lakshadweep",
            "meghalaya",
            "nagaland",
            "sikkim",
        ]


    def validate_location(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.lower() in self.location_db():
            return {"location": value}
        else:
            dispatcher.utter_message(template="utter_wrong_location")
            return {"location": None}


    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:

        loc = tracker.get_slot('location')
        cnt_type = tracker.get_slot('count_type')

        message = "Received input location as -> {} and count_type as {}".format(loc, cnt_type)

        # dispatcher.utter_message(text=message)

        return []

class ActionResults(Action):

    def name(self):
        return "action_results"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        loc = tracker.get_slot('location')
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


