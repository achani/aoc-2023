from pathlib import Path

input_path = Path(__file__).parent.parent / "input" / "day01.tst"
file=open(input_path,'r')

d={'zero':0,'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9}

s=0
ans_lst=[]

for i in enumerate(file):
    first=None
    last=None
    highest=0
    lowest=0
    look_up={}
    st=i[1]
    for n in d:
        if n in st:
            look_up[st.find(n)]=n
    if len(look_up)>0:    
        highest=max(look_up)
        lowest=min(look_up)
        first=look_up[lowest]
        last=look_up[highest]

    ans=''
    front = 0
    back=len(st)-1
    
    while front<len(st) and not st[front].isdigit() :
        front += 1
    else:
        if not lowest and front<lowest:
            ans+=st[front]
        else:
            if first and not front<lowest:
                ans+=str(d[first])
            else:
                ans+=st[front]    

    while back>0 and not st[back].isdigit() :
        back -= 1
    else:
        if not highest and back>highest:
            ans +=  st[back]
        else:
            if last and not back>highest:
                ans+=str(d[last])
            else:
                ans+=st[back]
    s+=int(ans)
    ans_lst.append(int(ans))

print(ans_lst,len(ans_lst))    
print(sum(ans_lst))
print(s)