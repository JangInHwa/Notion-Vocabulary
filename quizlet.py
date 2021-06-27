from urllib import parse
import requests
from bs4 import BeautifulSoup

class Word:
	def __init__(self, eng, meaning):
		self.eng = eng
		self.meaning = meaning

def getQuizletWordList(quizlet_url:str) -> list[Word]:
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

	response = requests.get(quizlet_url, headers=headers)
	if response.status_code == 200:
		html = response.text
		soup = BeautifulSoup(html, 'html.parser')
		word_selected_results = soup.select('.notranslate')
		words:list[Word] = []
		for index in range(0, len(word_selected_results), 2):
			words.append(Word(word_selected_results[index].text, word_selected_results[index+1].text))
		return words
	else:
		return []

