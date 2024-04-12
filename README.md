# Chess-Battleship
A version of the traditional Chess game written in python (pygame), with an additional twist: you can't see enemy positions, similar to Battleship in which you have to guess where your opponent placed their ships! Created for a UCI ICS 60 project, solely by me (Abhinav Uppala).

## How to play

The game follows the same rules as chess, with white going first and alternating. Additionally, checks, pins, captures, checkmate, etc. all work the same way as regular chess. The only difference is that you cannot see the opposing side's pieces on your turn.

In order to move a piece, click on the piece you wish to move, and then click one of the highlighted squares showing the legal moves that piece can make in this position (this could provide insight into enemy pieces blocking yours, a pin on your piece, etc.). Clicking the piece's current square will deselect it.

## How to run the game

In order to run the game, download the entire source code as a ZIP file from GitHub. You can run the executable through command prompt or manually clicking it, either way works. IMPORTANT: make sure the chess_sprites directory with the saved images are in the same directory as the executable, otherwise it will crash. The game is meant to be played with 2 players locally, with swapping the computer after each turn (so you can't see opposing side's pieces).

Alternatively, you could run it through python by running main.py, ensuring view.py and chess_sprites are in the same directory. Additionally, you will need to pip install chess and pip install pygame in order for the code to function.
