
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
    res=res.split('_')
    res[0]=int(res[0])
    res[1]=int(res[1])
    if (res[0]>=len(l)):
        print("Invalid response!")
        response(l,c)
    elif l[res[0]]<res[1]:
        print("Invalid response! Heap overflow")
        response(l,c)
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
        inputstack()
    for i in range (n):
        l[i]=int(l[i])
    return l
       
def maingame(l):
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
        print("Player 1 wins")
    else :
        print("Player 2 wins")



l=inputstack()
print("GENERAL INSTRUCTION")
print("Enter your moves as a_b where a is the heap no. starting from 0 and b is no. of elements you want to remove")
maingame(l)



