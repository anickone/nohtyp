#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import xml.etree.ElementTree as ET

url='http://informer.gismeteo.ru/xml/27612_1.xml'
page=urllib.urlopen(url).read()
root = ET.fromstring(page)

weekday=['воскресенье','понедельник','вторник','среду','четверг','пятницу','субботу']
tod=['ночь','утро', 'день', 'вечер']

sity=root[0][0].attrib
print u'Город: %s, географические координаты(широта: %s, долгота: %s)' % ( urllib.unquote(sity['sname']).decode('cp1251') ,sity['latitude'],sity['longitude'])

data=root[0][0][0].attrib
print 'Прогноз на %s(%s.%s.%s)' % (weekday[int(data['weekday'])-1],data['day'],data['month'],data['year'])

for i,itod in enumerate(tod):
	print '%s:' % itod

	pressure=root[0][0][i][1].attrib
	print 'Давление: %s-%s мм.рт.ст.' % (pressure['min'],pressure['max'])

	temperature=root[0][0][i][2].attrib
	print 'Температура: %s...%s гр.' % (temperature['min'],temperature['max'])

	wind=root[0][0][i][3].attrib
	print 'Ветер: %s-%s м/с' % (wind['min'],wind['max'])

	relwet=root[0][0][i][4].attrib
	print 'Влажность: %s-%s %%' % (relwet['min'],relwet['max'])
	
	print '-'*35
