import PyPDF2
# from googletrans import Translator

# 打开 PDF 文件
with open('filename.pdf', 'rb') as file:
    # 创建一个 PdfReader 对象
    pdf_reader = PyPDF2.PdfReader(file)

    # 获取 PDF 文件的页数
    num_pages = len(pdf_reader.pages)

    # 创建一个翻译器对象
    # translator = Translator()

    # 读取每一页的文本内容并进行翻译
    for page_num in range(num_pages):
        # 获取当前页面
        page = pdf_reader.pages[page_num]

        # 提取当前页面的文本内容
        text = page.extract_text()

        # 使用 Google Translate API 进行翻译
        # translated_text = translator.translate(text, dest='en').text

        # 打印当前页面的翻译结果
        print(f'Translated Text for Page {page_num + 1}:')
        print(text)
        print('\n')
