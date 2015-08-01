import zlib
import struct
from array import array
#from Crypto.Cipher import AES
from utils.Common import Common
from MagicNaming import MagicNaming
from binascii import hexlify, unhexlify
from utils.Base64Decoder import Base64Decoder

from crypto.cipher.aes_cbc import AES_CBC
from crypto.cipher.base import noPadding

class ooyalaCrypto:
	def __init__(self):
		pass

	def ooyalaDecrypt(self, data):
		
		print "Ooyala: --> Attempting to decrypt SMIL..."
		
		crypt = {'KEY':'4b3d32bed59fb8c54ab8a190d5d147f0e4f0cbe6804c8e0721175ab68b40cb01','IV':'00020406080a0c0ea0a2a4a6a8aaacae'}
		decodedByteArray = Base64Decoder().decode(data)
		data = Common().ByteArrayToString(decodedByteArray)
		aes_key = unhexlify(crypt['KEY'])
		iv_bytes = iv=unhexlify(crypt['IV'])
		d = iv_bytes + data
		cipher = AES_CBC(aes_key, padding=noPadding(), keySize=32)
		v = cipher.decrypt(d)
		length = struct.unpack('>I', v[:4])[0]
		compressed = v[4:length+4]
		decompressed = zlib.decompress(compressed)
		
		print "Ooyala: --> SMIL decrypted successfully."
		
		return decompressed[16:]