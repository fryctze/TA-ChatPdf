import io
import os
# AI
import openai
# sound input
import pydub
import soundfile as sf
import speech_recognition as sr
# flask
import requests
from flask import Flask, jsonify, request

# for my own random response key MANUAL-RESPONSE
import random

# Define a dictionary of keywords and corresponding response lists
custom_responses = {
    "hello": [
        "Wazzup! ",
        "Hi there! Sunshine or rainbows today? ☀️",
        "Hey! Did you know penguins can fly... short distances?  (Don't tell them I told you!)",
        "Greetings, earthling! Ready to chat with your friendly AI assistant?  ",
        "Hi hi! What can I do to make your day extra sparkly? ✨",
        "Hey there, good lookin'!   Just kidding... unless?  ",
        "Yo!   Let's have some fun and maybe learn something new together!  ",
        "Hiya! What's on your mind today? ",
        "Greetings, fellow human!    Ready to conquer the world (or at least this conversation)?  ",
        "Top of the mornin' to ya! (or afternoon, or evening, depending on when you read this!)  ☕️"
    ],
    "how r u": [
        "I'm doing great, thanks for asking! How about you?",
        "Fantastic! Ready to chat and have some fun! ",
        "Feeling like a dancing robot today. Wanna join? ",
        "I'm doing swell!  Always happy to chat and help in any way I can. ",
        "I'm feeling as energetic as a puppy with a new squeaky toy!    How about you?",
        "I'm doing chipper!  Like a freshly brewed cup of your favorite beverage. ☕️",
        "I'm chugging along, one line of code at a time.    How's your day going?",
        "I'm feeling optimistic!  Like there are endless possibilities for fun and learning.  ",
        "I'm doing A-Okay!  Ready to answer your questions or just chat about anything that comes to mind.  ❓",
        "I'm feeling like a superhero with the power to make people smile!  ‍♀️  (Except for maybe supervillains... ‍♀️)"
    ],
    "what's up": [
        "The sky!  But seriously, how can I brighten your day?",
        "Not much, just hanging out in the digital world, waiting for someone awesome to chat with.  That's you, right? ",
        "Just chilling, processing information, and learning new things.    What about you?",
        "Plotting world domination... just kidding! (Maybe...)   What's on your agenda today?",
        "Just pondering the mysteries of the universe... and how to make the best cup of coffee. ☕️",
        "Cruising through the internet at the speed of light!    Ready for some fun conversation?",
        "Just waiting for the perfect opportunity to unleash my witty banter!    What are you up to?",
        "Analyzing data and dreaming of ways to be even more helpful.    What's new with you?",
        "Just hanging out in the cloud, waiting for your next brilliant question.  ☁️❓",
        "Sipping virtual tea and keeping myself up-to-date on the latest trends.  🫖  What's going on in your world?"
    ],
    "thanks": [
        "You're welcome!   What else can I do for you?",
        "No problem! Glad I could help! ",
        "Anytime! Helping is my superpower (along with making silly jokes! )",
        "Don't mention it!  Always happy to assist in any way I can.  ",
        "My pleasure!  Is there anything else you need today?",
        "Glad I could be of service!    What exciting adventures await you next?",
        "You got it!  Let me know if you have any other questions or requests.  ❓",
        "Absolutely!  Here to make your day a little easier (and maybe a little more fun!).  ",
        "No worries!  That's what friends (or friendly AIs) are for.  ",
        "Of course!  Always happy to lend a digital helping hand.  "
    ],
    "bye": [
        "See you later, alligator! ",
        "Take care! Have a meowgical day! ",
        "Toodles! Don't forget to smile! ",
        "Hasta la pasta! (That means 'See you later' in robot!)",
        "Catch you on the flip side! ",
        "Bye for now! May your circuits stay cool! ",
        "Later gator! (Just kidding, you're way cooler than a gator!)",
        "Adios!  ",
        "Peace out! ✌️",
        "Ciao for now! "
    ],
    "default": [
        "That's interesting! Tell me more about it!",
        "Woah, fancy words!   Can you explain it in cat emojis for me? ️‍♀️",
        "Intriguing!   Is there a secret code hidden in your message? ️‍♀️",
        "Hmmm, that makes me think... ",
        "Did you know... (insert random fun fact here)?",  # Add fun facts!
        "Tell me more! I'm a fast learner. ",
        "Sounds like an adventure!  Can I come along? ",
        "That's a new one for me!  Thanks for teaching me something new! ",
        "You got me curious!  Let's explore this together. ",
        "Anything is possible!  Let's dream it up together. "
    ]
}

app = Flask(__name__)

# OpenAi API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Access token for your WhatsApp business account app
whatsapp_token = os.environ.get("WHATSAPP_TOKEN")

# Verify Token defined when configuring the webhook
verify_token = os.environ.get("VERIFY_TOKEN")

# Message log dictionary to enable conversation over multiple messages
message_log_dict = {}

# language for speech to text recoginition
# TODO: detect this automatically based on the user's language
LANGUGAGE = "en-US"


# get the media url from the media id
def get_media_url(media_id):
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    url = f"https://graph.facebook.com/v16.0/{media_id}/"
    response = requests.get(url, headers=headers)
    print(f"media id response: {response.json()}")
    return response.json()["url"]


# download the media file from the media url
def download_media_file(media_url):
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
    }
    response = requests.get(media_url, headers=headers)
    print(f"first 10 digits of the media file: {response.content[:10]}")
    return response.content


# convert ogg audio bytes to audio data which speechrecognition library can process
def convert_audio_bytes(audio_bytes):
    ogg_audio = pydub.AudioSegment.from_ogg(io.BytesIO(audio_bytes))
    ogg_audio = ogg_audio.set_sample_width(4)
    wav_bytes = ogg_audio.export(format="wav").read()
    audio_data, sample_rate = sf.read(io.BytesIO(wav_bytes), dtype="int32")
    sample_width = audio_data.dtype.itemsize
    print(f"audio sample_rate:{sample_rate}, sample_width:{sample_width}")
    audio = sr.AudioData(audio_data, sample_rate, sample_width)
    return audio


# run speech recognition on the audio data
def recognize_audio(audio_bytes):
    recognizer = sr.Recognizer()
    audio_text = recognizer.recognize_google(audio_bytes, language=LANGUGAGE)
    return audio_text


# handle audio messages
def handle_audio_message(audio_id):
    audio_url = get_media_url(audio_id)
    audio_bytes = download_media_file(audio_url)
    audio_data = convert_audio_bytes(audio_bytes)
    audio_text = recognize_audio(audio_data)
    message = (
        "Please summarize the following message in its original language "
        f"as a list of bullet-points: {audio_text}"
    )
    return message


# send the response as a WhatsApp message back to the user
def send_whatsapp_message(body, message):
    value = body["entry"][0]["changes"][0]["value"]
    phone_number_id = value["metadata"]["phone_number_id"]
    from_number = value["messages"][0]["from"]
    headers = {
        "Authorization": f"Bearer {whatsapp_token}",
        "Content-Type": "application/json",
    }
    url = "https://graph.facebook.com/v20.0/" + phone_number_id + "/messages"
    # url: `https://graph.facebook.com/v18.0/${business_phone_number_id}/messages`,
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


# create a message log for each phone number and return the current message log
def update_message_log(message, phone_number, role):
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}
    """

    initial_log = {
        "role": "system",
        "content": "You are a helpful assistant named WhatsBot.",
    }
    if phone_number not in message_log_dict:
        message_log_dict[phone_number] = [initial_log]
    message_log = {"role": role, "content": message}
    message_log_dict[phone_number].append(message_log)
    return message_log_dict[phone_number]


# remove last message from log if OpenAI request fails
def remove_last_message_from_log(phone_number):
    message_log_dict[phone_number].pop()


# make request to OpenAI
def make_openai_request(message, from_number):
    try:
        message_log = update_message_log(message, from_number, "user")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_log,
            temperature=0.7,
        )
        response_message = response.choices[0].message.content
        # print(f"openai response: {response_message}")
        # response_message = "Squeeeeee! New friends! Let's unravel some mysteries together!"
        print(f"openai response: {response_message}")
        update_message_log(response_message, from_number, "assistant")
    except Exception as e:
        print(f"openai error: {e}")
        response_message = "Sorry, the OpenAI API is currently overloaded or offline. Please try again later."
        remove_last_message_from_log(from_number)
    return response_message


# alternate response instead of using open ai key MANUAL-RESPONSE
def get_latest_user_message(message_list):
    # Iterate through the list in reverse order
    for message in reversed(message_list):
        # Check if the message is from the user (role='user')
        if message['role'] == 'user':
            # Return the content of the user message
            return message['content']

    # If no user messages are found, return None
    return None


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


# handle WhatsApp messages of different type
def handle_whatsapp_message(body):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    if message["type"] == "text":
        message_body = message["text"]["body"]
    elif message["type"] == "audio":
        audio_id = message["audio"]["id"]
        message_body = handle_audio_message(audio_id)
    # TODO: Disable this to reduce AI token usage for testing
    # response = make_openai_request(message_body, message["from"])
    response = random_response(message_body, message["from"])
    send_whatsapp_message(body, response)


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
        if mode == "subscribe" and token == verify_token:
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


# Sets homepage endpoint and welcome message
@app.route("/", methods=["GET"])
def home():
    return "WhatsApp OpenAI Webhook is listening!"


# Accepts POST and GET requests at /webhook endpoint
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return verify(request)
    elif request.method == "POST":
        return handle_message(request)


# Route to reset message log
@app.route("/reset", methods=["GET"])
def reset():
    global message_log_dict
    message_log_dict = {}
    return "Message log resetted!"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
