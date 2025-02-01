import pandas as pd
from prompt import organise_text, sentiment_analysis


def get_prompt():
    """Obtain the prompt from the prompt files.

    Returns:
        prompt_sentiment (file): prompt for sentiment analysis
        prompt_organise (file): prompt for organising text
    """
    try:
        with open("prompt_sentiment.txt", "r") as file:
            prompt_sentiment = file.read()

        with open("prompt_organise.txt", "r") as file:
            prompt_organise = file.read()
    except FileNotFoundError:
        print("Error: Prompt file not found.")
        exit()

    return prompt_sentiment, prompt_organise


if __name__ == "__main__":
    df = pd.read_excel('../data/Data.xlsx')
    results = pd.DataFrame(columns=['Title', 'Sentiment', 'Category', 'Text'])
    prompt_sentiment, prompt_organise = get_prompt()

    for i in range(100):
        if i % 10 == 0:
            print(f"Processing article {i}")
        text = organise_text(prompt_organise, df['Articles'][i])
        result = sentiment_analysis(prompt_sentiment, text)
        # print(f"Result:{result}\n")
        try:
            splitted_result = result.split(',')
            sentiment, category = splitted_result[0], splitted_result[1]
        except ValueError:
            print(f"Error when splitting result: {result}, saving results...")
            results.to_excel('results.xlsx')
            exit()
        results.loc[i] = [df['Sujet'][i], sentiment, category, text]
    print("\nDone\n")
    results.to_excel('results.xlsx')
