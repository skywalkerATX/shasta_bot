import os  # for environment variables
from flask import Flask, request # for web server and requests in Heroku
from twilio.twiml.messaging_response import MessagingResponse # for phone number
import openai # for ya know

from dotenv import load_dotenv # for environment variables from Procfile

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # DO NOT add your key here - refer to README.md. Use this variable name in your .env file.

TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")  # Same with this one

def generate_chatbot_response(prompt):  # This is the function that generates the response from the chatbot, modified from the MARV chatbot example. 
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.4, # 0.8 is the MARV default
        max_tokens=80,
        top_p=0.8, # 0.3 is the default
        frequency_penalty=0.6,  # .7 is the default
        presence_penalty=0.4 # 0.2 is the default
    )
    return response.choices[0].text.strip()

@app.route("/sms", methods=["POST"]) # This is the function that handles the incoming SMS message
def sms_reply(): 
    incoming_msg = request.values.get("Body", "").strip()
    prompt = f"You: {incoming_msg}\nShasta:"  # you can change the name of the chatbot here
    chatbot_response = generate_chatbot_response(prompt)

    twiml_resp = MessagingResponse()
    twiml_resp.message(chatbot_response)
    return str(twiml_resp)

if __name__ == "__main__": # This is the function that runs the web server
    app.run(debug=True)