from notion.block import Children, CollectionViewPageBlock
from notion.client import NotionClient
import json
from quizlet import Word, getQuizletWordList


def get_schema_todo():
    return {
        # title 항상 존재 해야한다
        "title": {
            "name": "영단어 ",
            "type": "title"
        },
        "mean1": {
            "name": "뜻           ",
            "type": "text"
        },
        "eng2": {
            "name": "영단어 ",
            "type": "text"
        },
        "mean2": {
            "name": "뜻           ",
            "type": "text"
        },
    }


if __name__ == '__main__':
    with open("notion-config.json", "r") as f:
        notion_config_json = f.read()
    notion_config = json.loads(notion_config_json)

    notion_token_v2 = notion_config['token_v2']
    notion_page_url = notion_config['page_url']
    if notion_token_v2 == '':
        notion_token_v2 = input(
            'Enter the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so\ntoken_v2 : '
        )
    if notion_page_url == '':
        notion_page_url = input(
            'Enter your notion page url that you want to make word list at\nurl:'
        )
    with open("notion-config.json", "w") as f:
        f.write(
            json.dumps({
                'token_v2': notion_token_v2,
                'page_url': notion_page_url
            }))
    quizlet_url = input('Enter Quizlet url : ')
    words: list[Word] = getQuizletWordList(quizlet_url)
    notion_page_name = input('Notion Word List Page Name : ')

    client = NotionClient(token_v2=notion_token_v2)

    page = client.get_block(notion_page_url)
    meaning_collection: CollectionViewPageBlock = page.children.add_new(
        CollectionViewPageBlock)
    meaning_collection.collection = client.get_collection(
        client.create_record("collection",
                             parent=meaning_collection,
                             schema=get_schema_todo()))
    meaning_collection.title = notion_page_name
    view = meaning_collection.views.add_new(view_type="table")

    hidden_meaning_collection: CollectionViewPageBlock = page.children.add_new(
        CollectionViewPageBlock)
    hidden_meaning_collection.collection = client.get_collection(
        client.create_record("collection",
                             parent=hidden_meaning_collection,
                             schema=get_schema_todo()))
    hidden_meaning_collection.title = notion_page_name + ' (hidden meaning)'
    hidden_meaning_collection.views.add_new(view_type="table")

    for index in range(0, len(words), 2):
        meaning_row = meaning_collection.collection.add_row()
        meaning_row.title = words[index].eng
        meaning_row.set_property('mean1', words[index].meaning)
        hidden_meaning_row = hidden_meaning_collection.collection.add_row()
        hidden_meaning_row.title = words[index].eng
        print('add word on notion (' + str(index + 1) + ' of ' +
              str(len(words)) + ')')
        if index + 1 >= len(words):
            break
        meaning_row.set_property('eng2', words[index + 1].eng)
        meaning_row.set_property('mean2', words[index + 1].meaning)
        hidden_meaning_row.set_property('eng2', words[index + 1].eng)
        print('add word on notion (' + str(index + 2) + ' of ' +
              str(len(words)) + ')')
