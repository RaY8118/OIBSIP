import sys
import requests, json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QHBoxLayout, QScrollArea, QComboBox,QStatusBar
)
from datetime import datetime


# Your API key (replace with your actual API key)
file = json.load(open('key.json'))
api_key = file["api_key"]


class HeaderSection(QWidget):
    def __init__(self):
        super().__init__()

        # App Title
        self.title_label = QLabel("Weather App")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: #ffffff;
            background-color: #2196F3;
            padding: 15px;
            border-radius: 8px;
        """)

        # City Input
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter City Name")
        self.city_input.setStyleSheet("""
            padding: 10px;
            font-size: 14pt;
            border-radius: 8px;
            border: 1px solid #2196F3;
            background-color: #e3f2fd;
        """)

        # Fetch Weather Button
        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.setStyleSheet("""
            padding: 10px;
            font-size: 14pt;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        """)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)



class ForecastSection(QGroupBox):
    def __init__(self):
        super().__init__("7-day Forecast")
        self.setStyleSheet("""
            QGroupBox {
                background-color: #f4f4f4;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
            QGroupBox::title {
                subcontrol-origin: padding;
                padding-left: 10px;
                color: #333;
                font-size: 18pt;
                font-weight: bold;
            }
        """)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def update_forecast(self, data):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for day in data:
            date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
            day_of_week = date_obj.strftime('%A')

            # Create a widget for each day's forecast
            day_widget = QWidget()

            # Layout for the day's forecast
            day_layout = QHBoxLayout()

            # Day label
            day_label = QLabel(day_of_week)
            day_label.setStyleSheet("""
                font-size: 16pt;
                font-weight: bold;
                color: #333;
                margin-right: 10px;
            """)
            day_layout.addWidget(day_label)

            # Temperature range
            temp_range_label = QLabel(f"{day['day']['mintemp_c']}°C / {day['day']['maxtemp_c']}°C")
            temp_range_label.setStyleSheet("""
                color: #555;
                font-size: 14pt;
            """)
            day_layout.addWidget(temp_range_label)

            # Set layout to the day's widget
            day_widget.setLayout(day_layout)
            self.layout.addWidget(day_widget)




class HourlyForecastSection(QWidget):
    def __init__(self):
        super().__init__()

        self.date_combo = QComboBox()
        self.date_combo.setStyleSheet("""
            padding: 10px;
            font-size: 14pt;
            border-radius: 8px;
            border: 1px solid #2196F3;
            background-color: #e3f2fd;
        """)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.date_combo)
        layout.addWidget(self.scroll_area)
        layout.setSpacing(0)

        self.setLayout(layout)

    def show_hourly_forecast(self, data, selected_date):
        for i in reversed(range(self.content_layout.count())):
            self.content_layout.itemAt(i).widget().setParent(None)

        for day in data:
            if day["date"] == selected_date:
                for hour in day["hour"]:
                    hour_text = f"{hour['time'].split(' ')[1]} - {hour['temp_c']}°C | {hour['wind_kph']} kph | {hour['humidity']}%"
                    hour_label = QLabel(hour_text)
                    hour_label.setFont(QFont('Arial', 12))
                    hour_label.setStyleSheet("""
                        padding: 12px;
                        border-bottom: 1px solid #ddd;
                        background-color: #e3f2fd;
                        border-radius: 5px;
                    """)
                    self.content_layout.addWidget(hour_label)
                break



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        header_layout = QVBoxLayout()
        self.header_section = HeaderSection()
        header_layout.addWidget(self.header_section)
        header_layout.addStretch()

        self.forecast_section = ForecastSection()
        layout.addWidget(self.forecast_section)

        self.hourly_forecast_section = HourlyForecastSection()
        layout.addWidget(self.hourly_forecast_section)

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addLayout(layout)
        central_widget.setLayout(main_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.header_section.get_weather_button.clicked.connect(self.get_weather)
        self.hourly_forecast_section.date_combo.currentIndexChanged.connect(self.update_hourly_forecast)

        self.setStyleSheet("background-color: #f0f0f0;")


    def get_weather(self):
        city = self.header_section.city_input.text()
        url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no'

        try:
            response = requests.get(url).json()
            self.data = response["forecast"]["forecastday"]
            self.hourly_forecast_section.date_combo.clear()
            for day in self.data:
                self.hourly_forecast_section.date_combo.addItem(day['date'])

            location_info = f"Weather data for {response['location']['name']}, {response['location']['country']}"
            self.status_bar.showMessage(location_info)
            self.forecast_section.update_forecast(self.data)
        except Exception as e:
            self.status_bar.showMessage(f"Error: {e}")

    def update_hourly_forecast(self):
        index = self.hourly_forecast_section.date_combo.currentIndex()
        if index != -1:
            selected_date = self.hourly_forecast_section.date_combo.itemText(index)
            self.hourly_forecast_section.show_hourly_forecast(self.data, selected_date)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Weather App")
    window.resize(1000, 600)  # Adjust window size as needed
    window.show()
    sys.exit(app.exec_())
