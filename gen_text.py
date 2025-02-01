import time
import boto3
import pandas as pd


# Setup bedrock
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2"
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
    #additional_model_fields = {"max_tokens": max_tokens}

    # Send the message.
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        #additionalModelRequestFields=additional_model_fields,
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
                {"text": "You are a sentiment analysis expert specializing in the perception of the French company Enedis by the public. \
                    Your task is to analyze French-language articles and categorize them based on both sentiment and topic.  You MUST respond in French. \
                    *Sentiment Analysis:** \
                    Use only 5 labels for sentiment to classify them : \
                        Positif, Négatif, Factuel, Factuel positif, Factuel négatif. \
                    **Topic Categorization:** \
                    Categorize each article into ONE of the following topics : \
                        Divers, Mobilité électrique, Réseau, Aléas Climatiques, Clients, Grèves, Innovation, Linky, Marque employeur / RH, Partenariats industriels / académiques, Prévention, Raccordement, Transition écologique. \
                    **Instructions for Sentiment Analysis:** \
                    Your response MUST be in the following format:  `Sentiment,Category` (e.g., `Négatif,Grèves`).  Do NOT include parentheses or any other text.  Give ONLY the sentiment and category, separated by a comma.  Do NOT provide any explanations or justifications. \
                    **Instructions for Analysis:** \
                        *   Prioritize identifying the *dominant* sentiment expressed in the article.  Even if an article contains mixed sentiments, choose the one that is most prevalent. \
                        *   For 'Factuel' sentiment, determine if the factual information presented has an overall positive or negative implication.  If the factual information is neutral, use 'Factuel'. \
                        *   For topic categorization, select the *most relevant* topic.  If an article covers multiple topics, choose the primary one. \
                        *   Be precise and concise in your responses."}    ]
    message = [{
        "role": "user",
        "content": [{"text": f"Analyze the sentiment of the following text: {text}."}]
    }]
    result = generate_conversation(model_ids[1], system_prompts, message)
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
    result = generate_conversation(model_ids[1], system_prompts, message, temperature=0.3)#, max_tokens=10000)
    return result


if __name__ == "__main__":
    df = pd.read_csv('data/testing.csv')
    results = pd.DataFrame(columns=['Title', 'Sentiment', 'Category', 'Text'])
    for i in range(100, len(df)):
        print("Index: ", i)
        text = organise_text(df['Articles'][i])
        result = sentiment_analysis(text)
        print(f"Result:{result}\n")
        try:
            splitted_result = result.split(',')
            sentiment, category = splitted_result[0], splitted_result[1]
        except ValueError:
            print(f"Error when splitting result: {result}")
            results.to_excel('results3a.xlsx')
            exit()
        results.loc[i] = [df['Sujet'][i], sentiment, category, text]
    print("\nDone\n")
    results.to_excel('results3a.xlsx')