import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

gemini_api_key = os.environ.get("GEMINI_API_KEY")

def get_weather_data(api_key: str, location: str, start_date: str, end_date: str) -> dict:

    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e.__str__)
        


def generate_itinerary(source, destination, start_date, end_date, no_of_day):
    prompt = f"Generate a personalized trip itinerary for a {no_of_day}-day trip from {source} to {destination} from {start_date} to {end_date}, with an optimum budget (Currency: INR)."
    try:
        response = model.generate_content(prompt)
        if response and response.candidates:
            itinerary_text = response.candidates[0].content.parts[0].text
            return itinerary_text
        else:
            return "Sorry, no itinerary could be generated. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error in generating itinerary: {e}"

