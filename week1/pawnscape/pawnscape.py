def create_initial_grid(n,first,back):
    l=[]
    firstrow=[]
    lastrow=[]
    for i in range (n):
        firstrow.append(first)
    l.append(firstrow)
    for i in range (n-2):
        new=[]
        for j in range (n):
            new.append('*')
        l.append(new)
    for i in range (n):
        lastrow.append(back)
    l.append(lastrow)
    return l
    
def print_grid(l):
    print("")
    print("Current Board is")
    print("  ",end="")
    for j in range(len(l)):
        print(j,end=" ")
    print(end="\n")
    for i in range (len(l)):
        print(i,end=" ")
        for j in range (len(l)):
            print(l[i][j],end=" ")
        print(end="\n")
    print("")

def isvalid_move(l,moving,other,dire):
    move=[]
    for i in range (len(l)):
        for j in range (len(l)):
            if l[i][j]==moving:
                if l[i+dire][j]=='*':
                    move.append([i+dire,j,i,j])
                if j<len(l)-1 and l[i+dire][j+1]==other:
                    move.append([i+dire,j+1,i,j])
                if j>0 and l[i+dire][j-1]==other:
                    move.append([i+dire,j-1,i,j])
    return move

def inputMove(l,moving,other,dire):
    validmoves=isvalid_move(l,moving,other,dire)
    if validmoves==[]:
        print("Game is draw")
        return False

    if moving=='W':
        print("Enter your move as white")
    elif moving=='B':
        print("Enter your move as black")
    move=input()
    if len(move)!=4:
        print("Invalid move,try again, move length dhould be 4 digits")
        cnew=inputMove(l,moving,other,dire)
        return cnew
    moveList=[int(move[0]),int(move[1]),int(move[2]),int(move[3])]
    found=False
    tree=-1
    for ele in validmoves:
        c=0
        for i in range (4):
            if moveList[i]==ele[i]:
                c=c+1
        if c==4:
            found=True
            tree=i
            break
    
    if not found:
        print("Invalid move, try again")
        cnew=inputMove(l,moving,other,dire)
        return cnew
    else:
        l[moveList[2]][moveList[3]]="*"
        l[moveList[0]][moveList[1]]=moving
        print_grid(l)
        if moving=='W' and ((moveList[0]==0 and dire==-1) or (moveList[0]==len(l)-1 and dire==1)):
            print ("White wins")
            return False
        elif moving=='B' and ((moveList[0]==0 and dire==-1) or (moveList[0]==len(l)-1 and dire==1)):
            print("Black wins")
            return False
        else :
            return True
    


def maingame():
    print("Enter the size of the board(<=10)")
    size=int(input())
    print("Do you want to play as White(you get the priveledge to move first)\nReply with y/n")
    c=input()
    if c=='y':
        l=create_initial_grid(size,'B','W')
        print_grid(l)      
        move=True
        var=0
        while(move):
            if(var==0):
                move=inputMove(l,'W','B',-1)                
                var=1
            else:
                var=0
                move=inputMove(l,'B','W',1)                
    elif c=='n':
        l=create_initial_grid(size,'W','B')
        print_grid(l)
        move=True
        var=1
        while(move):
            if(var==0):
                move=inputMove(l,'W','B',1)
                var=1
            else:
                var=0
                move=inputMove(l,'B','W',-1)
    else:
        print("Invalid input! expected (y/n)")
        maingame()



maingame()
