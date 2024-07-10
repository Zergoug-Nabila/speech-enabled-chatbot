import streamlit as st
import speech_recognition as sr
from nltk.chat.util import Chat, reflections

def load_data(file_path):
    pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "::" in line:
                pattern, response = line.split("::", 1)  # Split into two parts only
                pairs.append((pattern.strip(), [response.strip()]))  # Strip whitespace from pattern and response
            elif line:  # Skip empty lines
                st.warning(f"Ignoring line due to incorrect format: {line}")
    return pairs



# Load and preprocess the data
pairs = load_data('chatbot_data.txt')
chatbot = Chat(pairs, reflections)

def transcribe_speech(api, language):
    # Initialize recognizer class
    r = sr.Recognizer()
    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("Speak now...")
        # listen for speech and store in audio_text variable
        audio_text = r.listen(source)
        st.info("Transcribing...")

        try:
            # Using selected Speech Recognition API
            if api == "Google":
                text = r.recognize_google(audio_text, language=language)
            elif api == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language)
            else:
                text = "Unsupported API"
            return text
        except sr.RequestError:
            return "API unavailable or unresponsive"
        except sr.UnknownValueError:
            return "Sorry, I did not get that. Please try again."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

def get_bot_response(user_input):
    if user_input.strip() != "":
        response = chatbot.respond(user_input)
        return response
    else:
        return "Sorry, I didn't get that."

def main():
    st.title("Speech-Enabled Chatbot")
    
    st.write("Choose the Speech Recognition API:")
    api = st.selectbox("API", ["Google", "Sphinx"])

    st.write("Choose the language:")
    language = st.selectbox("Language", ["en-US", "fr-FR"])

    st.write("You can interact with the chatbot using text or speech.")
    
    # Text input
    user_input = st.text_input("Type your message:")
    
    if st.button("Send"):
        if user_input:
            response = get_bot_response(user_input)
            st.write(f"Chatbot: {response}")
    
    st.write("Or, you can use speech input:")

    # Initialize session state to hold the transcription text
    if 'text' not in st.session_state:
        st.session_state.text = ""

    # Add a button to trigger speech recognition
    if st.button("Start Recording"):
        st.session_state.text = transcribe_speech(api, language)
        st.write("Transcription: ", st.session_state.text)
        if st.session_state.text and st.session_state.text != "Unsupported API" and "API unavailable or unresponsive" not in st.session_state.text:
            response = get_bot_response(st.session_state.text)
            st.write(f"Chatbot: {response}")

    # Display transcription and save button only if there's text
    if st.session_state.text:
        if st.button("Save Transcription"):
            with open("transcription.txt", "w") as f:
                f.write(st.session_state.text)
            st.success("Transcription saved to transcription.txt")

if __name__ == "__main__":
    main()
