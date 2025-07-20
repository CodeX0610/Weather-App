import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QFont

# Replace with your own OpenWeatherMap API key
API_KEY = '56ea6085fe9103bbb966a4f855aac08f'  # <-- PUT YOUR API KEY HERE

def get_weather(city):
    """Fetch weather data for a city from OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Weather App')
        self.setMinimumWidth(350)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Weather App")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2a82da")
        layout.addWidget(title)

        # Search bar
        search_layout = QHBoxLayout()
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText('Enter city name...')
        search_layout.addWidget(self.city_input)
        self.button = QPushButton('Get Weather')
        self.button.clicked.connect(self.show_weather)
        search_layout.addWidget(self.button)
        layout.addLayout(search_layout)

        # Weather info display
        self.result = QLabel('')
        self.result.setFont(QFont("Arial", 12))
        layout.addWidget(self.result)

        # Set main layout
        self.setLayout(layout)

    def show_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.result.setText("Please enter a city name.")
            return

        data = get_weather(city)
        if data.get('cod') == 200:
            temp = data['main']['temp']
            desc = data['weather'][0]['description'].title()
            feels = data['main']['feels_like']
            humid = data['main']['humidity']
            wind = data['wind']['speed']
            icon_code = data['weather'][0]['icon']
            # Display weather info in Apple-like style
            self.result.setText(
                f"<h3>{city.title()}</h3>"
                f"<b>🌡️ {temp}°C</b> ({desc})<br>"
                f"Feels like: {feels}°C<br>"
                f"Humidity: {humid}%<br>"
                f"Wind: {wind} m/s"
            )
        elif data.get("error"):
            self.result.setText(f"Error: {data['error']}")
        else:
            self.result.setText("City not found or API error.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())