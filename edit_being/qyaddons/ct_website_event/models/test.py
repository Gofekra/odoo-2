#!c:Program Filespython252python.ex
# -*- coding: utf-8 -*-
import re,urllib2
from subprocess import Popen, PIPE
print  re.search('d+.d+.d+.d+',Popen('ipconfig', stdout=PIPE).stdout.read())
print re.search('d+.d+.d+.d+',urllib2.urlopen("http://city.ip138.com/ip2city.asp").read())