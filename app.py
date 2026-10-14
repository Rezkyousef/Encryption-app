import streamlit as st
import hashlib
import random
import time

# --- Block 1: Setup and Session State ---
st.set_page_config(page_title="Security Tools App", layout="wide")

# Initialize session state variables
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'target_key' not in st.session_state:
    st.session_state.target_key = random.randint(1, 26)

# --- Block 2: Sidebar Navigation ---
st.sidebar.title("Navigation")
task = st.sidebar.selectbox("Select a Task", ["Task 1: Hashing", "Task 2: Caesar Cipher", "Task 2: Test Yourself"])

# --- Block 3: Task 1 - Hashing ---
if task == "Task 1: Hashing":
    st.header("Task 1: Hashing Algorithm")
    st.write("Convert your plaintext into a fixed-length hash.")
    
    plaintext = st.text_input("Enter text to hash:")
    
    if st.button("Generate Hash"):
        if plaintext:
            # Immediate visual process animation
            with st.spinner("Processing plaintext to ciphertext..."):
                time.sleep(1.5) # Simulate processing time
                ciphertext = hashlib.sha256(plaintext.encode()).hexdigest()
            
            st.success("Process Completed.")
            st.write("Ciphertext Output (SHA-256):")
            st.code(ciphertext)
        else:
            st.warning("Please enter some text first.")

# --- Block 4: Task 2 - Caesar Cipher (Hardcoded Key) ---
elif task == "Task 2: Caesar Cipher":
    st.header("Task 2: Shift Cipher")
    st.write("Encrypt your text using a hidden fixed key.")
    
    # Hardcoded key, hidden from the user
    SECRET_KEY = 3 
    
    plaintext = st.text_input("Enter plaintext:")
    
    if st.button("Encrypt Text"):
        if plaintext:
            with st.spinner("Applying shift cipher process..."):
                time.sleep(1.5)
                ciphertext = ""
                for char in plaintext:
                    if char.isalpha():
                        # Determine if the character is uppercase or lowercase
                        shift = 65 if char.isupper() else 97
                        # Shift character and wrap around the alphabet
                        ciphertext += chr((ord(char) - shift + SECRET_KEY) % 26 + shift)
                    else:
                        ciphertext += char
            
            st.success("Process Completed.")
            st.write("Ciphertext Output:")
            st.code(ciphertext)
        else:
            st.warning("Please enter some text first.")

# --- Block 5: Task 2 - Test Yourself Game ---
elif task == "Task 2: Test Yourself":
    st.header("Test Yourself: Guess the Key")
    st.write("I will encrypt your text with a random key between 1 and 26. Try to guess it.")
    
    # Display Current Score
    st.subheader(f"Current Score: {st.session_state.score}")
    
    test_plaintext = st.text_input("Enter plaintext for the test:")
    
    if st.button("Generate Test Ciphertext"):
        if test_plaintext:
            with st.spinner("Encrypting with a random key..."):
                time.sleep(1)
                test_ciphertext = ""
                for char in test_plaintext:
                    if char.isalpha():
                        shift = 65 if char.isupper() else 97
                        test_ciphertext += chr((ord(char) - shift + st.session_state.target_key) % 26 + shift)
                    else:
                        test_ciphertext += char
            
            # Save the ciphertext to session state to display it alongside the guessing input
            st.session_state.current_ciphertext = test_ciphertext
        else:
            st.warning("Please enter some text first.")
            
    # Show ciphertext and input for guessing if ciphertext exists
    if 'current_ciphertext' in st.session_state:
        st.write("Ciphertext Output:")
        st.code(st.session_state.current_ciphertext)
        
        user_guess = st.number_input("Guess the key (1-26):", min_value=1, max_value=26, step=1)
        
        if st.button("Submit Guess"):
            if user_guess == st.session_state.target_key:
                st.success("Correct. You earned a point.")
                st.session_state.score += 1
                # Generate a new key for the next round
                st.session_state.target_key = random.randint(1, 26)
                # Remove the current ciphertext to force a new round
                del st.session_state.current_ciphertext
            else:
                st.error("Incorrect. You lost a point. Try again.")
                st.session_state.score -= 1
