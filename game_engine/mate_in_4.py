import json
mate_in_4 = json.load(open('mate_in_4.json'))

from tqdm import tqdm
# import matplotlib.pyplot as plt
# import numpy as np
import time
# import chess.svg
from my_final_engine import My_Engine

start = time.time()
correct = 0
# data = np.zeros(489)
for puzzle in tqdm(list(mate_in_4.keys())):
    # start_ = time.time()
    engine = My_Engine(puzzle)
    result = engine.puzzle_solving(7)
    if engine.board.is_checkmate():
        correct += 1
    else:
        print(puzzle)
    # data[i] = time.time() - start_
        # print(chess.svg.board(engine.board, lastmove=engine.board.peek()))
print(f'Time: {time.time() - start} s')
print(f'Correct: {correct}/{len(mate_in_4)}')
# plt.plot(np.arange(489), data)
# plt.show()