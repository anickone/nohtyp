#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#m=int(sys.argv[1])
m=3
a=list('absd')
s=[]
def p(n,s):
	if n > 0:
		for i in a:
			s.append(i)
			p(n-1,s)
			s.pop()
	else:
		print ''.join(s)
for i in range(m+1):
	p(i,s)
