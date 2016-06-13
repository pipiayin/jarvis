#encoding=utf-8
import jieba

jieba.set_dictionary('dict.txt.big')

string1 = u'請幫我google一下生涯規劃'
string2 = u'查詢生涯規劃'
string3 = u'找生涯規劃'

strings = [string1,string2,string3]

for s in strings:
    print "Input：",s

    words = jieba.cut(s, cut_all=False)

    print "Output 精確模式 Full Mode："
    for word in words:
        print word
    print("----")
