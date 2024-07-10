# Game of NIM
## Basic overview
The number of piles, i.e., the rows in the image, of the game is finite, and
each pile contains a finite number of matchsticks. These numbers can vary for
different instances of Nim. Each player, during her turn, chooses exactly one
pile, and removes any number of matchsticks from the pile she has selected
(she must remove at least one matchstick). The player who removes the last
matchstick wins the game.

## Theory behind the Game
I have my SOS on Game Theory due to which I have an idea on games like nim, Hackenbush and domineering. This past knowledge for nim carved my way easy for this.

So basically, for a particular Nim position we can calculate the bitwise XOR and if it is zero then the first player can force a win. If this is not the case then the second player can force a win.

The reason for the above logic lies in Bouton's Theorem which is basically from a Nim zero position any move will lead to only a non-zero Nim position while there exists a move from a non-zero nim position to a zero position. This is simple to prove and easy to visualize.

## My implementation
I first implemented a simple 2 player game in [nim_basic](nim_basic.py). After this I implemented the game with computer with the above strategy in [nim_final](nim_final.py) eventually realizing that I implemented the game in misere play(mainly because that the website link provided for playing also has misere play). So both the files above contain the gameplay in misere play wherein the person who picks the last looses the game.

 Followed by this I created the gameplay in normal play that ther person who plays last wins. The implementation is done in [nim_normal](nim_normal.py).