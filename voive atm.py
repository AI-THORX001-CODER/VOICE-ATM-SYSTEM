import speech_recognition as sr
import datetime
import random
import asyncio
import edge_tts
import playsound
import os
import time

# 🏦 Account Data
balance = 5000
pin = "1234"
transactions = []

# 🎙️ JARVIS VOICE SYSTEM
async def speak_async(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-GuyNeural",   # Deep AI voice
        rate="+50%",               # Slow speaking
        pitch="-8Hz"               # Deep tone
    )
    await communicate.save("voice.mp3")
    playsound.playsound("voice.mp3")
    os.remove("voice.mp3")

def speak(text):
    print("🤖 JARVIS:", text)

    # Thinking pause
    time.sleep(0.2)

    # Split sentences for natural speaking
    sentences = text.split(".")
    
    for sentence in sentences:
        if sentence.strip() != "":
            asyncio.run(speak_async(sentence.strip()))
            time.sleep(0.2)

# 🤖 JARVIS AI RESPONSES
def ai_reply(command, amount=None, balance=None):

    if "balance" in command:
        responses = [
            f"I have accessed your account. Your current balance is {balance} rupees.",
            f"Sir, you currently have {balance} rupees available.",
            f"Your account balance stands at {balance} rupees."
        ]
        return random.choice(responses)

    elif "deposit" in command:
        return f"Deposit successful. {amount} rupees has been added to your account."

    elif "withdraw" in command:
        return f"Withdrawal complete. Please collect {amount} rupees. Remaining balance is {balance} rupees."

    elif "history" in command:
        return "Displaying your recent transactions now."

    elif "exit" in command:
        return "THANK YOU FOR USING ATM."

    else:
        return "I did not understand that command. Please repeat."

# 🎤 VOICE INPUT
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            command = r.recognize_google(audio).lower()
            print("✅ You said:", command)
            return command
    except:
        return input("⌨️ Type command: ").lower()

# 🔐 LOGIN SYSTEM
def login():
    attempts = 3
    while attempts > 0:
        user_pin = input("Enter YOUR ATM PIN: ")
        if user_pin == pin:
            speak("Authentication successful. Welcome back, sir.")
            return True
        else:
            attempts -= 1
            speak(f"Incorrect PIN. Attempts remaining {attempts}")
    speak("Access denied. Account has been locked.")
    return False

# 🏦 ATM FUNCTIONS
def check_balance():
    speak(ai_reply("balance", balance=balance))

def deposit():
    global balance
    try:
        amount = int(input("Enter amount: "))
        if amount <= 0:
            speak("Invalid amount entered.")
            return
        balance += amount
        transactions.append(f"{datetime.datetime.now()} - Deposited {amount}")
        speak(ai_reply("deposit", amount=amount))
    except:
        speak("Invalid input detected.")

def withdraw():
    global balance
    try:
        amount = int(input("Enter amount: "))
        if amount <= 0:
            speak("Invalid amount entered.")
            return
        if amount <= balance:
            balance -= amount
            transactions.append(f"{datetime.datetime.now()} - Withdrew {amount}")
            speak(ai_reply("withdraw", amount=amount, balance=balance))
        else:
            speak("Insufficient balance.")
    except:
        speak("Invalid input detected.")

def show_transactions():
    if not transactions:
        speak("There are no transactions to display.")
    else:
        speak(ai_reply("history"))
        for t in transactions:
            print(t)

# 🤖 MAIN SYSTEM
if login():
    speak("Welcome to SBI BANKING.")

    while True:
        speak("Please state your command: balance, deposit, withdraw, history, or exit.")
        command = listen()

        if command == "":
            continue

        if "balance" in command:
            check_balance()

        elif "deposit" in command:
            deposit()

        elif "withdraw" in command:
            withdraw()

        elif "history" in command:
            show_transactions()

        elif "exit" in command:
            speak(ai_reply("exit"))
            break

        else:
            speak(ai_reply(command))