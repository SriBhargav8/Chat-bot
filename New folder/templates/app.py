from flask import Flask, request, render_template
import openai
from translate import Translator


# Set up your OpenAI API credentials
openai.api_key = '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'

def translation(text1,lang):
    
    lang=lang.lower()
    
     # Create a Translator object
    if lang=="telugu":
        translator = Translator(to_lang="te")
    elif lang=="hindi":
        translator = Translator(to_lang="hin")
    elif lang=="tamil":
        translator = Translator(to_lang="ta")
    elif lang=="kannada":
        translator = Translator(to_lang="kn")
    elif lang=="malayalam":
        translator = Translator(to_lang="ml")
    else:
        translator = Translator(to_lang="en")
        

    # Define the text to be translated
    text_to_translate = text1

    # Split the text into smaller chunks
    text_chunks = [text_to_translate[i:i+500] for i in range(0, len(text_to_translate), 500)]

    # Translate each chunk and store the results
    translated_chunks = []
    for chunk in text_chunks:
        translated_chunk = translator.translate(chunk)
        translated_chunks.append(translated_chunk)

    # Join the translated chunks back into a single translated text
    translated_text = ' '.join(translated_chunks)

    # Print the translated text
    return translated_text

# Function to send a message to the chatbot and receive its response
def chat(message):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=4000,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10
    )
    return response.choices[0].text.strip()




def is_government_service(question):
    # Define your prompt for the API call
    prompt = "Is the following question related to a government service? \nQuestion: " + question + "\nAnswer:"

    # Call the OpenAI API to generate the response
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the binary output from the API response
    output = response.choices[0].text.strip()

    # Convert output to binary representation
    if output == 'Yes':
        binary_output = 1
    else:
        binary_output = 0

    return binary_output




app = Flask(__name__)

# Chatbot route
@app.route("/")
def index():
    return render_template("home.html")


@app.route('/process_dropdown', methods=['POST'])
def process_dropdown():
    dropdown_option = request.form.get('dropdown')
    global lang
    lang=dropdown_option
    return render_template('home.html')

@app.route("/get")
def get_bot_response():
    userText=request.args.get("msg")
    matching_question = is_government_service(userText)
    if matching_question:
        bot_response = chat(userText)
        resp=translation(bot_response,lang)
        return resp
    else:
        resp=translation("Jarvis: the service you entered is not a governement service please try again !",lang)
        return resp

if __name__ == '__main__':
    app.run(debug=True)