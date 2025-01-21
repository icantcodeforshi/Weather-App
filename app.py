from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your actual WeatherAPI key
API_KEY = "9a538eb6a3c146da95e151646252001"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None

    if request.method == 'POST':
        # Get user input from the form
        location = request.form.get('location', '').strip()

        if location:
            # Construct WeatherAPI request URL
            url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"

            try:
                response = requests.get(url)
                data = response.json()
                print(data)

                # If the API returned an error message
                if "error" in data:
                    weather_data = {
                        "error_message": data["error"].get("message", "An unknown error occurred.")
                    }
                # If 'current' data is present, consider it a successful response
                elif "current" in data:
                    weather_data = data
                else:
                    # No 'error' key but also no 'current' - unexpected data structure
                    weather_data = {"error_message": "No weather data found or an unexpected response."}

            except requests.exceptions.RequestException as e:
                # Catch network errors or other request issues
                weather_data = {"error_message": str(e)}

    # Render the template, passing any weather_data or error message to index.html
    return render_template("index.html", weather_data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
