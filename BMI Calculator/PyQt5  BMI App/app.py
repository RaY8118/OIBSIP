import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox,QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import sqlite3


def init_db():
    conn = sqlite3.connect('bmi_calculator.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bmi_data
                 (weight REAL, height REAL, bmi REAL)''')
    conn.commit()
    conn.close()


def save_data(weight, height, bmi):
    conn = sqlite3.connect('bmi_calculator.db')
    c = conn.cursor()
    c.execute('INSERT INTO bmi_data (weight, height, bmi) VALUES (?, ?, ?)',
              (weight, height, bmi))
    conn.commit()
    conn.close()


def plot_data():
    conn = sqlite3.connect('bmi_calculator.db')
    c = conn.cursor()
    c.execute('SELECT rowid, bmi FROM bmi_data')
    data = c.fetchall()
    conn.close()
    if data:
        ids, bmi_values = zip(*data)
        plt.plot(ids, bmi_values, marker='o', color='#007bff')
        plt.xlabel('Entry', fontsize=12, color='#333')
        plt.ylabel('BMI', fontsize=12, color='#333')
        plt.title('BMI Over Time', fontsize=14, color='#007bff')
        plt.grid(True)
        plt.show()


def calculate_bmi():
    try:
        weight = float(weight_input.text())
        height = float(height_input.text())
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be greater than zero.")
        bmi = weight / (height ** 2)
        bmi_result_label.setText(f"Your BMI is: {bmi:.2f}")
        category_result_label.setText(bmi_category(bmi))
        save_data(weight, height, bmi)
    except ValueError as e:
        QMessageBox.critical(window, "Input Error", str(e))


def bmi_category(bmi):
    if bmi < 18.5:
        return "You are Underweight"
    elif 18.5 <= bmi < 24.9:
        return "You are Normal"
    elif 25 <= bmi < 29.9:
        return "You are Overweight"
    elif bmi >= 30:
        return "You are Obese"


def plot_button_clicked():
    plot_data()


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("BMI Calculator")
window.setFixedWidth(600)
window.setFixedHeight(400)
window.setWindowIcon(QIcon('icon.png'))

window.setStyleSheet("""
    QWidget {
        background-color: #f0f4f8;
    }
    QLabel {
        font-size: 14pt;
        color: #333;
        padding: 5px;
    }
    QLineEdit {
        font-size: 10pt;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #fff;
    }
    QPushButton {
        font-size: 12pt;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #007bff;
        color: white;
    }
    QPushButton:hover {
        background-color: #0056b3;
    }
    QPushButton:pressed {
        background-color: #004494;
    }
    QWidget#titleBanner {
        background-color: #007bff;
        color: white;
        padding: 10px;
        font-size: 16pt;
        font-weight: bold;
    }
""")

layout = QVBoxLayout()

title_banner = QLabel("BMI Calculator")
title_banner.setObjectName("titleBanner")
title_banner.setAlignment(Qt.AlignCenter)
layout.addWidget(title_banner)

layout.addWidget(QLabel("Enter your weight in kg:"))
weight_input = QLineEdit()
weight_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
layout.addWidget(weight_input)

layout.addWidget(QLabel("Enter your height in meters:"))
height_input = QLineEdit()
height_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
layout.addWidget(height_input)

calculate_button = QPushButton("Calculate BMI")
calculate_button.clicked.connect(calculate_bmi)
layout.addWidget(calculate_button)

bmi_result_label = QLabel("")
layout.addWidget(bmi_result_label)

category_result_label = QLabel("")
layout.addWidget(category_result_label)

plot_button = QPushButton("Plot BMI Chart")
plot_button.clicked.connect(plot_button_clicked)
layout.addWidget(plot_button)

window.setLayout(layout)
init_db()
window.show()
sys.exit(app.exec_())
