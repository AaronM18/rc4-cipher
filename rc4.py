
def getInput(lines = []):
  """ 
    Gets input from file input. Returns list of lines from input file
  """
  import fileinput
  return [ line.strip('\n') for line in fileinput.input() ]

class RC4:

  def ksa(self, key: str) -> list:
    keylength = len(key)

    S = list(range(256)) # 0 to 255
    
    j = 0
    for i in range(256):
      j = (j + S[i] + key[i % keylength]) % 256 # new value
      S[i], S[j] = S[j], S[i] # value swap
    
    return S
    
  def prga(self, S: list) -> str:
    i, j = 0, 0

    while True:
      i = (i + 1) % 256
      j = (j + S[i]) % 256
      S[i], S[j] = S[j], S[i]

      K = S[(S[i] + S[j]) % 256]
      yield K

  def buildKeyStream(self, key: str) -> list:
    key = [ord(c) for c in key]
    S = self.ksa(key)
    return self.prga(S)

  def encrypt(self, plaintText: str, key: str) -> str:
    keystream = self.buildKeyStream(key)

    cipherText = [ "%02X" % (ord(c) ^ next(keystream)) for c in plaintText ]

    return ''.join(cipherText)

  def decrypt(self, cipherText: str, key: str) -> str:
    import codecs

    keystream = self.buildKeyStream(key)

    cipherText = codecs.decode(cipherText, 'hex_codec')

    plaintText = [ "%02X" % (c ^ next(keystream)) for c in cipherText ]
    
    return codecs.decode(''.join(plaintText), 'hex_codec').decode('utf-8')




def main():
  rc4 = RC4()

  lines = getInput()

  cypherText = rc4.encrypt(lines[1], lines[0])
  print(cypherText)
  # plaintText = rc4.decrypt(cypherText, lines[0])
  # print(plaintText)

if __name__ == "__main__":
  main()