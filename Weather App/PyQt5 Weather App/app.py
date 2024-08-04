import sys
import requests
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QListWidget, QScrollArea, QHBoxLayout)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# Load API key
file = json.load(open('key.json'))
api_key = file["api_key"]

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a horizontal layout for the main window
        main_layout = QHBoxLayout()

        # Create a vertical layout for the input section
        input_layout = QVBoxLayout()

        # Style for the input section
        input_layout.setContentsMargins(10, 10, 10, 10)
        input_layout.setSpacing(10)

        # Create a label for instructions with styling
        self.instruction_label = QLabel('Enter the name of the city:', self)
        self.instruction_label.setFont(QFont('Arial', 12, QFont.Bold))
        self.instruction_label.setStyleSheet("color: #333333;")
        input_layout.addWidget(self.instruction_label)

        # Create a textbox for user input with styling
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('City name...')
        self.city_input.setFont(QFont('Arial', 10))
        self.city_input.setStyleSheet("padding: 5px; border: 1px solid #cccccc; border-radius: 4px;")
        input_layout.addWidget(self.city_input)

        # Create a button to trigger the API call with styling
        self.button = QPushButton('Get Weather', self)
        self.button.setFont(QFont('Arial', 10, QFont.Bold))
        self.button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 4px;")
        self.button.clicked.connect(self.get_weather)
        input_layout.addWidget(self.button)

        # Create a label to display the results with styling
        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Arial', 10))
        self.result_label.setStyleSheet("color: #555555;")
        self.result_label.setWordWrap(True)
        input_layout.addWidget(self.result_label)

        # Create a list widget to display dates with styling
        self.date_list = QListWidget()
        self.date_list.setStyleSheet("background-color: #f9f9f9; border: 1px solid #cccccc; border-radius: 4px;")
        self.date_list.setFixedWidth(150)
        self.date_list.setFont(QFont('Arial', 10))
        self.date_list.itemClicked.connect(self.show_hourly_forecast)

        # Create a scroll area for hourly forecast with styling
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        # Create a widget to hold the content of the scroll area
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)
        
        # Set a vertical layout for the content widget
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setStyleSheet("background-color: #f9f9f9;")

        # Add the input layout and scroll area to the main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.date_list)
        main_layout.addWidget(self.scroll_area)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('Weather App')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #ffffff;")
        self.show()

    def get_weather(self):
        city = self.city_input.text()
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no'

        try:
            response = requests.get(url, verify=False).json()
            self.data = response["forecast"]["forecastday"]
            
            # Populate the date list with dates
            self.date_list.clear()
            for day in self.data:
                self.date_list.addItem(day['date'])

            self.result_label.setText(f"Weather data for {response['location']['name']}, {response['location']['country']}")
        except Exception as e:
            self.result_label.setText(f"Error: {e}")

    def show_hourly_forecast(self, item):
        # Clear the current content layout
        for i in reversed(range(self.content_layout.count())): 
            self.content_layout.itemAt(i).widget().setParent(None)
        
        # Find the selected date's data
        selected_date = item.text()
        for day in self.data:
            if day["date"] == selected_date:
                for hour in day["hour"]:
                    hour_text = (f"Time: {hour['time']}\n"
                                 f"Temp (C): {hour['temp_c']}°C\n"
                                 f"Wind (kph): {hour['wind_kph']} kph\n"
                                 f"Humidity: {hour['humidity']}%\n"
                                 f"Condition: {hour['condition']['text']}\n")
                    hour_label = QLabel(hour_text)
                    hour_label.setFont(QFont('Arial', 9))
                    hour_label.setStyleSheet("padding: 5px; border-bottom: 1px solid #eeeeee;")
                    self.content_layout.addWidget(hour_label)
                break

def main():
    app = QApplication(sys.argv)
    ex = WeatherApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
