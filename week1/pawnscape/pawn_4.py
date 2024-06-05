def isvalid_move(l,moving,other,dire):
    move=[]
    for ele in l:
        print(ele)
    print("")
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

def computerPlayforwhite(l):
    movelist=isvalid_move(l,'W','B',-1)
    if movelist==[]:
        m=["Game is draw"]
        return m
    else:
        for move in movelist:
            newl=l.copy()
            ilovelist=[]
            c=moveme(newl,move,'W')
            print(c)
            if c==1:
                m=["White"]
                m.append(move)
                ilovelist.append(m)            
            else:
                m=computerplayforblack(newl)
                m.append(move)
                ilovelist.append(m)
        return ilovelist




def computerplayforblack(l):
    movelist=isvalid_move(l,'B','W',1)
    if movelist==[]:
        m=["Game is draw"]
        return m
    else:
        for move in movelist:
            newl=l.copy()
            ilovelist=[]
            c=moveme(newl,move,'B')
            if c==-1:
                m=["Black"]
                m.append(move)
                ilovelist.append(m)            
            else:
                m=computerPlayforwhite(newl)
                m.append(move)
                ilovelist.append(m)
        return ilovelist

def moveme(l,moveList,moving):
    l[moveList[2]][moveList[3]]="*"
    l[moveList[0]][moveList[1]]=moving
    if moving=='W' and moveList[0]==0 :
        return 1
    elif moving=='B' and moveList[0]==len(l)-1 :
        return -1
    else :
        return 0



def mainplay():
    l=create_initial_grid(4,'B','W')
    c=computerPlayforwhite(l)
    print(c)

mainplay()