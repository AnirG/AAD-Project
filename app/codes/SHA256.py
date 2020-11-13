# SHA256


two_pow_32=4294967296
def Shift_Right(shift_bits,value):
    return ((value>>shift_bits)%two_pow_32)

def Right_Rotation(rotate_bits,value):
    rotate_bits=(rotate_bits)%32
    return (((value>>rotate_bits) + (value<<(32-rotate_bits)))%two_pow_32)

def Exclusive_OR(x=0,y=0,z=0):
    return ((x^y)^z)

def Add(a=0,b=0,c=0,d=0,e=0):
    values=[a,b,c,d,e]
    ans=0
    for i in values:
        ans = ((ans + i) % two_pow_32)
    return ans




def Lower_Sigma_0(value):
    a = Right_Rotation(7,value)
    b = Right_Rotation(18,value)
    c = Shift_Right(3,value)
    ans = Exclusive_OR(a,b,c)
    return ans

def Lower_Sigma_1(value):
    a = Right_Rotation(17,value)
    b = Right_Rotation(19,value)
    c = Shift_Right(10,value)
    ans = Exclusive_OR(a,b,c)
    return ans

def Upper_Sigma_0(value):
    a = Right_Rotation(2,value)
    b = Right_Rotation(13,value)
    c = Right_Rotation(22,value)
    ans = Exclusive_OR(a,b,c)
    return ans

def Upper_Sigma_1(value):
    a = Right_Rotation(6,value)
    b = Right_Rotation(11,value)
    c = Right_Rotation(25,value)
    ans = Exclusive_OR(a,b,c)
    return ans

def Choice(x,y,z):
    x = x % two_pow_32
    y = y % two_pow_32
    z = z % two_pow_32
    ans = 0
    for i in range(0,32):
        if(x&(1<<i) == (1<<i)):
            ans+= (y&(1<<i))
        else:
            ans+= (z&(1<<i))
    return ans

def Majority(x,y,z):
    x = x % two_pow_32
    y = y % two_pow_32
    z = z % two_pow_32
    ans = 0
    for i in range(0,32):
        t=0
        if(x&(1<<i) == (1<<i)):
            t+=1
        if(y&(1<<i) == (1<<i)):
            t+=1
        if(z&(1<<i) == (1<<i)):
            t+=1
        if(t >= 2):
            ans+= (1<<i)
    return ans



def pad(input_binary):
    input_length = len(input_binary)
    x = (input_length + 64) % 512
    x = 512 - x
    for i in range(0,x):
        if(i==0):
            input_binary += '1'
        else:
            input_binary += '0'
    size_in_binary=len(format(input_length,'b'))
    x = 64 - size_in_binary
    for i in range(0,x):
        input_binary += '0'
    input_binary+= format(input_length,'b')
    output=[]
    x=int(len(input_binary)/512)
    for i in range(0,x):
        output.append(''.join(input_binary[(i*512) + j] for j in range(0,512) ) )
    return output


def make_message_schedule(message_block):
    output =[]
    for i in range(0,16):
        temp = int(''.join(message_block[(i*32) + j] for j in range(0,32) ), 2)
        output.append(temp)
    for i in range(16,64):
        temp = Add( Lower_Sigma_1(output[i-2]) , output[i-7] , Lower_Sigma_0(output[i-15]) , output[i-16] )
        output.append(temp)
    return output



   
def SHA256(input_str):
    Constant = []
    Hash1 = []
    binary_answer = ''
    hexadecimal_answer = ''
    for i in range(64):
        Constant.append(0)
    for i in range(8):
        Hash1.append(0)

    input_binary = ''.join(format(ord(i), 'b') for i in input_str)
    message_blocks = pad(input_binary)
    for message_block in message_blocks:
        message_schedule = make_message_schedule(message_block)
        Hash2 = Hash1
        for i in range(0,64):
            T1 = Add( Upper_Sigma_1(Hash2[4]) , Choice(Hash2[4],Hash2[5],Hash2[6]) , Hash2[7] , Constant[i] , message_schedule[i] )
            T2 = Add( Upper_Sigma_0(Hash2[0]) , Majority(Hash2[0],Hash2[1],Hash2[2]) )
            for j in range(7):
                Hash2[7 - j] = Hash2[6 - j]
            Hash2[0] = Add(T1,T2)
            Hash2[4] = Add(Hash2[4],T1)
        for i in range(8):
            Hash1[i] = Add(Hash1[i],Hash2[i])
        for i in Hash1:
            temp = format(i,'b')
            x = 32 - len(temp)
            if(x>0):
                for j in range(x):
                    binary_answer+='0'
            binary_answer+=temp
        for i in range(64):
            temp = 8*(int(binary_answer[i*4])) + 4*(int(binary_answer[(i*4)+1])) + 2*(int(binary_answer[(i*4)+2])) + (int(binary_answer[(i*4)+3]))
            if(temp == 10):
                hexadecimal_answer+='a'
            elif(temp == 11):
                hexadecimal_answer+='b'
            elif(temp == 12):
                hexadecimal_answer+='c'
            elif(temp == 13):
                hexadecimal_answer+='d'
            elif(temp == 14):
                hexadecimal_answer+='e'
            elif(temp == 15):
                hexadecimal_answer+='f'
            else:
                hexadecimal_answer+= str(temp)
        #print(binary_answer)
        #print(hexadecimal_answer)
        return binary_answer, hexadecimal_answer

# if __name__ == "__main__":
#     inp = input()
#     print(SHA256(inp))