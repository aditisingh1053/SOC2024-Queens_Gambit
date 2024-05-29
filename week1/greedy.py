print("Enter the size of the list")
n=int(input())
print("Enter the elements of the list")
l=input()
l=l.split()
if len(l)!=n:
    print("Invalid input try again")
    exit()
for i in range (n):
    l[i]=int(l[i])

sc1=0
sc2=0
c=0
for i in range (n):
    if c==0:
        c=1
        if l[0]>=l[-1]:
            sc1=sc1+l[0]
            l.pop(0)
        else:
            sc1=sc1+l[-1]
            l.pop()
    else:
        c=0
        if l[0]>=l[-1]:
            sc2=sc2+l[0]
            l.pop(0)
        else:
            sc2=sc2+l[-1]
            l.pop()
    print("Standing of game",i+1,"th move")
    print("Score of player1",sc1)
    print("score of player2",sc2)
    print("list remaining",l)

if sc1>sc2:
    print("Player 1 wins")
elif sc1<sc2:
    print("Player 2 wins")
else :
    print("Game is a tie")

            

