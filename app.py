from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import fcntl

app = Flask(__name__)

def get_horoscope(zodiac_sign, month, day, year):
    url = f"https://www.vogue.in/horoscope/collection/horoscope-today-{month}-{day}-{year}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to retrieve the horoscope. Please try again later."

    soup = BeautifulSoup(response.content, 'html.parser')
    horoscopes = soup.find_all('h2')
    
    for horoscope in horoscopes:
        title = horoscope.get_text(strip=True).lower()
        if zodiac_sign.lower() in title:
            content = horoscope.find_next('span').get_text(strip=True)
            return content
    
    return "Horoscope for the given zodiac sign not found."

@app.route('/', methods=['GET', 'POST'])
def horoscope():
    horoscope_text = ""
    if request.method == 'POST':
        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        user_month = date_obj.strftime('%B').lower()
        user_day = date_obj.strftime('%d').lower()
        user_year = date_obj.strftime('%Y').lower()
        user_horoscope = request.form['horoscope'].lower()
        horoscope_text = get_horoscope(user_horoscope, user_month, user_day, user_year)
    return render_template('index.html', horoscope_text=horoscope_text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use the PORT environment variable if set, otherwise default to 5000
    app.run(host="0.0.0.0", port=port)
