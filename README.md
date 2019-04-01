# 4511W

## How to run qubic.py
It can be run with two arguments to play a single game.  
$ python3 qubic.py player1 player2
    
Or it can be run with 3 arguments to run many games. Should not use a human player if doing so.  
$ python3 qubic.py player1 player2 iterations
        
### Arguments
player1 - specifies the mode for player 1. 0: human player, 1: random player, 2: defensive AI, 3: aggressive AI.
        
player2 - same as player 1, but for the second player.
        
iterations - specifies the number of consecutive games to play.

### Examples 
$ python3 qubic.py 0 2, lets a human play against a defensive AI  
$ python3 qubic.py 3 2 10000, runs ten thousand games of aggressive vs defensive AI 
