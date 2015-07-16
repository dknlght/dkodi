from array import array

class Base64Decoder:
	def __init__(self):
		pass

	def Int2Bytes(self, data):
	    return array('i',[data]).tostring()

	def decode(self, encoded):
		ESCAPE_CHAR_CODE_1 = 61
		ESCAPE_CHAR_CODE_2 = 42
		count = 0
		filled = 0
		data = []
		newstring = ""
		work = [0, 0, 0, 0]
		inverse = [64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 62, 64, 64, 64, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 64, 64, 64, 64, 64, 64, 64, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 64, 64, 64, 64, 64, 64, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64];
		i = 0
		length = len(encoded)
		
		for i, char in enumerate(encoded):
			c = ord(encoded[i])
			if c == ESCAPE_CHAR_CODE_1 or c == ESCAPE_CHAR_CODE_2:
				work[count] = -1;
				count = count + 1
			elif inverse[c] != 64:
				work[count] = inverse[c]
				count = count + 1
		
			if count == 4:
				count = 0
				newstring += self.Int2Bytes((work[0] << 2) | ((work[1] & 0xFF) >> 4))
				filled = filled + 1

				if work[2] == -1:
					break;
				
				newstring += self.Int2Bytes((work[1] << 4) | ((work[2] & 0xFF) >> 2))
				filled = filled + 1
				
				if work[3] == -1:
					break;
				
				newstring += self.Int2Bytes((work[2] << 6) | work[3])
				filled = filled + 1
				
		for char in newstring[0::4]:
			data.append(ord(char))
		return data