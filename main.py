import os
import random
import requests
import json
import wikipedia
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def generate_meme(top_text, bottom_text):
    # Choose a random meme template
    meme_url = 'https://api.imgflip.com/get_memes'
    response = requests.get(meme_url)
    memes_data = json.loads(response.text)
    memes = memes_data['data']['memes']
    meme = random.choice(memes)
    meme_url = meme['url']

    # Download the meme image and open it using Pillow
    response = requests.get(meme_url)
    img = Image.open(BytesIO(response.content))

    # Add the text to the meme using Pillow
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(os.path.dirname(__file__), 'arial.ttf')
    font = ImageFont.truetype(font_path, size=random.randrange(200))
    text_color = (255, 255, 255)
    shadow_color = (0, 0, 0)
    x, y = img.size[0]/2, 10
    draw.text((x, y), top_text, font=font, fill=text_color, anchor='mt', stroke_width=2, stroke_fill=shadow_color)
    x, y = img.size[0]/2, img.size[1]-40
    draw.text((x, y), bottom_text, font=font, fill=text_color, anchor='mb', stroke_width=2, stroke_fill=shadow_color)

    # Save the meme image
    output = BytesIO()
    img.save(output, format='JPEG')
    output.seek(0)

    return output

def get_weather(location):
    # Define the base URL for OpenWeatherMap API

    # Add your OpenWeatherMap API key and the location to the request URL
    api_key = 'd0393467ffbd27822d08b4ac29c15ff6'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'

    # Send a request to the OpenWeatherMap API and get the response
    response = requests.get(url)

    # Check if the response contains weather information
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        status = weather_data['weather'][0]['description']

        # Return a string with the current weather information
        return f"The current temperature in {location} is {temperature:.1f}°C and the sky is {status}."
    else:
        # Handle the case where the location is not found
        return f"Sorry, I could not find weather information for {location}."
    
def get_joke():
    # Define the base URL for joke API
    url = 'https://official-joke-api.appspot.com/jokes/random'
    # Send a request to the joke API and get the response
    response = requests.get(url)
    # Check if the response contains a joke
    if response.status_code == 200:
        joke_data = response.json()
        joke_setup = joke_data['setup']
        joke_punchline = joke_data['punchline']
        # Return a string with the joke
        return f"{joke_setup} {joke_punchline}"
    else:
        # Handle the case where the joke API fails to respond
        return "Sorry, I couldn't find a joke at the moment."
def get_wiki(topic):
    try:
        # Set the language to English
        wikipedia.set_lang("en")
        # Get the Wikipedia page for the topic
        page = wikipedia.page(topic)
        # Get the summary of the page
        summary = page.summary
        # Return the summary
        return summary
    except wikipedia.exceptions.PageError:
        # Handle the case where the page is not found
        return f"Sorry, I couldn't find any information on {topic}."
    except wikipedia.exceptions.DisambiguationError:
        # Handle the case where the topic is ambiguous
        return f"Sorry, there are multiple pages for {topic}. Please be more specific."

def generate_response(input_text):
    # Split the user input into words and lowercase them
    words = input_text.lower().split()

    # Check if the user wants to see the weather
    if 'weather' in words:
        location=input("Please specify the location: ")
        weather = get_weather(location)
        # Get the current weather for the location
        if weather:
            response = weather
        else:
            response = f"Sorry, I couldn't get the weather for {location}."

    # Check if the user wants to generate a meme
    elif 'meme' in words:
        # Prompt the user to enter the top and bottom text for the meme
        print("Please specify the top and bottom text for the meme.")
        top_text = input("Top Text: ")
        bottom_text = input("Bottom Text: ")
        # Generate the meme
        meme = generate_meme(top_text, bottom_text)
        # Return the meme as a file
        response = {'file': meme, 'filename': 'meme.jpg'}

    # Check if the user wants to get information from Wikipedia
    elif 'wiki' in words:
        # Extract the topic from the input
        topic=input("Enter the topic you want to search:- ")
        # Get the Wikipedia summary for the topic
        summary = get_wiki(topic)
        response = summary

    elif 'joke' in words:
        joke = get_joke()
        if joke:
            response = joke
        else:
            response = "Sorry, I couldn't get a joke."

    # If the user didn't ask for weather, a meme, or Wikipedia, generate a default response
    else:
        responses = ["Sorry, I don't understand.",
                     "Can you please rephrase that",
                     "I'm not sure what you're asking for.",
                     "Could you please try again?",
                     "I'm afraid I don't know the answer to that."]
        response = random.choice(responses)

    return response
 
while True:
    # Listen for user input
    input_text = input('You: ')

    # Generate a response based on the user input
    response = generate_response(input_text.lower())
    if isinstance(response, dict):
        with open(response['filename'], 'wb') as f:
            f.write(response['file'].getbuffer())
    
    # Print the response to the console
    print('Bot:', response)

    
