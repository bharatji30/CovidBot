## covid form inquiry
* greet
  - utter_greet
  - utter_aim
* pull_from
  - action_slot_refresh
  - Covid_Form
  - form{"name": "Covid_Form"}
  - form{"name": null}
  - slot{"count_type":"confirmed"}
  - slot{"location":"Delhi"}
  - action_results
* context
  - action_results
* pull_from_filled
  - action_results
* goodbye
  - utter_goodbye


## covid pre-filled form inquiry
* greet
  - utter_greet
  - utter_aim
* pull_from_filled
  - action_results
* context
  - action_results
* goodbye
  - utter_goodbye


## covid invalid form inquiry
* greet
  - utter_greet
  - utter_aim
* pull_from
  - action_slot_refresh
  - Covid_Form
  - form{"name": "Covid_Form"}
* chitchat
  - utter_chitchat
  - Covid_Form
  - form{"name": null}
  - slot{"count_type":"confirmed"}
  - slot{"location":"Delhi"}
* goodbye
  - utter_goodbye




## say goodbye
* goodbye
  - utter_goodbye