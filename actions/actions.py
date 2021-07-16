from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from actions.database_connectivity import dataupdate
from actions.unique_id import random_generator_id
from actions.queries import executequery
from actions.unique_id import generate_otp
#from actions.summarizer import gmailsummarise


class ActionCredentialForm(Action):

    def name(self) -> Text:
        return "credential_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", "email_id", "phone_number", "service", "information"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict]:
        dispatcher.utter_message(response="utter_submit")
        return []


class ValidateCredentialForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_credential_form"

    def validate_name(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:

        print(f"name given = {slot_value} length = {len(slot_value)}")
        contains_digit = False
        s = slot_value
        for character in s:
            if character.isdigit():
                contains_digit = True

        if contains_digit or len(slot_value) <= 2 or '@' in s:
            dispatcher.utter_message(text=f"I'm assuming you mis-spelled the name.")
            return {"name": None}
        else:
            return {"name": slot_value.capitalize()}

    def validate_email_id(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                          domain: DomainDict) -> Dict[Text, Any]:

        email = slot_value.lower()
        if '.com' in email and '@' in email:
            return {"email_id": slot_value.lower()}
        else:
            dispatcher.utter_message(text=f"I'm assuming you mis-spelled the email id.")
            return {"email_id": None}

    def validate_phone_number(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                              domain: DomainDict) -> Dict[Text, Any]:

        num = slot_value

        if len(num) != 10:
            dispatcher.utter_message(text=f"I'm assuming you mis-spelled the number.")
            return {"phone_number": None}
        else:
            return {"phone_number": slot_value}

    def validate_information(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker,
                             domain: DomainDict) -> Dict[Text, Any]:

        if len(slot_value) < 10:
            dispatcher.utter_message(text=f"Could you please explain it, again?")
            return {"information": None}
        else:
            return {"information": slot_value}


class ActionSubmit(Action):

    def name(self) -> Text:
        return "action_submit"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        random_ID = random_generator_id()
        dataupdate(
            random_ID,
            tracker.get_slot("name"),
            tracker.get_slot("email_id"),
            tracker.get_slot("phone_number"),
            tracker.get_slot("service"),
            tracker.get_slot("information")
        )
        dispatcher.utter_message(response="utter_submit")
        dispatcher.utter_message(text=f"Your unique id is {random_ID}")

        return []


class ActionStatusForm(Action):

    def name(self) -> Text:
        return "status_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["unique_id", "otp_number"]

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any], ) -> List[Dict]:
        dispatcher.utter_message(text="Value Submitted")
        return []


class ValidateStatusForm(FormValidationAction):

    otp = generate_otp()

    def name(self) -> Text:
        return "validate_status_form"

    def validate_unique_id(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:

        print(f"id given = {slot_value}")
        s = slot_value
        if len(s) != 8:
            dispatcher.utter_message(text=f"I'm assuming you mis-spelled your unique ID")
            return {"unique_id": None}
        else:
            v = executequery(s)
            if len(v) == 0:
                dispatcher.utter_message(text=f"Sorry, We don't have any information regarding this unique ID")
                return {"unique_id": None}
            else:
                mobile_number_of_user = '+91' + str(v[0][1])
                print(self.otp)

                account_sid = 'account_sid'
                auth_token = 'auth_token'

                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                    body=f"Your OTP is {self.otp}️",
                    from_='+1407*******',
                    to=mobile_number_of_user
                )
                print(message.status)

                return {"unique_id": slot_value}

    def validate_otp_number(self, slot_value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:

        print(f"otp given = {slot_value}")
        s = slot_value
        if len(s) != 6 and s != self.otp:
            dispatcher.utter_message(text=f"I'm assuming you mis-spelled your OTP")
            return {"otp_number": None}
        else:
            return {"otp_number": slot_value}


class ActionStatus(Action):

    def name(self) -> Text:
        return "action_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.get_slot("unique_id")
        value = executequery(user_id)
        name_of_user = value[0][0]
        mobile_number_of_user = '+91' + str(value[0][1])
        status_of_user = value[0][2]
        message = f"{name_of_user}, Your status is {status_of_user}."
        dispatcher.utter_message(text=message)
        return []


#class ActionSummarise(Action):

#    def name(self) -> Text:
#        return "action_summarise"

#    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        message = gmailsummarise()
#        dispatcher.utter_message(text=message)


