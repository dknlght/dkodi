import re
import base64
import utils.sha256 as sha256
from utils.Common import Common
from resources.lib.BeautifulSoup import BeautifulSoup

MAGIC_STRING_DESCRIPTOR_SEED = "BH5c@EYh^^*&%";
MAGIC_STRING_FIRST_HASH_A = "O0yLA $^&%*)(=";
MAGIC_STRING_FIRST_HASH_B = "siiKret~";
MAGIC_STRING_SECOND_HASH = "0o0%^&GHYb";

class MagicNaming:
	def __init__(self):
		pass
	
	def getVideoUrl(self, smil):
		chunkArray = []

		print "Ooyala: --> Calculating video URL..."

		soup = BeautifulSoup(smil)
		rtmpDomain = soup.find('rtmpdomains').string
		rtmpDomain = rtmpDomain.split(',')[0]
		httpDomain = soup.find('domains').string
		httpDomain = httpDomain.split(',')[0]
		vData = soup.find('vdata')
		if vData:
			streams = vData.findAll('stream', attrs={'f':'h264'})
			streams = sorted(streams, key=lambda x: x['w'])
# 			version = vData['version']
			version = "1:1" ## Overriding 'version' for PostTV
			embedCode = vData['embedcode']
			ts = str(vData.find('ts').string)
			tsArray = ts.split(",")
			domain = ""
			if len(tsArray) > 2:
				domain = "http://" + httpDomain + "/"
			else:
				domain = rtmpDomain + "/mp4:s/"
			vidLength = len(tsArray)-1
			for i, startTime in enumerate(tsArray[:vidLength]):
				index = i
				start = int(startTime)
				br = int(streams[-1]['br'])
				width = int(streams[-1]['w'])
				url = self.getChunkUrl(embedCode, version, index, start, br, width)
				url = domain + url
				chunkArray.append(url)
		else:
			print "Ooyala: --> Could not find vData, trying the other."
			promo = soup.find('promo')
			promoVids = re.findall('[A-z0-9]{32}', promo)
			chunkArray.append(rtmpDomain + str(promoVids[0]) + str(promoVids[-1]))
			print "Ooyala: --> Formed the following URL: " + str(chunkArray[0])
		print "Ooyala: --> Successfully formed URL."
		return chunkArray
	
	def getChunkUrl(self, embedCode, version, index, start, br, width):
		local7 = self.getRevisionAndVersion(version)[1];
		local8 = self.generateCommondId(local7, self.transformChunkIndex(index), self.transformBitrate(br), self.transformWidth(width))
		local9 = Common().int2base(start,16);
		finalString = self.generateFinalString(embedCode, local8, self.generateFirstHash(local8), self.generateSecondHash(local9))
		return finalString

	def getRevisionAndVersion(self, param1):
		local2 = param1.split(":")
		if len(local2) < 2:
			return [local2[0], ""]
		local3 = local2[1].find(".")
		if local3 != -1:
			local4 = local2[1][0:local3]
			local5 = local2[1][local3+1:]
		else:
			local4 = ""
			local5 = local2[1]
		return [local4, local5]

	def transformChunkIndex(self, index):
		chunkIndex = Common().int2base(index, 35)
		if len(chunkIndex) > 1:
			return chunkIndex[::-1]
		else:
			return chunkIndex
	
	def transformBitrate(self, bitrate):
		bitrateStr = Common().int2base(bitrate, 33)
		return bitrateStr
	
	def transformWidth(self, width):
		widthStr = Common().int2base(width, 32)
		return widthStr[::-1]
	
	def generateChunkName(self, commonId, firstHash, secondHash):
		loc4 = []
		for char in commonId:
			loc4.append(ord(char))
		loc6 = []
		loc6.extend(Common().createByteArray(secondHash[2:15]))
		loc6.extend(loc4)
		loc6.extend(Common().createByteArray(firstHash))
		newString = Common().ByteArrayToString(loc6)
		return base64.standard_b64encode(newString).replace("+","-").replace("/","_")[2:34]
	
	def generateFinalString(self, embedCode, commonId, firstHash, secondHash, pcode = None, pathformat = None):
		if pathformat == None:
			return embedCode + "/" + self.generateChunkName(commonId, firstHash, secondHash)
		else:
			FinalString = pathformat
			FinalString.replace("%%embed_code%%",embedCode).replace("%%pcode%%",pcode).replace("%%file_name%%", self.generateChunkName(commonId, firstHash, secondHash)).replace("%%extension_if_mp4%%", "")
			return FinalString

	def generateFirstHash(self, string):
		tohash = str(MAGIC_STRING_FIRST_HASH_A + string + MAGIC_STRING_FIRST_HASH_B)
		hash = sha256.sha256(tohash).digest()
		return hash

	def generateSecondHash(self, string):
		tohash = str(MAGIC_STRING_SECOND_HASH + string)
		hash = sha256.sha256(tohash).digest()
		return hash

	def generateCommondId(self, param1, param2, param3, param4):
		return param1 + param2 + ":" + param3 + ":" + param4 + ";"
