from keywardToPdf.Parsing import Parsing  

def main():
    try:
        # 단일 키워드 검색
        # parser = Parsing("cancer", num_of_articles=3)
        # articles_info = parser.get_articles_info()
        
        # 여러 키워드로 검색하는 경우
        keywords = "behavior; brain; collagenases"
        parser_multiple = Parsing(keywords, num_of_articles=3)
        articles_info_multiple = parser_multiple.get_articles_info()
        # print(len(articles_info_multiple))
        # print(articles_info_multiple[0]['url'])
        # print([i['url'] for i in articles_info_multiple]) 

        parser_multiple.download_pdfs()

        

    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()