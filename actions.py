# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from help.unicodename import remove_non_ascii_normalized


class ActionsStatusCoronaState(Action):

    def name(self) -> Text:
        return "actions_status_corona_state"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get('https://covid19-brazil-api.now.sh/api/report/v1').json()

        entities = tracker.latest_message['entities']
        print('Última mensagem', entities)
        state = None

        for e in entities:
            if e['entity'] == "state":
                state = e['value']
                print(state)

        message =\
            f'Você digitou: {state}, está correto?\n\n' \
            'Hum... que coisa não? eu acho que você esqueceu ou errou alguma letra. Não consegui localizar este ' \
            f'estado({state})\n' \

        for data in response['data']:
            if remove_non_ascii_normalized(data['state']) == remove_non_ascii_normalized(state):
                print(data)
                message =\
                    f"Estado: {data['state']}\n" \
                    f"Casos confirmados: {data['cases']}\n" \
                    f"Supeitos: {data['suspects']}\nMortes: {data['deaths']}\n" \
                    f"Ultima atualização: {data['datetime']}"

        dispatcher.utter_message(text=message)

        return []
