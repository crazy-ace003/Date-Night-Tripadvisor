
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
 logger.info(event)
 logger.info(context)
 try:
   if event['session']['new']:
     logger.info('Session started')
   request_type = event['request']['type']
   if request_type == 'LaunchRequest':
       response = launch_request()
       logger.info(response)
       return response
   elif request_type == 'IntentRequest':
       user_id = event['request']['intent']['slots']['User']['value']
       response = intent_request(user_id)
       logger.info(response)
       return response
   elif request_type == 'SessionEndedRequest':
     print 'Session ended'
 except Exception, error:
   print ('Received an unexpected request type' + str(error))
   return []

def session_started():
   print 'do nothing'

def launch_request():
   card_title = 'Welcome'
   speech_output = 'Welcome to get a user. What user should I get?'
   reprompt_text = 'What user should I get?'
   should_end_session = False
   session_attributes = {}
   speechlet_response = build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
   response = build_response(session_attributes, speechlet_response)
   return response

def intent_request(user_id):
   table = 'test'
   dynamo = boto3.resource('dynamodb').Table(table)
   user = dynamo.get_item(TableName=table, Key={'UserID': user_id})
   username = user['Item'].get('FirstName')
   card_title = 'Welcome'
   speech_output = username
   reprompt_text = 'Where am I?'
   should_end_session = True
   session_attributes = {}
   speechlet_response = build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session)
   response = build_response(session_attributes, speechlet_response)
   return response

def session_ended():
   print 'Session Ended'

def build_speechlet_response(card_title, speech_output, reprompt_text,
                            should_end_session):
 output_speech = {
                 'outputSpeech': {
                   'type': 'PlainText',
                   'text': speech_output
                 },
                 'card': {
                   'type': 'Simple',
                   'title': 'SessionSpeechlet - ' + card_title,
                   'content': 'SessionSpeechlet - ' + speech_output
                 },
                 'reprompt': {
                   'outputSpeech': {
                     'type': 'PlainText',
                     'text': reprompt_text
                   }
                 },
                 'shouldEndSession': should_end_session
                 }
 return output_speech

def build_response(session_attributes, speechlet_response):
   response = {
       'version': '1.0',
       'sessionAttributes': session_attributes,
       'response': speechlet_response
       }
   return response
