import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    # Define the character sets
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected.")
    
    # Generate the password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    # Get user input for password length
    while True:
        try:
            length = int(input("Enter the desired password length: "))
            if length <= 0:
                raise ValueError("Password length must be a positive integer.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

    # Get user preferences for character types
    use_letters = input("Include letters (y/n)? ").strip().lower() == 'y'
    use_numbers = input("Include numbers (y/n)? ").strip().lower() == 'y'
    use_symbols = input("Include symbols (y/n)? ").strip().lower() == 'y'

    try:
        # Generate and display the password
        password = generate_password(length, use_letters, use_numbers, use_symbols)
        print(f'Generated Password: {password}')
    except ValueError as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()