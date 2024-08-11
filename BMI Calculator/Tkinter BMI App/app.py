import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

def calculate_bmi():
    try:
        weight = float(weight_input.text())
        height = float(height_input.text())
        if height <= 0:
            raise ValueError("Height must be greater than zero.")
        bmi = weight / (height ** 2)
        bmi_result_label.setText(f"Your BMI is: {bmi:.2f}")
        category_result_label.setText(bmi_category(bmi))
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

# Create the main window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("BMI Calculator")
window.setFixedWidth(500)
window.setFixedHeight(300)
# Create and place the widgets
layout = QVBoxLayout()

layout.addWidget(QLabel("Enter your weight in kg:"))
weight_input = QLineEdit()
layout.addWidget(weight_input)

layout.addWidget(QLabel("Enter your height in meters:"))
height_input = QLineEdit()
layout.addWidget(height_input)

calculate_button = QPushButton("Calculate BMI")
calculate_button.clicked.connect(calculate_bmi)
layout.addWidget(calculate_button)

bmi_result_label = QLabel("")
layout.addWidget(bmi_result_label)

category_result_label = QLabel("")
layout.addWidget(category_result_label)

window.setLayout(layout)

# Run the application
window.show()
sys.exit(app.exec_())
