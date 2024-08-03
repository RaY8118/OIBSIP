import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
import json
file = json.load(open('key.json'))
api_key = file["api_key"]

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a vertical layout
        layout = QVBoxLayout()

        # Create a label for instructions
        self.instruction_label = QLabel('Enter the name of the city:', self)
        layout.addWidget(self.instruction_label)

        # Create a textbox for user input
        self.city_input = QLineEdit(self)
        layout.addWidget(self.city_input)

        # Create a button to trigger the API call
        self.button = QPushButton('Get Weather', self)
        layout.addWidget(self.button)

        # Create a label to display the results
        self.result_label = QLabel('', self)
        layout.addWidget(self.result_label)

        # Connect the button's clicked signal to the function
        self.button.clicked.connect(self.get_weather)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def get_weather(self):
        # Function to be executed when the button is clicked
        city = self.city_input.text()
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

        try:
            response = requests.get(url, verify=False).json()
            city_name = response["location"]["name"]
            country = response["location"]["country"]
            temp_c = response["current"]["temp_c"]
            humidity = response["current"]["humidity"]
            conditions = response["current"]["condition"]["text"]

            result_text = f"City: {city_name}, {country}\nTemperature: {temp_c}°C\nHumidity: {humidity}%\nConditions: {conditions}"
        except Exception as e:
            result_text = f"Error: {e}"

        self.result_label.setText(result_text)

def main():
    app = QApplication(sys.argv)
    ex = WeatherApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
