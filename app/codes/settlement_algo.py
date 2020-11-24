def Sort_Tuple(tup):  
    lst = len(tup)  
    for i in range(0, lst):  
          
        for j in range(0, lst-i-1):  
            if (tup[j][1] > tup[j + 1][1]):  
                temp = tup[j]  
                tup[j]= tup[j + 1]  
                tup[j + 1]= temp  
    return tup 

def remove_ele(inp,val):
    temp = []
    if(val == 0):
        for i in range(1,len(inp)):
            temp.append(inp[i])

    if (val == -1):
        for i in range(0,len(inp)-1):
            temp.append(inp[i])
    return temp

def Settle(debt_input,limit = 500):

    inp = []
    ans = []
    ans_data = []
    for i in range(0,len(debt_input)):
        if(debt_input[i][1] != 0):
            inp.append([debt_input[i][0], debt_input[i][1], limit] )

    inp = Sort_Tuple(inp)

    while(len(inp) > 1):
        if(inp[0][1] + inp[-1][1] == 0):
            ans.append(inp[-1][0] + ' pays ' + inp[0][0] + ' Rs.' + str(inp[-1][1]) )
            ans_data.append([ inp[-1][0], inp[0][0], str(inp[-1][1]) ])
            inp = remove_ele(inp, 0)
            inp = remove_ele(inp, -1)
        elif(inp[0][1] + inp[-1][1] < 0):
            ans.append(inp[-1][0] + ' pays ' + inp[0][0] + ' Rs.' + str(inp[-1][1]) )
            ans_data.append([ inp[-1][0], inp[0][0], str(inp[-1][1]) ])
            inp[0][1] += inp[-1][1]
            inp = remove_ele(inp, -1)
        elif(inp[0][1] + inp[-1][1] > 0):
            if( inp[0][1] + inp[-1][1] > inp[0][2] ):
                ans.append(inp[-1][0] + ' pays ' + inp[0][0] + ' Rs.' + str(-1*inp[0][1]))
                ans_data.append([ inp[-1][0], inp[0][0], str(-1 * inp[0][1]) ])
                inp[-1][1] += inp[0][1]
                inp = remove_ele(inp,0)
            else:
                ans.append(inp[-1][0] + ' pays ' + inp[0][0] + ' Rs.' + str(inp[-1][1]) )
                ans_data.append([ inp[-1][0], inp[0][0], str(inp[-1][1]) ])
                inp[0][1] += inp[-1][1]
                inp = remove_ele(inp,-1)
        inp = Sort_Tuple(inp)
    return (ans,ans_data)

# p =[('A',-50), ('B',-30), ('C',+10), ('D',+20), ('E',+40),('F',-100),('G',+110)]
# r = [('A',0),('B',0)]
# x = []
# print(Settle( p )[0])
