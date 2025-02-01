import ast
import pandas as pd
from PyPDF2 import PdfReader
from prompt import get_text_from_pdf, sentiment_analysis


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


if __name__ == "__main__":
    pdf = PdfReader('articles.pdf')
    articles = pd.DataFrame(columns=['Date', 'Territoire', 'Sujet',
                                     'Catégorie', 'Sentiment',
                                     'Média', 'Article'])
    found = 0
    index = 0
    prompt_sentiment, prompt_read_pdf = get_prompt()

    for i in range(2, len(pdf.pages)):

        page = pdf.pages[i]
        text = page.extract_text()
        if found:
            article_info = get_text_from_pdf(prompt_read_pdf, text)
            try:
                article_info = ast.literal_eval(article_info)
            except ValueError:
                print(f"Error when converting to dict: {article_info}")
                articles.to_excel('results.xlsx')
                exit()

            result = sentiment_analysis(prompt_sentiment,
                                        article_info['Article'])
            # print(f"Result:{result}\n")
            try:
                splitted_result = result.split(',')
                sentiment, category = splitted_result[0], splitted_result[1]
            except ValueError:
                print(f"Error when splitting result: {result}")
                articles.to_excel('results.xlsx')
                exit()

            article_info['Sentiment'] = sentiment
            article_info['Catégorie'] = category
            articles = pd.concat([articles, pd.DataFrame([article_info])],
                                 ignore_index=True)
            index += 1

        if "DR " in text and found == 0:
            # Loop while we don't find the first article
            found = 1
    articles.to_excel('results.xlsx')
