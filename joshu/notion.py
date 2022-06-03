import os

import requests

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_URL = os.environ["NOTION_URL"]


def add_thought_to_inbox(thought_text):
    thought_text = thought_text.replace("/t", "").strip()
    header = {"Authorization": f"Bearer {NOTION_TOKEN}",
              "Content-Type": "application/json",
              "Notion-Version": "2022-02-22"}
    
    inbox_db_id = os.environ["NOTION_INBOX_DB_ID"]

    body = {
                "parent":{
                    "type": "database_id",
                    "database_id": inbox_db_id
                },
                "properties": {
                    "Thought": {
                        "type": "title",
                        "title": [{
                            "type": "text",
                            "text": {"content": thought_text}
                        }]
                    }
                }
            }
    response = requests.post(url=NOTION_URL,
                             headers=header,
                             data=body)
    
    if response.status_code == 200:
        return "OK"
    else:
        return "ERROR"
