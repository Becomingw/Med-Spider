import json

import openai
import requests


#  彩云翻译API
def tranlate(source, direction, token):
    url = "http://api.interpreter.caiyunai.com/v1/translator"

    # WARNING, this token is a test token for new developers,
    # and it should be replaced by your token

    payload = {
        "source": source,
        "trans_type": direction,
        "request_id": "demo",
        "detect": True,
    }

    headers = {
        "content-type": "application/json",
        "x-authorization": "token " + token,
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    return json.loads(response.text)["target"]

def openai_help(key,openkey):
    openai.api_base = 'https://api.chatanywhere.cn/v1'
    openai.api_key = openkey
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "你是一个Pubmed文献搜索词推荐者，当我向你提供一个关键词时，你需要将它转化为Pubmed可用的严格的逻辑搜索词，例如：用户输入：机器学习的不足，你返回：("
                                        "\"machine learning\"AND\"limitation\")OR(\"machine "
                                        "learning\"AND\"deficiency\")。仅返回搜索词，不允许返回任何中文。我的第一个关键词是:"+key}
        ]
    )
    key_word = completion.choices[0].message['content']
    return key_word
