#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mechanize
from bs4 import BeautifulSoup
import urllib2 
import cookielib
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('invault.cfg')

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("https://id.orange.fr/auth_user/bin/auth_user.cgi")

formcount=0
for frm in br.forms():
    if str(frm.attrs["id"])=="AuthentForm":
        break
    formcount=formcount+1

br.select_form(nr=formcount)
br.form['credential'] = config.get('OrangeADSL', 'username')
br.form['password'] = config.get('OrangeADSL', 'password')
br.submit()

br.open("https://espaceclientv3.orange.fr/?page=factures-historique")

soup = BeautifulSoup(br.response().read())

factures=soup.find("ul", {"class": "factures"})

for f in factures:
    d = f.find("span" , {"class": "colonneDate"}).text
    url = f.find("span", {"class": "colonneTelecharger"}).find("a")["href"]
    print("%s %s" % (d, url))
