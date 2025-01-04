import re
import random
import json
import long_responses as long

# Load responses from JSON file
try:
    with open('responses.json') as file:
        responses = json.load(file)
except FileNotFoundError:
    print("Warning: responses.json not found. Default responses will be used.")
    responses = {}

# Stop words list
stop_words = ['the', 'is', 'in', 'at', 'to', 'and', 'a', 'of', 'for', 'on', 'with', 'it']

# Function to tokenize and remove stop words
def preprocess_message(message):
    tokens = re.split(r'\s+|[,;?!.-]\s*', message.lower())  # Tokenization
    filtered_tokens = [word for word in tokens if word not in stop_words]  # Stop word removal
    return filtered_tokens

# Function to identify topic
def identify_topic(filtered_tokens):
    if any(word in filtered_tokens for word in ['hello', 'hi', 'hey']):
        return "greetings"
    elif any(word in filtered_tokens for word in ['who', 'you', 'introduce']):
        return "introduction"
    elif any(word in filtered_tokens for word in ['bye', 'goodbye', 'see']):
        return "farewell"
    elif any(word in filtered_tokens for word in ['help', 'assist']):
        return "help"
    elif any(word in filtered_tokens for word in ['weather', 'rain', 'sunny']):
        return "weather"
    elif any(word in filtered_tokens for word in ['hobby', 'hobbies', 'interest']):
        return "hobbies"
    elif any(word in filtered_tokens for word in ['thanks', 'thank', 'appreciate']):
        return "gratitude"
    elif any(word in filtered_tokens for word in ['chat', 'talk', 'conversation']):
        return "smalltalk"
    else:
        return None

# Message probability for keyword matching
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Count matches
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculate match percentage
    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    # Check required words
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Check all messages
def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Add predefined responses
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye', 'bye bye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Add long responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

# Get chatbot response
def get_response(user_input, lang="en"):
    filtered_tokens = preprocess_message(user_input)
    topic = identify_topic(filtered_tokens)

    if topic and responses:
        return responses.get(topic, {}).get(lang, ["I'm not sure what you mean. Can you rephrase that?"])[0]
    else:
        split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
        return check_all_messages(split_message)

# Main loop
if __name__ == "__main__":
    print("AI Chatbot is running... Type 'exit' to stop.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        # Ask for language preference
        lang = input("Translate to Bahasa Indonesia? (yes/no): ").lower()
        if lang == "yes":
            print(f"Chatbot: {get_response(user_input, 'id')}")
        else:
            print(f"Chatbot: {get_response(user_input, 'en')}")
