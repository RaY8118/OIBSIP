def calculate_bmi(weight, height):
    if height <= 0:
        return "Height must be greater than zero."
    
    # Calculate BMI
    bmi = weight / (height ** 2)
    return bmi

def bmi_category(bmi):
    if bmi < 18.5:
        return "You are Underweight"
    elif 18.5 <= bmi < 24.9:
        return "You are Normal"
    elif 25 <= bmi < 29.9:
        return "You are Overweight"
    elif bmi >= 30:
        return "You are Obese"
    else:
        return "Enter proper data"

# Example usage
weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in meters: "))

bmi = calculate_bmi(weight, height)
print(f"Your BMI is: {bmi:.2f}")
category = bmi_category(bmi)
print(category)
