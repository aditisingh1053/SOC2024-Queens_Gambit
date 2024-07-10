import json
mate_in_2 = json.load(open('mate_in_2.json'))

# import matplotlib.pyplot as plt
# import numpy as np
from tqdm import tqdm
import time
# import chess
import chess.svg
# from engine import My_Engine
# from new_engine import Engine
# from try_2 import My_Engine
# from my_final_engine import My_Engine
from something import My_Engine
# from justwhy import My_Engine

# data = np.zeros(351)
start = time.time()
correct = 0
for i, puzzle in enumerate(tqdm(mate_in_2)):
    # start_ = time.time()
    engine = My_Engine(puzzle)
    result = engine.puzzle_solving(3)
    if engine.board.is_checkmate():
        correct += 1
    else:
        print(puzzle)
    # data[i] = time.time() - start_
        # print(chess.svg.board(engine.board, lastmove=engine.board.peek()))
print(f'Time: {time.time() - start} s')
print(f'Correct: {correct}/{len(mate_in_2)}')
# plt.plot(np.arange(351), data)
# plt.show()