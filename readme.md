# Med-Spider⚕

该项目是一个基于Python的GUI（Tkinter）工具，旨在通过让ChatGPT提供的关键词，从PubMed数据库中检索相关文献并提供免费文献的PDF下载。

相比自己给关键词（写正则表达式），ChatGPT更擅长这一任务，你要做的就是给它一个你想要了解的领域🤓！

## 安装

请提前安装``Python>=3.9``  

1. 克隆该项目到本地

```shell
git clone https://github.com/Becomingw/Med-Spider.git
```

2. 安装依赖项

```shell
pip install -r requirements.txt #-i https://pypi.tuna.tsinghua.edu.cn/simple（国内用户可选）
```

3. 运行程序

```shell
cd Med-Spider
python GUI.py
```

## 特性

1. 提供无脑操作的GUI界面🖥；
2. 提供彩云☁接口，使用彩云翻译api将摘要翻译为中文（每个月免费10万字）；
3. ChatGPT🤖代写文献关键词正则表达式；
4. 提供PubMed免费文献直接下载🖨，部分非免费文献下载；

## 使用方法

1. 勾选是否使用彩云Token或者ChatGPT；
2. 如果不使用彩云与GPT则彩云token与GPTkey可以为空，否则必须正确填写‼；
3. 当使用ChatGPT时，关键词可输入例如：肿瘤复发转移的相关研究。【你填写的关键词应该像一篇中文综述的标题】
4. 当未使用ChatGPT时，关键词必须为全英文且为正确的正则表达式‼，错误的输入返回文献为0或极少；
5. 下载的文献信息存在程序根目录下的表格RX.xlsx内，格式为：

| title        | journal          | Date   | doi     | abstract | 摘要                 | PMID | journal_link     | free_link        | download                         |
| ------------ | ---------------- | ------ | ------- | -------- | -------------------- | ---- | ---------------- | ---------------- | -------------------------------- |
| 这是文献标题 | 这是文献期刊全称 | 发表年 | 文献doi | 英文摘要 | 使用彩云时的中文摘要 | PMID | 文献原始期刊地址 | 文献免费获取地址 | 是否下载（1为已下载，0为未下载） |

- 下载PDF功能独立于搜索功能，用户需要手动点击下载文献，并且保证程序根目录下有RX.xlsx文件；
- 注意，如果想多次分批次搜集文献，请注意将RX.xlsx改名后保存，否则将被新的文献替换；
- 上限为理论搜集文献的上限数量，实际与用户搜索关键词有关。（不建议设置过大）

## 使用范例

<img src="fig\5.png" alt="5" style="zoom:50%;" />

<img src="fig\1.png" alt="1" style="zoom:27%;" />

<img src="fig\4.png" alt="4" style="zoom:37%;" />

<img src="fig\3.png" alt="3" style="zoom:50%;" />

## 注意事项

1. 彩云翻译API--[彩云科技开放平台](https://platform.caiyunapp.com/regist)
2. 该程序使用的ChatGPT接口来自于[GPT-API-free](https://github.com/chatanywhere/GPT_API_free),Github用户可获取一个受限免费key；
3. 如想使用其他GPT接口或者官方默认接口，请在``tookit.py``文件下更改：

```python
openai.api_base = 'https://api.openai.com/v1' # 更改api后请使用支持chatGPT的区域网络下使用本程序
```

1. 该程序提供的文献下载功能仅限于部分文献，大部分收费文献需要用户到journal_link跳转获取；
2. 该程序没有内置代理池（proxypool），故建议用户打开代理进行文献搜集，尽量使用非国内IP获取最佳体验☺；（不建议裸奔上阵😋）

### OK, enjoy it🥳!

## 版权信息

本项目遵循[Apache](https://github.com/Becomingw/Med-Spider/edit/main/LICENSE)许可证。

