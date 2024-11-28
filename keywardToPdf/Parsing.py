import pandas as pd
import requests
import os 
from urllib.parse import urlparse, unquote
from metapub import PubMedFetcher
import requests
from bs4 import BeautifulSoup

# 주의 사항 1초의 최대 3회 api 키 없을 경우 



class Parsing:
    
    def __init__(self, keyword, num_of_articles=10):
        self.keyword = keyword
        self.num_of_articles = num_of_articles
        self.pmids = []
        self.fetch = PubMedFetcher()
        self.fileDown = False
    def search_metapub(self):

        articles = {}
        try:

            pmids = self.fetch.pmids_for_query(self.keyword, retmax=self.num_of_articles)
            for pmid in pmids:
                articles[pmid] = self.fetch.article_by_pmid(pmid)

        except Exception as e:
            print(f"Error in search_metapub: {str(e)}")
            return {}

        return articles

    def get_articles_info(self):
        articles = self.search_metapub()
        articles_info = []

        for pmid, article in articles.items():
            try:
                article_info = {
                    'pmid': pmid,
                    'title': article.title,
                    'abstract': article.abstract,
                    'journal': article.journal,
                    'authors': article.authors,
                    'doi': article.doi,
                    'url': article.url,
                    'keywords': article.keywords
                }
                articles_info.append(article_info)
            except Exception as e:
                print(f"Error processing article {pmid}: {str(e)}")
                continue
        
        

        # df = pd.DataFrame(articles_info)
        # print(df)

        return articles_info
    
    def parse_url(self,url, pmid):
        try:
            response = requests.get(url+"/", stream=True,headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # HTTP 에러 체크
            html = response.text
            # BeautifulSoup 객체 생성
            soup = BeautifulSoup(html, 'html.parser')

            # 특정 태그에서 데이터 추출
            title = soup.title.text
            print("웹 페이지 제목:", title)
            pdf_url = soup.select_one('#full-view-identifiers > li:nth-child(2) > span > a')
            print(pdf_url.text)

            if 'pmc' in pdf_url.text.lower():
                response = requests.get(pdf_url.get('href'),headers={"User-Agent": "Mozilla/5.0"})
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                # 특정 태그에서 데이터 추출
                title = soup.title.text
                
                pdf_url1 = soup.select_one('#article-container > div.pmc-sidenav.desktop\:grid-col-4.display-flex > section > div > section > ul > li:nth-child(2) > a').get('href')

                # print(pdf_download_url)

                # print(pdf_url1)
                pdf_download_url = pdf_url.get('href')+pdf_url1
                self.download_pdf(pdf_download_url, pmid+".pdf")
        except Exception as e:
            print(f"Error in parse_url: {str(e)}")
            raise

  
    def download_pdf(self, url, pmid, save_path=None):
        """
        URL에서 PDF 파일을 다운로드하는 함수
        
        Parameters:
        url (str): PDF 파일의 URL
        save_path (str): 저장할 경로와 파일명 (None일 경우 URL의 파일명 사용)
        
        Returns:
        str: 저장된 파일의 경로
        """
        try:
            # URL 유효성 검사
            if not url.startswith(('http://', 'https://')):
                raise ValueError("올바른 URL 형식이 아닙니다.")

            # PDF 파일 다운로드
            response = requests.get(url, stream=True,headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # HTTP 에러 체크

            # Content-Type 확인
            content_type = response.headers.get('Content-Type', '')
            if 'application/pdf' not in content_type.lower():
                print("경고: 다운로드하는 파일이 PDF가 아닐 수 있습니다.")

            # 저장 경로 설정
            if save_path is None:
                # URL에서 파일명 추출
                url_path = urlparse(url).path
                # filename = unquote(os.path.basename(url_path))
                filename = pmid
                print(pmid)
                if not filename.lower().endswith('.pdf'):
                    filename += '.pdf'
                save_path = "./pdfFile/"+filename

            # 파일 저장
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

            print(f"파일이 성공적으로 다운로드되었습니다: {save_path}")
            self.fileDown = True
            return save_path

        except requests.exceptions.RequestException as e:
            print(f"다운로드 중 오류 발생: {e}")
            raise
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
            raise


    def download_pdfs(self):
        articles_info = self.get_articles_info()
        for article in articles_info:
            # print(article['url'])
            if self.fileDown == False:
                self.parse_url(article['url'], article['pmid'])
