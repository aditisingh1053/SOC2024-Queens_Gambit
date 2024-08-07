#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <memory>
#include "chess.hpp"
#include <cmath>
#include <unordered_map>

using namespace chess;
using namespace std;

class Engine {
public:
    Board board;
    std::unordered_map<uint64_t, std::pair<float, int>> transpositionTable;
    Engine(const std::string& fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        : board(fen) {}

    void setFen(const std::string& fen) {
        board = Board(fen);
    }


    vector<Move> getLegalMoves() {
        vector<Move> legalMoves;
        Movelist moves;
        movegen::legalmoves(moves, board);
        for (const auto& move : moves) {
            legalMoves.push_back(move);
        }
        return legalMoves;
    }

    vector<Move> getOrderedMoves() {
        auto moves = getLegalMoves();
        vector<pair<float, Move>> orderedMoves;
        for (const auto& move : moves) {
            board.makeMove(move);
            if (board.getHalfMoveDrawType().first == GameResultReason::CHECKMATE) {
                board.unmakeMove(move);
                return {move};
            } else if (board.inCheck()) {
                if (board.sideToMove() == Color("w")) {
                    orderedMoves.push_back({50,move});
                } else {
                    orderedMoves.push_back({-50,move});
                }
            } else {
                 if (board.sideToMove() == Color("w")) {
                    orderedMoves.push_back({evaluate(),move});
                } else {
                    orderedMoves.push_back({-evaluate(),move});
                }
            }
            float score = evaluate();
            board.unmakeMove(move);
        }
        sort(orderedMoves.begin(), orderedMoves.end(), [](const auto& a, const auto& b) {
            return a.first > b.first;
        });
        vector<Move> ordered;
        for (const auto& move : orderedMoves) {
            ordered.push_back(move.second);
        }
        return ordered;
    }

    void makeMove(const Move& move) {
        board.makeMove(move);
    }

    void undoMove(const Move& move) {
        board.unmakeMove(move);
    }

    float evaluate() {

        float score = 0;
        int white_pawns = 0, black_pawns = 0;
        vector<int> white_pawns_loc; vector<int> black_pawns_loc;
        int white_pieces = 0, black_pieces = 0;
        float white_eval = 0, black_eval = 0;
        int white_king = 0, black_king = 0;
        for (int i=0; i<64; i++) {
            int piece = board.at(Square(i));
            // cout<<piece<<endl;
            if (piece != 12) {
                if (piece < 6) {
                    white_pieces++;
                    switch (piece)
                    {
                    case 0:
                        white_pawns_loc.push_back(i);
                        white_pawns++;
                        break;
                    case 1:
                        white_eval += 3 + (float) knights_util[i]/100;
                        break;
                    case 2:
                        white_eval += 3.2 + (float) bishops_util[i]/100;
                        break;
                    case 3:
                        white_eval += 5 + (float) rooks_util[i]/100;
                        break;
                    case 4:
                        white_eval += 9 + (float) queens_util[i]/100;
                        break;
                    case 5:
                        white_king = i;
                        break;
                    default:
                        break;
                    }
                } else {
                    black_pieces++;
                    switch (piece)
                    {
                    case 6:
                        black_pawns_loc.push_back(63-i);
                        black_pawns++;
                        break;
                    case 7:
                        black_eval += 3 + (float) knights_util[63-i]/100;
                        break;
                    case 8:

                        black_eval += 3.2 + (float) bishops_util[63-i]/100;
                        break;
                    case 9:

                        black_eval += 5 + (float) rooks_util[63-i]/100;
                        break;

                        black_eval += 9 + (float) queens_util[63-i]/100;
                        break;
                    case 11:
                        black_king = 63-i;
                        break;
                    default:
                        break;
                    }
                }
            }
        }
        if (white_pieces + black_pieces > 8) {
            white_eval += (float) kings_start_util[white_king]/100;
            black_eval += (float) kings_start_util[black_king]/100;
        } else {
            white_eval += (float) kings_end_util[white_king]/100;
            black_eval += (float) kings_end_util[black_king]/100;
        }
        if (white_pieces + black_pieces > 8){
            for (int i=0; i<white_pawns; i++){
                white_eval+=1+(float)pawns_start_util[white_pawns_loc[i]]/100;
            }
            for (int i=0; i<white_pawns; i++){
                black_eval+=1+(float)pawns_start_util[black_pawns_loc[i]]/100;
            }

        }
        else{
            for (int i=0; i<white_pawns; i++){
                white_eval+=1+(float)pawns_end_util[white_pawns_loc[i]]/100;
            }
            for (int i=0; i<white_pawns; i++){
                black_eval+=1+(float)pawns_end_util[black_pawns_loc[i]]/100;
            }
        }

        score = white_eval - black_eval;
        return score;
    }

    string getBestMoveforwhite(int maxDepth = 6) {
        alphaBetaPruningforwhite(maxDepth, -INFINITY, INFINITY);
        return alphaBetaPruningforwhite(maxDepth, -INFINITY, INFINITY).second;
    }
    
    vector<float> pawns_start_util = {
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        5.0, 10.0, 10.0, -20.0, -20.0, 10.0, 10.0, 5.0, 
        5.0, -5.0, -10.0, 0.0, 0.0, -10.0, -5.0, 5.0, 
        0.0, 0.0, 0.0, 20.0, 20.0, 0.0, 0.0, 0.0, 
        5.0, 5.0, 10.0, 25.0, 25.0, 10.0, 5.0, 5.0, 
        10.0, 10.0, 20.0, 30.0, 30.0, 20.0, 10.0, 10.0, 
        50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    };

    vector<float> pawns_end_util={
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 
        10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 
        20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 
        30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 30.0, 
        50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 
        80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 80.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  
    };
    
    vector<float> knights_util = {
        -50.0, -40.0, -30.0, -30.0, -30.0, -30.0, -40.0, -50.0, 
        -40.0, -20.0, 0.0, 5.0, 5.0, 0.0, -20.0, -40.0, 
        -30.0, 5.0, 10.0, 15.0, 15.0, 10.0, 5.0, -30.0, 
        -30.0, 0.0, 15.0, 20.0, 20.0, 15.0, 0.0, -30.0, 
        -30.0, 5.0, 15.0, 20.0, 20.0, 15.0, 5.0, -30.0, 
        -30.0, 0.0, 10.0, 15.0, 15.0, 10.0, 0.0, -30.0, 
        -40.0, -20.0, 0.0, 0.0, 0.0, 0.0, -20.0, -40.0, 
        -50.0, -40.0, -30.0, -30.0, -30.0, -30.0, -40.0, -50.0, 
    };
    
    vector<float> bishops_util = {
        -20.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -20.0, 
        -10.0, 5.0, 0.0, 0.0, 0.0, 0.0, 5.0, -10.0, 
        -10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, -10.0, 
        -10.0, 0.0, 10.0, 10.0, 10.0, 10.0, 0.0, -10.0, 
        -10.0, 5.0, 5.0, 10.0, 10.0, 5.0, 5.0, -10.0, 
        -10.0, 0.0, 5.0, 10.0, 10.0, 5.0, 0.0, -10.0, 
        -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -10.0, 
        -20.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -20.0, 
    };
    
    vector<float> rooks_util = {
        0.0, 0.0, 0.0, 5.0, 5.0, 0.0, 0.0, 0.0, 
        -5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, 
        -5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, 
        -5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, 
        -5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, 
        -5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -5.0, 
        5.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 5.0, 
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
    };
    
    vector<float> queens_util = {
        -20.0, -10.0, -10.0, -5.0, -5.0, -10.0, -10.0, -20.0, 
        -10.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, -10.0, 
        -10.0, 5.0, 5.0, 5.0, 5.0, 5.0, 0.0, -10.0, 
        0.0, 0.0, 5.0, 5.0, 5.0, 5.0, 0.0, -5.0, 
        -5.0, 0.0, 5.0, 5.0, 5.0, 5.0, 0.0, -5.0, 
        -10.0, 0.0, 5.0, 5.0, 5.0, 5.0, 0.0, -10.0, 
        -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -10.0, 
        -20.0, -10.0, -10.0, -5.0, -5.0, -10.0, -10.0, -20.0, 
    };

    vector<float> kings_start_util = {
        20.0, 30.0, 10.0, 0.0, 0.0, 10.0, 30.0, 20.0, 
        20.0, 20.0, -5.0, -5.0, -5.0, -5.0, 20.0, 20.0, 
        -10.0, -20.0, -20.0, -20.0, -20.0, -20.0, -20.0, -10.0, 
        -20.0, -30.0, -30.0, -40.0, -40.0, -30.0, -30.0, -20.0, 
        -30.0, -40.0, -40.0, -50.0, -50.0, -40.0, -40.0, -30.0, 
        -40.0, -50.0, -50.0, -60.0, -60.0, -50.0, -50.0, -40.0, 
        -60.0, -60.0, -60.0, -60.0, -60.0, -60.0, -60.0, -60.0, 
        -80.0, -70.0, -70.0, -70.0, -70.0, -70.0, -70.0, -80.0, 
    };

    vector<float> kings_end_util = {
        -50.0, -30.0, -30.0, -30.0, -30.0, -30.0, -30.0, -50.0, 
        -30.0, -25.0, 0.0, 0.0, 0.0, 0.0, -25.0, -30.0, 
        -25.0, -20.0, 20.0, 25.0, 25.0, 20.0, -20.0, -25.0, 
        -20.0, -15.0, 30.0, 40.0, 40.0, 30.0, -15.0, -20.0, 
        -15.0, -10.0, 35.0, 45.0, 45.0, 35.0, -10.0, -15.0, 
        -10.0, -5.0, 20.0, 30.0, 30.0, 20.0, -5.0, -10.0, 
        -5.0, 0.0, 5.0, 5.0, 5.0, 5.0, 0.0, -5.0, 
        -20.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -20.0, 
    };

    pair<float, string> alphaBetaPruningforwhite(int depth, float alpha, float beta) {

        
        if (board.getHalfMoveDrawType().first == GameResultReason::CHECKMATE) {
            if(board.sideToMove() == Color("w")) {
                return {-INFINITY, ""}; 
            } else {
                return {INFINITY, ""};
            }
        }
        else if (board.isGameOver().first != GameResultReason::NONE) {
            return {0, ""};
        }
        if (depth == 0) {
            return {evaluate(), ""};
        }
        auto moves = getLegalMoves();
        string bestMove = uci::moveToUci(moves[0]);
        for (const auto& move : moves) {
            board.makeMove(move);
            float score;
            if (transpositionTable.find(board.hash()) != transpositionTable.end()) {
                std::pair<float, int> transposition = transpositionTable[board.hash()];
                if (transposition.second >= depth) {
                    score = transposition.first;
                } else {
                    score = alphaBetaPruningforwhite(depth - 1, alpha, beta).first;
                }
            } else {
                score = alphaBetaPruningforwhite(depth - 1, alpha, beta).first;
            }

            board.unmakeMove(move);
            if (board.sideToMove() == Color("w")) {
                if (score > alpha) {
                    alpha = score;
                    bestMove = uci::moveToUci(move);
                }
            } else {
                if (score < beta) {
                    beta = score;
                    bestMove = uci::moveToUci(move);
                }
            }
            if (alpha >= beta) {
                break;
            }

        }

        return {board.sideToMove() == Color("w") ? alpha : beta, bestMove};
    }

};

int main() {
    Engine engine = Engine();
    int move_count = 0;
    while(engine.board.isGameOver().first == GameResultReason::NONE) {
        //  cout << engine.board << '\n';
        if (move_count % 2 == 0) {
;
            auto mymove=engine.getBestMoveforwhite(5);
            Move move = uci::uciToMove(engine.board, mymove);
            cout << "White: " << uci::moveToUci(move) << endl;
           
            engine.board.makeMove(move);
        } else {
            string move;
            cin >> move;
            Move move_ = uci::uciToMove(engine.board, move);
            engine.board.makeMove(move_);
            cout << "Black: " << uci::moveToUci(move_) << endl;
        }

        move_count++;
        cout << move_count << '\n';    }
    cout << "Best Move: " << engine.getBestMoveforwhite(5) << endl;
    return 0;
}