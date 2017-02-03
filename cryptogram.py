#!/usr/bin/python
# coding: utf-8
#cryptogram.py
#grabs a quote from the web and makes it a cryptogram.

import random
import urllib
import requests
from HTMLParser import HTMLParser
from lxml import html
from lxml import *
import argparse

parser = argparse.ArgumentParser(prog='cryptogram.py', description='This program creates cryptograms from quotes on websites. It creates a file called "cryptograms.txt" and "cryptogram-answers.txt" in the directory the script was run.')
parser.add_argument('-num', type=int, default=1, help='number of cryptograms you want created. Default is 1.')
parser.add_argument('-answerfile', default='cryptogram-answers.txt', help='file to save answer to. Default is cryptogram-answers.txt.')
parser.add_argument('-cryptogramfile', default='cryptograms.txt', help='file to save answer to. Default is cryptograms.txt.')

args = parser.parse_args()
#print args.num

################ Variables ################
websites = [{'url':"https://www.goodreads.com/quotes/", 'xpath':'//div[@class="quoteText"]/text()'}, {'url':"https://www.goodreads.com/quotes/tag/science", 'xpath':'//div[@class="quoteText"]/text()'}, {'url':"https://www.goodreads.com/quotes/tag/life", 'xpath':'//div[@class="quoteText"]/text()'}, {'url':"https://www.goodreads.com/quotes/tag/humor", 'xpath':'//div[@class="quoteText"]/text()'}, {'url':"http://www.gunnar.cc/quotes/text.html", 'xpath':'//font[@face="COMIC SANS MS, ROCKWELL"]/text()'}, {'url': 'https://twitter.com/greatestquotes', 'xpath': '//p[@class="TweetTextSize TweetTextSize--16px js-tweet-text tweet-text"]/text()'}]

alphabet = list('abcdefghijklmnopqrstuvwxyz')
random_alphabet = ''


############### Functions ################
def GetWebsite():
    #randomly selects a website from those supplied in program
    max = len(websites)
    chosen = random.randint(0,max-1)
    #chosen = max - 1
    return websites[chosen]

def RemoveUnprintable(string):
    #removes or replaces some unicode characters that don't have ascii char
    printable = string.replace("&#226", "'")
    printable = printable.replace("&#8220", "\"")
    printable = printable.replace("&#128", "")
    printable = printable.replace("&#153", "")
    printable = printable.replace("&#8221", "\"")
    printable = printable.replace("&#8213", "")
    return printable

def GetSentence(link, xpath):
    #scrapes a webpage for the quotes to use
    page = requests.get(link)
    enc = page.encoding
    # remove malformed br tags that were causing issues parsing the quotes
    pagetext = page.content.replace('br /', '/br')
    #create an htmlelement out of the unicode text
    tree = html.fromstring(pagetext)
    # select the quotes based on the xpath filter
    quotes = tree.xpath(xpath)
    goodquotes =[]
    for quote in quotes:
        # encode and clean up quotes
        quoteclean = quote.encode('ascii', 'xmlcharrefreplace').strip()
        quoteclean = quoteclean.encode(enc)
        quoteclean = RemoveUnprintable(quoteclean)
        if len(quoteclean) > 4 and quoteclean <> "Recommended Reading":
             goodquotes.append(quoteclean)
    max = len(goodquotes)
    chosen = random.randint(0,max-1)
    sentence = (goodquotes[chosen])
    return sentence


def RandomizeAlphabet():
    #returns a random alphabet to use as the substitution cipher
    randomized = list(alphabet)
    random.shuffle(randomized)
    return randomized
    
def ZipLists(list1, list2):
    #defines the substitution cipher based on the randomized alphabet
    #if finds plaintext letters that are the same as the crypto letters
    #it swaps them so they're different
    zipped = dict(zip(list1, list2))
    sames = []
    for key in zipped:
        if key == zipped[key]:
            sames.append(key)
    if sames <> "":
        for each in sames:
            index = (len(sames) - sames.index(each)) -1
            zipped[each] = sames[index]
    return zipped

def CryptogramIt(sentence, zipped_alphabet):
    #takes quote and applies substitution cipher to make cryptogram
    cryptogram =""
    sentence = sentence.lower()
    for let in sentence:
        if let not in alphabet:
            cryptogram = cryptogram + let
        else:
            cryptogram = cryptogram + zipped_alphabet[let]
    return cryptogram


################ Main program ############
for i in range(0, args.num):
    if i == 0:
        cryptogramfile = open(args.cryptogramfile, 'w')
        answerfile = open(args.answerfile, 'w')
    else:
        cryptogramfile = open(args.cryptogramfile, 'a')
        answerfile = open(args.answerfile, 'a')       
    website = GetWebsite()
    sentence = GetSentence(website['url'], website['xpath'])
    random_alphabet = RandomizeAlphabet()
    zipped_alphabet = ZipLists(alphabet, random_alphabet)
    cryptogram = CryptogramIt(sentence, zipped_alphabet)
    cryptogramfile.write(str(i+1) +") " + cryptogram + "\n\n")
    answerfile.write(str(i+1) +") " + sentence + "\n" + str(zipped_alphabet) +"\n\n")


