# The Game of Quintris

### Objective:
To make the AI play the Quintris game by scoring the highest possible score.

### Formulation of each problem:

#### Choosing the next best move:

Make the current piece to move in the all possible combinations and place it in the all possible state. Now as we know the next move, for each possible state of the first piece we place the all the combinations of the second piece to get the score for all the possible combination of the current piece and the next piece.

#### Calculating the scores for each move:

For each combination of the current and next piece we find the following:

1) Aggregate height :
       The sum of height of the pieces in each column of the board. Here the weight is initiated such a way that with increase in level, the score will be multiplied by itself by the level of the column.
       
2) Complete line:
       If a lines gets completely filled up by the pieces then the score is the vanishing line. 
       
3) Bumps in the board:
       For the bumps we calculate the summation of the difference in the absolute value of the height of pieces in each column.
   
4) Holes in the board:
       A hole in the board is such that if no piece covers a particular index on the board and we have a piece on top of it, then we calculate the summation of all such holes.
       
       
### Description of the program

For all the combination of the current piece moves on the board, the score is calculated with respect to the next piece. The maximum score is chosen wth having a positive "complete line" weight and negative "Aggregate height" , "Bumps in the board" , "Holes in the board" weights. 


### Problems faced and Design decisions:
##### Problems faced -
In the computer animated function it always was going to infinite loop and hence I've implemented the code in the computer simple version.

##### Design decisions - 
First I tried using the genetic algorithm, but updating the weights became complex and followed the lines of expectiminimax to find the possible successors and also the best move.
  
