from wordcloud import WordCloud
import numpy as np
import jieba
from PIL import Image
def trans(data):
    alice_coloring = np.array(Image.open("A.jpg"))
    wordcloud = WordCloud(background_color="white",mask=alice_coloring,font_path = 'WE.TTF',width=1000, height=860, margin=2).generate(data)
    wordcloud.to_file("qw.jpg")
def main():
    a=[]
    f = open('comment.txt', 'r', encoding="utf-8").read()
    words=list(jieba.cut(f))
    for word in words:
        if len(word)>1:
            a.append(word)
    txt=r' '.join(a)
    trans(txt)
if __name__ == '__main__':
    # main()
    url = "https://static.zhihu.com/heifetz/main.app.bcbe6146eb81b5efaede.js"
    import requests
    r = requests.get(url)
    print(r.text)
    f = open("js.txt","w",encoding="utf-8")
    f.write(r.text)





# width,height,margin可以设置图片属性

# generate 可以对全部文本进行自动分词,但是他对中文支持不好,对中文的分词处理请看我的下一篇文章
#wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)
# 你可以通过font_path参数来设置字体集

#background_color参数为设置背景颜色,默认颜色为黑色
#
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
#
# wordcloud.to_file('test.png')
