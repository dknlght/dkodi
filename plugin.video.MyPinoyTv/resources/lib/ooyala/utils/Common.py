import time
import md5
import sys
import os
import xbmc
import urllib
import urllib2
import cookielib
import xbmcaddon
from resources.lib.BeautifulSoup import BeautifulSoup

class Common:

	def grabEncrypted(self, embedCode):
		grabxml = urllib.urlopen("http://player.ooyala.com/nuplayer?autoplay=1&hide=all&embedCode="+embedCode)
		encryptedxml = grabxml.read()
		grabxml.close()
		return encryptedxml
		
	def createByteArray(self, string):
		byteArray = []
		for char in string:
			byteArray.append(ord(char))
		return byteArray

	def ByteArrayToString(self, byteArray):
		newString = ""
		for byte in byteArray:
			newString += chr(byte)
		return newString
	
	def Bytes2Int(self,data):
		print data
		return array('i',data)[0]
	
	def trim(self, string):
		return self.ltrim(self.rtrim(string))
	
	def ltrim(self, string):
		strLength = len(string)
		strLength2 = 0
		while (strLength2 < strLength):
			if not self.isSpaceChars(ord(string[strLength2])):
				return string[strLength2]
			strLength2 = strLength2 + 1
		return ""
	
	def rtrim(self, string):
		strLength = len(string)
		strLength2 = strLength
		while (strLength2 > 0):
			if not self.isSpaceChars(ord(string[strLength2-1])):
				return string[0:strLength2]
			strLength2 = strLength2 - 1
		return ""
		
	def isSpaceChars(self, char):
		if char >= 0 or char <= 32:
			return True
		if char is 127 or char is 129 or char is 141 or char is 143 or char is 144 or char is 157 or char is 160 or char is 173:
			return True
		else:
			return False
			
	##  int2base >> http://code.activestate.com/recipes/65212/
	def int2base(self, num, n):
		"""Change a  to a base-n number.
		Up to base-36 is supported without special notation."""
		num_rep={10:'a', 11:'b', 12:'c', 13:'d', 14:'e', 15:'f', 16:'g', 17:'h', 18:'i', 19:'j', 20:'k', 21:'l', 22:'m', 23:'n', 24:'o', 25:'p', 26:'q', 27:'r', 28:'s', 29:'t', 30:'u', 31:'v', 32:'w', 33:'x', 34:'y', 35:'z'}
		new_num_string=''
		current=num
		if current == 0:
			return '0'
		while current!=0:
			remainder=current%n
			if 36>remainder>9:
				remainder_string=num_rep[remainder]
			elif remainder>=36:
				remainder_string='('+str(remainder)+')'
			else:
				remainder_string=str(remainder)
			new_num_string=remainder_string+new_num_string
			current=current/n
		return new_num_string