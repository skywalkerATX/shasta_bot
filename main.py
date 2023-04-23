import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def generate_chatbot_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.4, # 0.8 is the default
        max_tokens=80,
        top_p=0.8, # 0.3 is the default
        frequency_penalty=0.6,  # .7 is the default
        presence_penalty=0.4 # 0.2 is the default
    )
    return response.choices[0].text.strip()

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.values.get("Body", "").strip()
    prompt = f"You: {incoming_msg}\nShasta:"
    chatbot_response = generate_chatbot_response(prompt)

    twiml_resp = MessagingResponse()
    twiml_resp.message(chatbot_response)
    return str(twiml_resp)

if __name__ == "__main__":
    app.run(debug=True)