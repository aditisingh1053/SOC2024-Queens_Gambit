#include "chess.hpp"

using namespace chess;
using namespace std;

int main () { 
    Board board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");


    for (int i=0; i<64; i++){
        if (i%8==0){
            cout<<endl;
        }
        cout<<Square(i)<<" ";
        
    }
    cout<<endl;
    return 0;
}