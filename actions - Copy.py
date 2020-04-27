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
            "count_type": self.from_entity(entity="count_type"),
            "location": self.from_entity(entity="location"),
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
        if isinstance(value, str):
            if value.lower() in self.count_type_db():
                return {"count_type": value}
            else:
                dispatcher.utter_message(template="utter_wrong_count_type")
                return {"count_type": None}
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

        location = tracker.get_slot('location')
        count_type = tracker.get_slot('count_type')

        message = "Received input location as -> {} and count_type as {}".format(location, count_type)

        dispatcher.utter_message(text=message)

        return []

class ActionSlotRefresh(Action):

    def name(self):
        return "action_slot_refresh"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

