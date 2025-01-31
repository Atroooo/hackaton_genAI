import time
import boto3
import pandas as pd


# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",

)

model_ids = [
    "mistral.mistral-large-2407-v1:0",
    "us.amazon.nova-pro-v1:0",
]


def generate_conversation(model_id, system_prompts, messages, temperature=0.2, max_tokens=50):
    """
    Sends messages to a model.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_prompts (JSON) : The system prompts for the model to use.
        messages (JSON) : The messages to send to the model.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    # Base inference parameters to use.
    inference_config = {"temperature": temperature}
    # Additional inference parameters to use.
    additional_model_fields = {"max_tokens": max_tokens}

    # Send the message.
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
    )

    # Log token usage.
    token_usage = response["usage"]
    print(f"Input tokens: {token_usage['inputTokens']}")
    print(f"Output tokens: {token_usage['outputTokens']}")
    print(f"Total tokens: {token_usage['totalTokens']}")
    print(f"Stop reason: {response['stopReason']}")

    text_response = response["output"]["message"]["content"][0]["text"]

    return text_response


def sentiment_analysis(text):
    """
    Function to return a JSON object of sentiment from a given text.
    """
    system_prompts = [
                {"text": "You are an app that performs sentiment analysis on articles. Those articles will be in french and you'll also have to answer in french. \
                    You will have to use only 5 labels to classify them : \
                        Positif, Négatif, Factuel, Factuel positif, Factuel négatif. \
                    You will also have to give a categorise those articles into one of those categories : \
                        Divers, Mobilité électrique, Réseau, Aléas Climatiques, Clients, Divers, Grèves, Innovation, Linky, Marque employeur / RH, Partenariats industriels / académiques, Prévention, Raccordement, Transition écologique. \
                    No need to justify your answer, just give the sentiment and the category."}
    ]
    message = [{
        "role": "user",
        "content": [{"text": f"Analyze the sentiment of the following text: {text}."}]
    }]
    result = generate_conversation(model_ids[0], system_prompts, message)
    return result


def organise_text(text):
    """Function to organise text into a more readable format.

    Args:
        text (str): text to be organised.
    """
    system_prompts = [
                {"text": "You are an app that organises text. You will have to organise the text into a more readable format. \
                    The text will be in french and you'll also have to return it in french. Precise if the text is a title, a subtitle, a paragraph or a list."}]
    message = [{
        "role": "user",
        "content": [{"text": f"Organise the following text: {text}."}]
    }]
    result = generate_conversation(model_ids[0], system_prompts, message, temperature=0.1, max_tokens=10000)
    return result


if __name__ == "__main__":
    df = pd.read_excel('Data.xlsx')
    text = organise_text(df['Articles'][0])
    time.sleep(0.5)
    print(f"\nOrganised Text:\n{text}")
    print("\n=== Sentiment Analysis Example ===")
    sentiment_analysis_json = sentiment_analysis(text)
    print(f"\nSentiment_Analysis JSON:\n{sentiment_analysis_json}")
