# Shasta Textbot Deployment Guide

This guide will help you set up and deploy the Shasta (or name it whatever you want) textbot using OpenAI, Flask, Heroku, and Twilio. 

Shasta is the name of the hero from CS Lewis's Narnia Chronicles', ["The Horse and His Boy"](https://en.wikipedia.org/wiki/The_Horse_and_His_Boy). The name is just something I came up with quickly and not especially fitting, given that this is repurposed from OpenAI's "Marv" bot that's designed to be nothing but a snarky assistant with no power (to access the internet).

If you tool around in the [Marv bot OpenAI playground](https://platform.openai.com/playground/p/default-marv-sarcastic-chat?model=text-davinci-003) you can try tweaking models then replicate those model settings in your main.py model file. 

The instructions below will walk you through the process of creating an OpenAI API key, setting up a Heroku app, configuring Twilio, and modifying the textbot responses.

## Table of Contents

- [Shasta Textbot Deployment Guide](#shasta-textbot-deployment-guide)
  - [Table of Contents](#table-of-contents)
  - [Create an OpenAI API Key](#create-an-openai-api-key)
  - [Environment Setup and .env File](#environment-setup-and-env-file)
  - [Setting up Twilio](#setting-up-twilio)
  - [Setting up Heroku](#setting-up-heroku)
  - [Modifying the Chatbot Responses](#modifying-the-chatbot-responses)
  - [A Note on Costs and Sharing the Phone Number](#a-note-on-costs-and-sharing-the-phone-number)
    - [As of April 23, 2023](#as-of-april-23-2023)

## Create an OpenAI API Key

1. Go to the [OpenAI website](https://beta.openai.com/signup) and create an account if you don't have one already.
2. After signing up or logging in, navigate to the [API Keys page](https://beta.openai.com/account/api-keys).
3. Click on the "Create API key" button and take note of the generated key. This key will be used to authenticate requests to the OpenAI API.

## Environment Setup and .env File

To keep your API keys and other sensitive information secure, use a `.env` file to store them. This file should be added to your project's `.gitignore` so that it is not tracked by version control and accidentally shared.

Create a `.env` file in the root of your project and add the following variables:

```python
OPENAI_API_KEY=your_openai_api_key
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```


Replace `your_openai_api_key` and `your_twilio_phone_number` with the actual values you obtained from OpenAI and Twilio.

## Setting up Twilio

1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio) if you don't have one already.
2. After signing up or logging in, go to the [Phone Numbers page](https://www.twilio.com/console/phone-numbers/incoming) and click on "Get a Trial Number" or "Buy a Number" if you want a specific number.
3. Once you have a Twilio phone number, navigate to the phone number's configuration page.
4. Scroll down to the "Messaging" section and set the "A MESSAGE COMES IN" webhook to your Heroku app's `/sms` endpoint (e.g., `https://your-heroku-app.herokuapp.com/sms`). Make sure the request method is set to "HTTP POST".
5. Save your changes on the Twilio phone number configuration page.

## Setting up Heroku

1. Sign up for a [Heroku account](https://signup.heroku.com/) if you haven't already.
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and log in by running `heroku login` in your command line.
3. In the root directory of your project, run `heroku create` to create a new Heroku app.
4. Push your code to Heroku by running `git push heroku main`.
5. Set the environment variables on Heroku:
```python
heroku config:set OPENAI_API_KEY=your_openai_api_key
heroku config:set TWILIO_PHONE_NUMBER=your_twilio_phone_number
```
6. (Optional) Scale your app by running `heroku ps:scale web=1`.
7. Visit your app's URL (displayed in the Heroku dashboard) to check if it's running.

## Modifying the Chatbot Responses
To modify the chatbot responses, you can adjust the parameters passed to the openai.Completion.create() function in

file. Some of the key parameters to tweak are:

- `temperature`: Controls the randomness of the generated responses. Higher values (e.g., 1.0) will make the output more random and creative, while lower values (e.g., 0.2) will make it more focused and deterministic.
- `max_tokens`: The maximum number of tokens (words or word pieces) in the generated response. Adjusting this value controls the length of the response.
- `top_p`: This parameter controls the nucleus sampling. Adjusting this value may influence the diversity of the generated responses. A higher value (e.g., 0.8) may result in more diverse responses, while a lower value (e.g., 0.3) will likely result in more conservative ones.
- `frequency_penalty`: This parameter can be used to encourage or discourage the use of common words or phrases. A higher frequency_penalty value (e.g., 0.8 or even 1.0) will encourage the model to generate less frequent or more unusual words and phrases, which can lead to more creative outputs.
- `presence_penalty`: This parameter influences the repetition of words or phrases within the generated response. A higher presence_penalty value (e.g., 0.5 or even 1.0) will discourage the model from repeating the same words or phrases within the response, which can lead to more creative and diverse outputs.


## A Note on Costs and Sharing the Phone Number

Keep an eye on the costs associated with using OpenAI, Heroku, and Twilio services, as some of them may have fees depending on your usage. 

### As of April 23, 2023

- `Twilio`: Bills at \\$.0079 per in/outbound text. That's \\$.0158 per conversation. This can add up quickly. Carrier fees usually average 50% of your conversation fees, so around \\$.008 in carrier fees per post and response. The initial fee for phone number setup is a one-time \\$4. There's also a \\$1.55/month local phone number fee and \\$.75/month 911 fee. 
  
- `Heroku`: This will work consistently provided you use the Hobby level dyno Gunicorn (Green Unicorn). This costs \\$7/month. If you turn off the Hobby dyno and opt for free, you may notice delayed responses or configuring error notices sent from twilio. 

Make sure to monitor your usage and adjust your plan accordingly to avoid unexpected charges. This goes for Heroku. 

Most importantly, be mindful when sharing your Twilio phone number. If people share your bot it could spread exponentially, leading to fees you never intended! 
