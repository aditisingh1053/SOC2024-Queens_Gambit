def best_move(l,st,end,sign):
    if end==st:
        score=sign*l[st]
        # print("cal",st,l[st])
        # print("returned basic",[score,st])
        return [score,st]
    else :
        # print("calling",st,end-1,sign*-1,l[st:end])
        score1=sign*l[end]+best_move(l,st,end-1,sign*-1)[0]
        # print("calling",st+1,end,sign*-1,l[st+1:end+1])
        score2=sign*l[st]+best_move(l,st+1,end,sign*-1)[0]
        # print("Scores are ",score1,score2)
        if(score1*sign>=score2*sign):
            # print("returned",[score1,end])
            return [score1,end]
        else:
            # print("returned",[score2,st])
            return [score2,st]
        

    


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
        good=best_move(l,0,len(l)-1,1)
        sc1+=l[good[1]]
        l.pop(good[1])
        c=1
    else:
        c=0
        good=best_move(l,0,len(l)-1,1)
        sc2+=l[good[1]]
        l.pop(good[1])

    print("Standing of game at move no.",i+1)
    # print("Score of player1",sc1)
    # print("score of player2",sc2)
    # print("list remaining",l)

if sc1>sc2:
    print("Player 1 wins")
elif sc1<sc2:
    print("Player 2 wins")
else :
    print("It's a draw")