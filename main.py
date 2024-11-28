from keywardToPdf.parsing import Parsing
from keywardToPdf.translator import translate_text
from keywardToPdf.gemini_api import GeminiWrapper
import argparse, sys


def main(keywords):
    try:
        # 단일 키워드 검색
        # parser = Parsing("cancer", num_of_articles=3)
        # articles_info = parser.get_articles_info()
        
        # 여러 키워드로 검색하는 경우"
        parser_multiple = Parsing(keywords, num_of_articles=50)
        articles_info_multiple = parser_multiple.get_articles_info()


        parser_multiple.download_pdfs()

        

    except Exception as e:
        print(f"Error in main: {str(e)}")

def keyword_extraction(text):
        try:
            # Initialize the wrapper
            gemini = GeminiWrapper()
            
            # Example prompt
            prompt = text

            print(text)
            
            # Generate and print response
            response = gemini.extract_medical_keyword(prompt)
            print(f"Response: {response}")
            return response
        except Exception as e:
            print(f"Error: {str(e)}")
    




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-text', help=' : Please set the keyword you want to search', type=str) 
    keyword_extra = keyword_extraction(parser.parse_args().text)
    print(keyword_extra)
    keyword = translate_text(keyword_extra)
    print(keyword)
    main(keywords=keyword)