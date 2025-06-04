import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

MAIN_URL = "https://www.geeksforgeeks.org/ai-ml-ds-interview/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
CSV_FILE = "all_interview_qna.csv"

def get_article_links():
    response = requests.get(MAIN_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    # print(soup.select_one("text"))
    links = []
    for a in soup.select(".text"):
        print(type(a))
        
        hrefs = [a['href'] for a in soup.find_all('a', href=True)]
        for href in hrefs :
            if href.startswith("https://www.geeksforgeeks.org") and "interview-questions" in href:
                links.append(href)
        # print(hrefs)
    
    print(f"✅ Found {len(links)} article links.")
    return list(set(links))  # remove duplicates

def scrape_questions_from_article(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    content = soup.select_one(".text")
    if not content:
        return []
    
    qna_list = []
    question = None

    for tag in content.find_all(["h2", "h3", "p"]):
        if tag.name in ["h2", "h3"] and "?" in tag.text:
            question = tag.text.strip()
        elif tag.name == "p" and question:
            answer = tag.text.strip()
            qna_list.append({"Question": question, "Answer": answer, "Source": url})
            question = None
    
    return qna_list

def scrape_all_articles():
    all_qna = []
    links = get_article_links()

    for i, link in enumerate(links):
        print(f"🔍 Scraping {i+1}/{len(links)}: {link}")
        try:
            qna = scrape_questions_from_article(link)
            all_qna.extend(qna)
            time.sleep(1)  # be polite
        except Exception as e:
            print(f"❌ Error in {link}: {e}")

        # Update CSV continuously
        pd.DataFrame(all_qna).to_csv(CSV_FILE, index=False)
    
    print(f"✅ Finished scraping. Total Q&A pairs: {len(all_qna)}")

if __name__ == "__main__":
    scrape_all_articles()
