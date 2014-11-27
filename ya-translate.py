#!/usr/bin/python
# -*- coding: utf-8 -*-

# translate with yandex

import sys, re, json, urllib, os

help='''
DESCRIPTION
  ya-translate.py - переводит англ. слова с помощью яндекса
SYNOPSIS
  ya-translate.py filename
    filename - файл с англ. текстом'''

def file_save(li,name):
  if bool(li)==False:
    return
  s='\n'.join(li)
  file_name='%s.txt' % name
  f=open(file_name,'w')
  f.write(s)
  f.close()

def file_read(name):
  f=open(name,'r')
  s=f.read()
  f.close()
  return s

if len(sys.argv)==1:
  print 'Нет параметров для запуска!'
  print help
  sys.exit(1)

# I known this words
fwords='mywords.txt'
if os.path.isfile(fwords):
  s=file_read(fwords)
else:
  s='i - я\na - артикль'
  file_save(s.split('\n'),fwords[:-4])

mywords=s.strip()
limywords=mywords.split('\n')

dicmyword={}
pattern=r"^([a-z]+)\s-\s(.+)$"
p_my_words=re.compile(pattern)
for line in limywords:
  res=p_my_words.findall(line)
  dicmyword[res[0][0]]=res[0][1]

# english text 
s=file_read(sys.argv[1])

txt=s.lower()
pattern=r"([a-z]+)"
p=re.compile(pattern)
res=p.findall(txt)

txt_dic={}
for key in res:
  if len(key)<2:
    continue
  else:
    if key in txt_dic:
      txt_dic[key]+=1
    else:
      txt_dic[key]=1

for word in txt_dic.keys():
  if word in dicmyword:
    txt_dic.pop(word)

li=txt_dic.keys()
if bool(li)==False:
  print 'нет новых слов'
  sys.exit(0)
li.sort()

url='https://translate.yandex.net/api/v1.5/tr.json/translate'
# free key get here: http://api.yandex.ru/key/form.xml?service=trnsl
key='enter free yandex key'
lang='en-ru'
code={
200:'Операция выполнена успешно',
401:'Неправильный ключ API',
402:'Ключ API заблокирован',
403:'Превышено суточное ограничение на количество запросов',
404:'Превышено суточное ограничение на объем переведенного текста',
413:'Превышен максимально допустимый размер текста',
422:'Текст не может быть переведен',
501:'Заданное направление перевода не поддерживается'
}
ltr=[]
lerr=[]

for word in li:
  query='%s?key=%s&text=%s&lang=%s' % (url,key,word,lang)
  fs=urllib.urlopen(query)
  s=fs.read()
  d=json.loads(s)
  if d['code']==200:
    wordtr=d['text'][0].encode('utf-8')
    if word==wordtr:
      err='%s - %s' % (word,'нет перевода')
      lerr.append(err)
    else:
      wordTranslate='%s - %s' % (word,wordtr)
      print wordTranslate
      ltr.append(wordTranslate)
  elif d['code']==422:
    err='%s - %s' % (word,code[d['code']])
    lerr.append(err)
    print err
  else:
    print 'Error - ',code[d['code']]
    sys.exit()

file_save(li,'word_sort')
file_save(ltr,'word_translated')
file_save(lerr,'word_unknowns')
