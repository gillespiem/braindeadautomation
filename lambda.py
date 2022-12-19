# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import json
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can say Hello or Help. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class SynergyIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SynergyIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #r = requests.get('http://www.braindeadprojects.com/ip')
        
        
        slot = ask_utils.request_util.get_slot(handler_input, "synergydevice")
        
        #speak_output = "Hello World batman!"
        if slot.value and slot.value in ("laptop", "desktop"):
            
            if slot.value == "laptop":
                r = requests.get('http://66.59.115.2:8080/synergy?synergydevice=laptop')
            elif slot.value == "desktop":
                r = requests.get('http://66.59.115.2:8080/synergy?synergydevice=desktop')        
            response_json = json.loads(r.text)
            
            if response_json["status"] == "0":
                speak_output = "Now setting Synergy master to %s " % slot.value
            else:
                speak_output = "There was an issue changing Synergy Master"
        else:
            speak_output = "I am not clear which device should become master. Please select either laptop or desktop"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class ThermostatGetIntentHandler(AbstractRequestHandler):
    """Handler for ThermostatGet Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ThermostatGet")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        #r = requests.get('http://www.braindeadprojects.com/ip')

        r = requests.get('http://66.59.115.2:8080/thermostat_get')
        response_json = json.loads(r.text)
        
        if response_json["tmode"] == 1:
            mode = "heat"
            set_temp = str(round(response_json["t_heat"]))
        elif response_json["tmode"] == 2:
            mode = "cool"
            set_temp = str(round(response_json["t_cool"]))
        elif response_json["tmode"] == 0:
            mode = "off"

        speak_output = "The thermostat is currently set to %s. The temperature inside is %s" % (mode, str(round(response_json["temp"])))


        if response_json["tmode"] != 0:
            speak_output = "%s and the target temperature is set to %s" % (speak_output, set_temp)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class ThermostatSetIntentHandler(AbstractRequestHandler):
    """Handler for ThermostatSet Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ThermostatSet")(handler_input)

    def handle(self, handler_input):
        slot_mode = ask_utils.request_util.get_slot(handler_input, "mode")
        slot_temperature = ask_utils.request_util.get_slot(handler_input, "setTemperature")
        
        if slot_mode.value in ("heat"):
            t_mode = "heat"
        elif slot_mode.value in ("cool"):
            t_mode = "cool"
        
        json_data = { "thermostat_mode" : t_mode , "setTemperature" : slot_temperature.value }
        
        r = requests.post("http://66.59.115.2:8080/thermostat_set", json = json_data )

        response_json = json.loads(r.text)
        
        if response_json["tmode"] == 1:
            mode = "heat"
            set_temp = str(round(response_json["t_heat"]))
        elif response_json["tmode"] == 2:
            mode = "cool"
            set_temp = str(round(response_json["t_cool"]))
        elif response_json["tmode"] == 0:
            mode = "off"

        speak_output = "The thermostat is now set to %s the house to %s degrees."  % (mode, set_temp)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )




class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

#Matt Gillespie's handlers
sb.add_request_handler(SynergyIntentHandler())
sb.add_request_handler(ThermostatGetIntentHandler())
sb.add_request_handler(ThermostatSetIntentHandler())


sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers



sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
