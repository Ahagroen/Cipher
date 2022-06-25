import secrets
def Main():
    incoming = inputGet()
    #version = incoming.versionCheck()
    direction = incoming.getDirection()
    textIn = incoming.getMessage(direction)
    keyIn = incoming.getKey()
    textOut = encode(textIn, keyIn, direction)
    output(textOut, direction)
    checkClose(direction, keyIn)

def recycle(key, direction):
    incoming = inputGet()
    textIn = incoming.getMessage(direction)
    textOut = encode(textIn, key, direction)
    output(textOut, direction)
    checkClose(direction, key)

def padding(textIn, direction):
    if direction == 1:
        #add padding char's
        #direction and quantity should be random
        #should ensure total message length is divisable by 4 for easy message transcription
        paddingChar = int(41)
        #print(textIn)
        textIn.insert(secrets.randbelow(len(textIn)), 41)
        #print (textIn)
        length = int(len(textIn))
        #print (length) 
        while length %4 != 0:
            textIn.insert(secrets.randbelow(len(textIn)), paddingChar)
            #print (textIn)
            length = int(len(textIn))
            #print (length)
        return textIn
    else:
        #remove padding char's
        textOut = textIn.replace('&','')
        return textOut
class inputGet:
    textIn = [0]
    keyIn = [0]
    direction = 0
    version = 0
    def versionCheck(self):
        print('Which encryption scheme was used?')
        print('(1) for version one, (2) for version 2')
        version = input('version = ')
        return version
    def getMessage(self, direction):
        #gets message and key (key Identifier only?)
        if direction == 0:
            print('Provide code')
            message = input("code = ")
            message = message.replace(' ','')
            #print (message)
        else:
            print('Provide Message')
            message = input("Message = ")
        textIn = convertText(message, direction)
        return textIn
    def getKey(self):
        print("Provide Key")
        key = input("Key = ")
        #textIn and keyIn must be arrays
        keyIn = convertText(key, 2)
        return keyIn
    def getDirection(self):
        print("(E)ncryption or (D)ecryption ?")
        directionIn = ord(input("E/D = ").lower())
        if directionIn == 101:
            direction = 1
        elif directionIn == 100:
            direction = 0
        else:
            print("not a valid option")
            exit()
        #print (directionIn)
        #print (direction)
        return direction

def convertText(text, direction):
    #converts string to values for usage
    #will need to be called twice (once for message and once for key)]
    imput = text.lower()
    output = []
    for letter in imput:
            # 0 corrisponds to space
        if letter == '?':
            number = 38
            #38 corrisponds to ?
        elif letter == ',':
            number = 39
            #39 corrisponds to .
        elif letter == '/':
            number = 37
            #37 corrisponds to /
        elif letter == '.':
            number = 40
            #40 corrisponds to .
        elif letter.isnumeric() == True:
            letter = int(letter)
            number = letter+27
            #numbers occupy 27-36
        elif letter.isalpha() == True:
            #swaps letters
            number = ord(letter) - 96
        elif letter == ' ':
            number = 0
        elif letter == '!':
            number = 0
        elif letter == '&' and direction == 0:
            number = 41
            #in plaintext this should never occur, as it acts as the padding charecter
        else:
            print('invalid input value; only alphanumeric as well as !, space, slash, period and comma can be used')
            break
        output.append(number)
    return output
    
def encode(textIn, keyIn, direction):
    #takes plaintext number and converts it into encoded number with encryption scheme
    x = 0
    codeOut = []
    y = 0
    if direction == 1:
        textIn = padding(textIn, direction)
        while x != len(textIn):
           encodedNum = textIn[x] + keyIn[y]
           code = encodedNum % 42
           x = x+1
           yNew = y+1
           y = yNew % len(keyIn)
           codeOut.append(code)
    else:
        while x != len(textIn):
            #print (textIn[x])
            encodedNum = textIn[x] - keyIn[y]
            code = encodedNum % 42
            x = x+1
            yNew = y+1
            y = yNew % len(keyIn)
            codeOut.append(code)
    #print(codeOut)
    textOut = convertNum(codeOut, direction)
    return textOut

def convertNum(values, direction):
    #converts values back to string
    output = ''
    for letter in values:
        if letter == 0 and direction == 1:
            number = '!'
            # 0 corrisponds to space
        elif letter == 0 and direction == 0:
            number = ' '
        elif letter == 41:
            number = '&'
        #serves as padding char, will get stripped out if decryption
        elif letter == 38:
            number = '?'
            #38 corrisponds to ?
        elif letter == 40:
            number = '.'
        elif letter == 39:
            number = ','
            #39 corrisponds to .
        elif letter == 37:
            number = '/'
            #37 corrisponds to /
        elif letter < 27:
            letter = letter+96
            number = chr(letter)
            #numbers occupy 27-36
        else: 
            number = letter-27
            number = number+48
            number = chr(number)
        output += number
    return output

def output(outgoing, direction):
    print('')
    out = outgoing
    #prints message and whether it was encoded or decoded, along with key identifier/key
    if direction == 1:
        out = ' '.join([out[i:i+4] for i in range(0, len(out), 4)])
        print ('encoded text = \n',out, '\n')
    else:
        out = padding(out, direction)
        print('plaintext = \n',out, '\n')
    #input("Press enter to exit (work will be deleted to ensure security)")

def checkClose(direction, key):
    print('')
    if direction == 1:
        print('If you would like to decrypt a message with the same key, press D \n If you would like to encrypt another message with this key, press E \n to close, press any other key')
    elif direction == 0:
        print('If you would like to decrypt another message with the same key, press D \n If you would like to encrypt a message with this key, press E \n to close, press any other key')
    answer = input('selection = ') 
    if answer == 'd' or answer == 'D':
        recycle(key, 0)
    elif answer == 'e' or answer == 'E':
        recycle (key, 1)
if __name__ == '__main__':             
    Main()