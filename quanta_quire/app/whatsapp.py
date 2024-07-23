from flask import Flask, jsonify, request, current_app
import requests
import random

from quanta_quire.app.chat import chat
from quanta_quire.helper import custom_responses



# Required webhook verifictaion for WhatsApp
# info on verification request payload:
# https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
def verify(request):
  # Parse params from the webhook verification request
  mode = request.args.get("hub.mode")
  token = request.args.get("hub.verify_token")
  challenge = request.args.get("hub.challenge")
  # Check if a token and mode were sent
  if mode and token:
    # Check the mode and token sent are correct
    if mode == "subscribe" and token == current_app.config['VERIFY_TOKEN']:
      # Respond with 200 OK and challenge token from the request
      print("WEBHOOK_VERIFIED")
      return challenge, 200
    else:
      # Responds with '403 Forbidden' if verify tokens do not match
      print("VERIFICATION_FAILED")
      return jsonify({"status": "error", "message": "Verification failed"}), 403
  else:
    # Responds with '400 Bad Request' if verify tokens do not match
    print("MISSING_PARAMETER")
    return jsonify({"status": "error", "message": "Missing parameters"}), 400


# handle incoming webhook messages
def handle_message(request):
  # Parse Request body in json format
  body = request.get_json()
  print(f"request body: {body}")

  try:
    # info on WhatsApp text message payload:
    # https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
    if body.get("object"):
      if (
          body.get("entry")
          and body["entry"][0].get("changes")
          and body["entry"][0]["changes"][0].get("value")
          and body["entry"][0]["changes"][0]["value"].get("messages")
          and body["entry"][0]["changes"][0]["value"]["messages"][0]
      ):
        handle_whatsapp_message(body)
      return jsonify({"status": "ok"}), 200
    else:
      # if the request is not a WhatsApp API event, return an error
      return (
        jsonify({"status": "error", "message": "Not a WhatsApp API event"}),
        404,
      )
  # catch all other errors and return an internal server error
  except Exception as e:
    print(f"unknown error: {e}")
    return jsonify({"status": "error", "message": str(e)}), 500


# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
  message = body["entry"][0]["changes"][0]["value"]["messages"][0]
  if message["type"] == "text":
    message_body = message["text"]["body"]

  # elif message["type"] == "audio":
  #   audio_id = message["audio"]["id"]
  #   message_body = handle_audio_message(audio_id)

  # TODO: Disable this to reduce AI token usage for testing
  response = make_openai_request(message_body, message["from"])
  #response = random_response(message_body, message["from"])
  send_whatsapp_message(body, response)


def random_response(message, from_number):
  # message_log = update_message_log(message, from_number, "user")
  print(f"DEBUG: {message}")

  # Lowercase the user input for case-insensitive matching
  lower_input = message.lower()

  # Check if the user's input matches a keyword in the dictionary
  for keyword, response_list in custom_responses.items():
    if keyword in lower_input:
      # Return a random response from the matching keyword's list
      response_message = random.choice(response_list)
      print(f"custome response: {response_message}")
      return response_message

  # If no keyword match is found, return a default response
  response_message = random.choice(custom_responses["default"])
  print(f"custome response: {response_message}")
  # update_message_log(response_message, from_number, "assistant")
  return response_message


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    headers = {
        "Authorization": f"Bearer {current_app.config['WHATSAPP_TOKEN']}",
        "Content-Type": "application/json",
    }
    url = "https://graph.facebook.com/v20.0/" + phone_number_id + "/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": from_number,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(url, json=data, headers=headers)
    print(f"whatsapp message response: {response.json()}")
    response.raise_for_status()


def make_openai_request(message, from_number):
  try:
    current_app.logger.info(from_number)
    current_app.logger.info(message)
    response_message = chat(from_number, message)
    print(f"openai response: {response_message}")
  except Exception as e:
    print(f"openai error: {e}")
    response_message = "Mohon maaf, API OpenAI saat ini sedang sibuk atau tidak terhubung. Silahkan coba lagi nanti."
  return response_message