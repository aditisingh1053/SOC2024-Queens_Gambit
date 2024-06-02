def isnim(l):
    newl=[]
    t=max(l)
    binary_t = bin(t)
    stripped_binary_t = binary_t.lstrip('-0b')
    for i in range (len(l)):
        binary = bin(l[i])[2:].zfill(len(stripped_binary_t))        
        newl.append(binary)
    c=True
    for i in range (len(stripped_binary_t)):
        k=0
        for j in range (len(l)):
            # print(newl[j])
            if newl[j][i]=='1':
                k+=1
        if (k%2!=0):
            c=False
            break
    return c

def print_general():
    print("GENERAL INSTRUCTION")
    print("Enter your moves as (a,b) seperated by comma where a is the heap no. starting from 0 and b is no. of elements you want to remove")


def response_computer(l,c):
    print("Computer's move: ",end=" ")
    row=0
    no=1
    for i in range (len(l)):
        kyu=0
        for j in range (1,l[i]+1):
            jnew=[]
            for ele in l:
                jnew.append(ele)

            # print(l)
            jnew[i]=jnew[i]-j
            if jnew[i]==0:
                jnew.pop(i)       
                    

            if len(jnew)>0 and isnim(jnew):
                row=i
                no=j
                kyu=1
                break
        if kyu==1:
            break
    res=[row,no]
    print(row,no)
    # print(l)
    l[res[0]]=l[res[0]]-res[1]
    if(l[res[0]]==0):
        l.pop(res[0])
        if len(l)==0:
            # print(l)
            return False
    # print(l)
    return True




def game_with_computer():
    print("Would you want to play first(y/n)")
    play=input()  
    if play=='y':
        l=inputstack()
        print_general()
        c=0
        end=True
        while(end):
            printnim(l)
            if(c==0):
                end=response(l,c)
                c=1
            else:
                end=response_computer(l,c)
                c=0
            
        if c==1:
            print("Player wins")
        else :
            print("Computer wins")
    elif play=='n':
        l=inputstack()
        print_general()
        c=0
        end=True
        while(end):
            printnim(l)
            if(c==0):
                end=response_computer(l,c)
                c=1
            else:
                end=response(l,c-1)
                c=0
            
        if c==1:
            print("Computer wins")
        else :
            print("Player wins")
    else:
        print("Enter valid input y/n ")
        game_with_computer()

def printnim(l):
    print("Current heap status")
    for i in range (len(l)):
        print(i,end=" ") 
        for j in range (l[i]):
            print("| ",end="")
        print(end="\n")

def response(l,c):
    print("Enter your move Player",c+1,end=": ")
    res=input()
    res=res.split(',')
    res[0]=int(res[0])
    res[1]=int(res[1])
    if (res[0]>=len(l)):
        print("Invalid response! 1st no. should be between 0 to",len(l)-1)
        newresponse=response(l,c)
        return newresponse
    elif l[res[0]]<res[1] or res[1]==0:
        print("Invalid response! 2nd no. should be between 1 to",l[res[0]])
        newresponse=response(l,c)
        return newresponse
    else:
        l[res[0]]=l[res[0]]-res[1]
        if(l[res[0]]==0):
            l.pop(res[0])
            if len(l)==0:
                return False
    return True

        
def inputstack():
    print("How many heaps do you want")
    n=int(input())
    print("Enter the no. of elements in each heap")
    l=input()
    l=l.split()
    if len(l)!=n:
        print("Invalid input try again")
        l=inputstack()
        return l
    for i in range (n):
        l[i]=int(l[i])
    return l
       
def maingame():
    print("Would you like to play 2p game or with computer (2p/c)")
    c=input()
    if(c=='2p'):
        l=inputstack()    
        print_general()
        c=0
        end=True
        while(end):
            printnim(l)
            if(c==0):
                end=response(l,c)
                c=1
            else:
                end=response(l,c)
                c=0
            
        if c==0:
            print("Player 2 wins")
        else :
            print("Player 1 wins")
    elif c=='c':
        game_with_computer()
        
    else:
        print("Enter valid input either '2p' or 'c'")
        maingame()

maingame()



