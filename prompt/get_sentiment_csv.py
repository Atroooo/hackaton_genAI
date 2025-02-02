import pandas as pd
from prompt import organise_text, sentiment_analysis
import time


def get_prompt():
    """Obtain the prompt from the prompt files.

    Returns:
        prompt_sentiment (file): prompt for sentiment analysis
        prompt_organise (file): prompt for organising text
    """
    try:
        with open("prompt_sentiment.txt", "r") as file:
            prompt_sentiment = file.read()

        with open("prompt_organize_text.txt", "r") as file:
            prompt_organise = file.read()
    except FileNotFoundError as e:
        print("Error: Prompt file not found:", e)
        exit()

    return prompt_sentiment, prompt_organise


if __name__ == "__main__":
    df = pd.read_excel('Data.xlsx')
    results = pd.DataFrame(columns=['Date', 'Territoire', 'Sujet', 'Catégorie',
                                    'Sentiment', 'Media', 'Articles'])
    prompt_sentiment, prompt_organise = get_prompt()

    for i in range(len(df)):
        if i % 10 == 0:
            print(f"Processing article {i}")
        try:
            text = organise_text(prompt_organise, df['Articles'][i])
            result = sentiment_analysis(prompt_sentiment, text)
            time.sleep(0.5)
            # print(f"Result:{result}\n")
            try:
                splitted_result = result.split(',')
                sentiment, category = splitted_result[0], splitted_result[1]
            except ValueError:
                print(f"Error when splitting result: {result}, saving results...")
                results.to_excel('results_data.xlsx', index=False)
                exit()
            results.loc[i] = [df['Date'][i], df['Territoire'][i], df['Sujet'][i],
                            category, sentiment,  df['Sujet'][i],  text]
        except Exception as e:
            print(f"Error when processing article {i}: {e}")
            continue
    print("\nDone\n")
    results.to_excel('results_data.xlsx', index=False)

# check batch + guardrails