# Greedy or not
## Overview of the game
This is a simple game in which there is a list of n numbers and two players move alternately. On each
move, a player removes either the first or last number from the list, and their
score increases by that number and that number gets deleted. Both players try
to maximize their scores and play optimally. A certain player wins if their score
is strictly greater than the score of the other person.

## My implementation overview
Initially for a long time I believed that optimal play for a person is that he decides between both the ends and pick the number which is greater. I wrote the code for this in [greedy_useless](greedy_useless.py). Eventually I realized that this is not optimal and then I implemented the recursive strategy. In this there is a function bestmove which returns a list which is the bestmove and a projected score and this the score is recursively calculated. And yes I spent a lot of time debugging the function 🤯 because of a silly mistake . My final code is in [greedy_working](greedy_working.py)

I eventually realized that the code is taking too much time for large arrays mainly because of it's exponential time complexity. I understood the process of implementing dynamic programming in this but was too lazy to do that so left it.

