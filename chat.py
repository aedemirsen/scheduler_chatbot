# Import necessary modules
import random
import json
import torch

import constants
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import service


# Initialize and load the chatbot model
def load_chatbot_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    file = "data.pth"
    data = torch.load(file)

    model = NeuralNet(data["input_size"], data["hidden_size"], data["output_size"]).to(device)
    model.load_state_dict(data["model_state"])
    model.eval()

    return model, data, intents, device


# Function to get response from the chatbot
def get_chatbot_response(sentence):
    tokenize_sentence = tokenize(sentence)
    x = bag_of_words(tokenize_sentence, data['all_words'])
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _, predicted = torch.max(output, dim=1)

    tag = data['tags'][predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        print("Success - {}", tag)
        if tag == 'EventTitle':
            # set title
            return service.set_title(sentence)
        elif tag == 'When':
            # ask gpt for necessary data
            return service.ask_gpt_for_necessary_data(sentence)
        elif tag == 'InquireMeetingDetails':
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return str(random.choice(intent['responses']))\
                        .format(service.format_schedule(constants.NECESSARY_SCHEDULING_FORMAT))
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    else:
        print("Fail - {}", tag)
        # ask gpt for help
        # gpt will return tag
        gpt_response = service.ask_gpt_for_tag(sentence)
        print(gpt_response)
        for intent in intents['intents']:
            if gpt_response == intent["tag"]:
                return random.choice(intent['responses'])


# Load the model
model, data, intents, device = load_chatbot_model()
