# -*- coding: utf-8 -*-
# pip3 install markdown
# pip3 install pdfkit

import codecs
import markdown
import pdfkit

with codecs.open("test.md", "r", encoding="utf-8") as f:
    md_content = f.read()

html_content = markdown.markdown(md_content)
with codecs.open("test.html", "w", encoding="utf-8") as f:
    # 加入文件头防止中文乱码
    f.write('<meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>')
    f.write(html_content)

pdfkit.from_file("test.html", "test.pdf")
