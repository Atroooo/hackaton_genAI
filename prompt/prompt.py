import boto3
import os
from dotenv import load_dotenv


load_dotenv()

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

model_ids = [
    "mistral.mistral-large-2407-v1:0",
    "us.amazon.nova-pro-v1:0",
    "us.amazon.nova-lite-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
]


def generate_conversation(model_id, system_prompts, messages,
                          temperature=0.2, max_tokens=50):
    """
    Sends messages to a model.

    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        system_prompts (JSON) : The system prompts for the model to use.
        messages (JSON) : The messages to send to the model.
        temperature (float): The temperature to use for the model.
            Default is 0.2.
        max_tokens (int): The maximum number of tokens to generate.
            Default is 50.

    Returns:
        response (JSON): The conversation that the model generated.

    """

    inference_config = {"temperature": temperature}
    additional_model_fields = {"max_tokens": max_tokens}

    # Send the message.
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        inferenceConfig=inference_config,
        # additionalModelRequestFields=additional_model_fields,
    )

    token_usage = response["usage"]
    print(f"Input tokens: {token_usage['inputTokens']}")
    print(f"Output tokens: {token_usage['outputTokens']}")
    print(f"Total tokens: {token_usage['totalTokens']}")

    text_response = response["output"]["message"]["content"][0]["text"]

    return text_response


# voir pour utiliser guardrails (step 6 le plus interessant pour nous)
def sentiment_analysis(prompt, text):
    """
    Function to return a JSON object of sentiment from a given text.

    Args:
        text (str): text to be analysed
        prompt (str): prompt to be used

    """
    system_prompts = [{"text": str(prompt)}]
    message = [{
        "role": "user",
        "content": [{"text": f"Analyze the sentiment of the following text: \
            {text}."}]
    }]
    result = generate_conversation(model_ids[1], system_prompts, message)
    return result


def organise_text(prompt, text):
    """
    Function to organise text into a more readable format.

    Args:
        text (str): text to be organised.
        prompt (str): prompt to be used
    """
    system_prompts = [{"text": str(prompt)}]
    message = [{
        "role": "user",
        "content": [{"text": f"Organise the following text: {text}."}]
    }]
    result = generate_conversation(model_ids[2], system_prompts, message,
                                   temperature=0.1, max_tokens=10000)
    return result


def get_info_from_pdf(prompt, text):
    """
    Function to get the informations from a pdf.

    Args:
        text (str): text from a pdf page.
        prompt (str): prompt to be used
    """
    system_prompts = [{"text": str(prompt)}]
    message = [{
        "role": "user",
        "content": [{"text": f"Get the informations from the following text: \
            {text}."}]
    }]
    result = generate_conversation(model_ids[2], system_prompts, message,
                                   temperature=0.2, max_tokens=10000)
    return result
