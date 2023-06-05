from tkinter import Tk, Label, Entry, Button, BooleanVar, Checkbutton, messagebox
import re
import pandas as pd

from tookit import openai_help
from PDFdownload import Pubmed_download, sci_hub
from pubmedclaw import main
from tkinter import ttk
import threading
import webbrowser


def submit():
    messagebox.showinfo("提示!!!", "请一定确保Excel表格已关闭!")
    page = int(page_entry.get())
    use_cytoken = cytoken_var.get()
    kw = kw_entry.get()
    cytoken = cytoken_entry.get() if use_cytoken else None
    use_gptkey = gptkey_var.get()
    gptkey = gptkey_entry.get() if use_gptkey else None
    # 执行你的操作
    print("上限:", page)
    print("关键词:", kw)
    print("彩云Token:", cytoken)
    print("GPTkey:", gptkey)
    threading.Thread(target=perform_operation, args=(kw, cytoken, page, gptkey)).start()


# 主程序进程
def perform_operation(kw,  cytoken, page, gptkey=None):
    if gptkey:
        kw = openai_help(kw, gptkey)
        print('openai_kw:', kw)
    page = (int(page)//10)+1
    main(page, kw, cytoken)


# 下载程序进程
def download_pdf():
    def download_operation():
        Pubmed_download('RX.xlsx')
        Df = pd.read_excel('RX.xlsx', engine='openpyxl')
        for index, raw in Df.iterrows():
            if raw['download'] == 0:
                Df.at[index, 'download'] = sci_hub(raw['doi'], filename=re.sub(r'[\\/:*?"<>|]', '_', raw['title']))
        try:
            Df.to_excel('Rx.xlsx', engine='openpyxl', index=False)
        except:
            print('请关闭excel文件后重试，本次表格写入失败！')
        print('Download all over!')
    # 在新线程中执行下载操作
    threading.Thread(target=download_operation).start()

# 超连接
def github_link():
    webbrowser.open("https://github.com/Becomingw/Med-Spider/")
def caiyun_link():
    webbrowser.open("https://docs.caiyunapp.com/blog/2018/09/03/lingocloud-api/")

# 设置主题
root = Tk()
root.title("MedSpider")
root.iconbitmap("claw.ico")
window_width = 420
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
style = ttk.Style()
style.configure("TLabel", foreground="black", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12))

# 是否使用彩云token
cytoken_var = BooleanVar()
cytoken_checkbox = Checkbutton(root, text="使用彩云", variable=cytoken_var, font=("SimSun", 10))
cytoken_checkbox.grid(row=0, column=0, pady=10)
# 是否使用GPT
gptkey_var = BooleanVar()
gptkey_checkbox = Checkbutton(root, text="使用GPT", variable=gptkey_var, font=("SimSun", 10))
gptkey_checkbox.grid(row=0, column=1, pady=10)

# 创建标签和输入框用于输入cytoken参数
cytoken_label = Label(root, text="彩云Token:", font=("SimSun", 12))
cytoken_label.grid(row=1, column=0, sticky="e")
cytoken_entry = Entry(root)
cytoken_entry.grid(row=1, column=1, sticky="e")

# 彩云link
link_label = Label(root, text="Token获取方法", fg="red", cursor="hand2", font=("Helvetica", 10))
link_label.grid(row=1, column=2, padx=5)
link_label.bind("<Button-1>", lambda e: caiyun_link())


# 创建标签和输入框用于输入gptkey参数
gptkey_label = Label(root, text="GPT key:", font=("SimSun", 12))
gptkey_label.grid(row=2, column=0, sticky="e")
gptkey_entry = Entry(root)
gptkey_entry.insert(0, 'sk-xxxxxxxxxxxxxxxxxxx')
gptkey_entry.grid(row=2, column=1, sticky="e")

# 创建标签和输入框用于输入page参数
page_label = Label(root, text="下载上限:", font=("SimSun", 12))
page_label.grid(row=3, column=0, sticky="e")
page_entry = Entry(root)
page_entry.insert(0, '10')
page_entry.grid(row=3, column=1, sticky="e")

# 创建标签和输入框用于输入kw参数
kw_label = Label(root, text="输入关键词:", font=("SimSun", 12))
kw_label.grid(row=4, column=0, sticky="e")
kw_entry = Entry(root)
kw_entry.insert(0, '未使用GPT输入需为英文')
kw_entry.grid(row=4, column=1, sticky="e")

# 超链接
label = Label(root, text="访问项目", fg="blue", cursor="hand2")
label.grid(row=2, column=2, padx=5)
# 绑定标签的点击事件到open_link函数
label.bind("<Button-1>", lambda e: github_link())

# 创建按钮用于提交参数
submit_button = Button(root, text="提交", command=submit, font=("SimSun", 12), relief="raised", width=10)
submit_button.grid(row=5, column=1, sticky="w")

download_button = Button(root, text="下载PDF", command=download_pdf, font=("SimSun", 12), relief="raised", width=10)
download_button.grid(row=5, column=2, sticky="e")

root.mainloop()
