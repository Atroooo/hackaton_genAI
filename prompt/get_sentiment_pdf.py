import ast
import json
import pandas as pd
from PyPDF2 import PdfReader
from prompt import get_info_from_pdf, sentiment_analysis


def get_prompt():
    """Obtain the prompt from the prompt files.

    Returns:
        prompt_sentiment (file): prompt for sentiment analysis
        prompt_organise (file): prompt for organising text
    """
    try:
        with open("prompt_sentiment.txt", "r") as file:
            prompt_sentiment = file.read()

        with open("prompt_read_pdf.txt", "r") as file:
            prompt_read_pdf = file.read()
    except FileNotFoundError:
        print("Error: Prompt file not found.")
        exit()

    return prompt_sentiment, prompt_read_pdf


def get_all_infos(pdf):
    """
    Function to get all the pages from a pdf file.

    Args:
        pdf (file): pdf file to extract the pages from.
    """
    data = pd.DataFrame(columns=['Date', 'Territoire', 'Sujet', 'Catégorie',
                                 'Sentiment', 'Média', 'Article'])
    article = ""
    found = 0

    for i in range(2, len(pdf.pages)):
        if i % 10 == 0:
            print(f"--- Processing page {i} ---")
        page = pdf.pages[i]
        text = page.extract_text()
        if "Parution : " not in text:
            article += text
        else:
            article += text
            temp = eval(get_info_from_pdf(prompt_read_pdf, article))
            data = pd.concat([data, pd.DataFrame([temp])], ignore_index=True)
            article = ""

        if "DR " in text and found == 0:
            # Loop while we don't find the first article
            found = 1
    return data


if __name__ == "__main__":
    pdf = PdfReader('articles.pdf')
    prompt_sentiment, prompt_read_pdf = get_prompt()

    df_articles = get_all_infos(pdf)

    for i in range(len(df_articles)):
        if i % 10 == 0:
            print(f"--- Processing article {i} ---")
        result = sentiment_analysis(prompt_sentiment,
                                    df_articles['Article'][i])
        try:
            splitted_result = result.split(',')
            sentiment, category = splitted_result[0], splitted_result[1]
        except ValueError:
            print(f"Error when splitting result: {result}, saving results...")
            df_articles.to_excel('results_c.xlsx', index=False)
            exit()
        df_articles.loc[i, 'Sentiment'] = sentiment
        df_articles.loc[i, 'Catégorie'] = category

    df_articles.reindex(columns=['Date', 'Territoire', 'Sujet', 'Catégorie',
                                 'Sentiment', 'Média', 'Article'])
    df_articles.to_excel('results_c.xlsx', index=False)
