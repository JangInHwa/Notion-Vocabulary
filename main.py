from notion.block import Children, CollectionViewPageBlock
from notion.client import NotionClient
import json
from quizlet import Word, getQuizletWordList


def get_schema_todo():
	return {
		# title 항상 존재 해야한다
		"title": {"name": "영단어ㅤ", "type": "title"},
		"mean1": {"name": "뜻ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", "type": "text"},
		"eng2": {"name": "영단어ㅤㅤ", "type": "text"},
		"mean2": {"name": "뜻ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ", "type": "text"},
	}


if __name__ == '__main__':
	quizlet_url = input('Enter Quizlet url : ')
	words: list[Word] = getQuizletWordList(quizlet_url)
	with open("notion-config.json", "r") as f:
		notion_config_json = f.read()
	notion_config = json.loads(notion_config_json)

	notion_token_v2 = notion_config['token_v2']
	notion_page_url = notion_config['page_url']

	# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
	client = NotionClient(token_v2=notion_token_v2)

	# Replace this URL with the URL of the page you want to edit
	page = client.get_block(
		notion_page_url)
	meaning_collection = page.children.add_new(CollectionViewPageBlock)
	meaning_collection.collection = client.get_collection(
		client.create_record(
			"collection", parent=meaning_collection, schema=get_schema_todo())
	)
	meaning_collection.title = '생성한 테이블'
	meaning_collection.views.add_new(view_type="table")

	for index in range(0, len(words), 2):
		row = meaning_collection.collection.add_row()
		row.title = words[index].eng
		row.set_property('mean1', words[index].meaning)
		print('add word on notion (' + str(index+1) + ' of ' + str(len(words)) + ')')
		if index + 1 >= len(words):
			break
		row.set_property('eng2', words[index+1].eng)
		row.set_property('mean2', words[index+1].meaning)
		print('add word on notion (' + str(index+2) + ' of ' + str(len(words)) + ')')

	# hidden_meaning_collection = page.children.add_new(CollectionViewPageBlock)
	# hidden_meaning_collection.collection = client.get_collection(
	# 	client.create_record(
	# 		"collection", parent=meaning_collection, schema=get_schema_todo())
	# )
	# hidden_meaning_collection.title = '생성한 테이블' + '(hidden meaning)'
	# hidden_meaning_collection.views.add_new(view_type="table")
	# for index in range(0, len(words), 2):
	# 	row = hidden_meaning_collection.collection.add_row()
	# 	row.title = words[index].eng
	# 	print('add word on notion (' + str(index+1) + ' of ' + str(len(words)) + ')')
	# 	if index + 1 >= len(words):
	# 		break
	# 	row.set_property('eng2', words[index+1].eng)
	# 	print('add word on notion (' + str(index+2) + ' of ' + str(len(words)) + ')')
