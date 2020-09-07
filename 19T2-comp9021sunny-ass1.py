standard={'I':1,'V':5,'X':10,'L':50,'C':100}
mode_list = []
out_put_dic = {}

#yuchen yang
def make_ele(string):
    x,v,i=string
    return ['',i,i+i,i+i+i,i+v,v,v+i,v+i+i,v+i+i+i,i+x]

#yuchen yang 
def get_index(string):
    return [string.index(i) for i in string]

#yuchen yang 
def create_dic(model='MDCLXVI'):
    model = "___" + model
    index=1
    diction={}
    temp=''
    for i in model[::-1]:
        temp=i+temp
        if len(temp)==3:
            diction[index]=make_ele(temp)
            index*=10
            temp=i
    return diction

#yuchen yang 
def convert_int(digit,model="MDCLXVI"):
    diction=create_dic(model)
    index=1
    out_put=''
    while digit>0:
        try:
            out_put=diction[index][digit%10]+out_put
        except:
            print('error')
        digit//=10
        index*=10
    if "_" in out_put:
        return False
    else:
        return out_put

#yuchen yang 
def convert_symbol(symbol,model="MDCLXVI"):
    prev=''
    diction=create_dic(model)
    dic_index=max(diction.keys())
    out_put=0
    for index in range(len(symbol)):
        curr=symbol[index]
        combine=prev+curr
        if combine in diction[dic_index]:
            prev=combine
        else:
            out_put+=diction[dic_index].index(prev)*dic_index
            dic_index //= 10
            try:
                while curr not in diction[dic_index]:
                    dic_index//=10
            except:
                print("error")
                break
            prev=curr
    out_put += diction[dic_index].index(prev) * dic_index
    print(out_put)

#yuchen yang 
def convert_mode(prev,digit):
    try:
        prev_mode = get_index(prev)
        temp = convert_int(mode_list.index(prev_mode))
        for j in range(len(temp)):
            out_put_dic[standard[temp[j]] * (10 ** digit)] = prev[j]
        return str(mode_list.index(prev_mode))
    except:
        return False

#yuchen yang 
def convert_symbol_2(symbol):
    prev=out_put=''
    for i in make_ele('CLX'):
        for j in make_ele('XVI'):
            mode_list.append(get_index(i + j))
    index=0
    symbol=symbol[::-1]
    while index < len(symbol):
        curr=symbol[index]
        index+=1
        while curr[0] in symbol[index:]:
            curr+=symbol[index]
            index+=1
        curr=curr[::-1]
        combine=curr+prev
        if get_index(combine) in mode_list:
            prev=combine
        else:
            out_put= convert_mode(prev,len(out_put)) + out_put
            prev = curr

    out_put = convert_mode(prev, len(out_put)) + out_put
    print(out_put)


convert_int(2345)
convert_symbol("EeDEBBBaA",'fFeEdDcCbBaA')
print(convert_symbol_2('abcaddefgf'))
print(out_put_dic)
max_key=max(out_put_dic.keys())
roman_symbol=''
while max_key > 0:
    if max_key in out_put_dic:
        roman_symbol+=str(out_put_dic[max_key])
    else:
        roman_symbol+='_'
    if str(max_key)[0]=='1':
        max_key//=2
    else:
        max_key//=5
print(roman_symbol)
# yuchen yang 
