# Part 1: Raichu

### Objective:
Create an AI giving the next ideal move in checkers to beat the opponent.

### Formulation of each problem:

##### Choosing valid states for each pawn - 
Various counters were used so as to not check the whole board. These counters iteratively checks only for those positions and not referencing the entire board.

For Pichu, counters wc1 and wc2 are used for left and right moves for the white pawn and counters bc1 and bc2 are used for the black pawn.
For Pikachu, counters i, j and k are used for front, left and right movements.
For Raichu, counters dlu,dru,drd,dld are used for diagonal moves - left up,right up,right down,left down  and counters fu,fd,fr,fl are used for front, down, right and left moves.

##### Checking if move is possible -
Various conditions using if statements under while loop are used to iteratively identify valid spaces and immediately discard them if not true.

##### Updating the states after each move - 
A dictionary is used to update and keep track of prior moves. It also holds the score, positions of the pawns and the board. The dictionary is called and updated with the new move, score and the board is updated at each level.

##### Deciding best moves for both sides - 
Implemented the minimax algorithm for a certain depth which looks for the best moves for our AI and the opponent and recursively updates the best move to be considered based on the depth.

### Description of the program:
The program first takes in the board, player, size of N*N board and the defined timelimit. It then gets the current board attributes based through the get_position function. The respected metrics are then passed to the minimax algorithm which iteratively calls the max or min function based on the player move to be decided.
At each iterative call, the current board attributes are called and passed into the get_new_position which gives the successors for the current board. Based on the depth and player move, it then gets the largest or smallest score and returns the board.
Finally, after each check, it returns the best possible move for the given player and returns a board string.

### Problems faced and Design decisions:
##### Problems faced -
On designing the valid moves, many problems surfaced regarding the logic for the counters as all the conditions were not considered and going into an infinite loop. Also, on returning the next move, the board returned contained ideal move for the opponent too. These issues were checked one by one through print statements and got resolved.

##### Design decisions - 
A heuristic is created to incentivise the killing of the opponent and keep moving forward. This decision was made so the opponent's pawns reduces and if incentivised to move forward, it evolves into Raichu and has many more better moves it can make. 
 
 
 
 
# Part 2: The Game of Quintris

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
 
 



## Part 3: Truth Be Told
### Problem Overview

Text classification involves classifying text to a particular class to solve some real-time problem such as fake news detection, spam mail detection and other Natual Language Processing (NLP) problems. This problem of classifying hotel reviews as deceptive or truthful falls under this category of problems. One of the most simplest and basic methods of performing text classification is by using Naive Bayes. 

The given problem contains two datasets train and test. Both contain labels (deceptive/ truthful) and the reviews. The train dataset is used to calculate the needed values to train the data with Naive Bayes and the test data is used to test the model and then finally calculate the accuracy. 

### Approach 

We start solving the problem by loading the train dataset. the data is stores in a form of a dictionary. The dictionary contains the labels, objects which is the reviews and classes(deceptive and truthful). 

The objects in the dictionary which are reviews is pre-processed to remove the special characters, extra white spaces in the reviews and change the text into lower case. Then the reviews are split into words and stored in a seperate dictionary according to the class it belongs to. (The reason for this is explained below.)

According to Naive Bayes

<a href="https://www.codecogs.com/eqnedit.php?latex=P(A|B)&space;=&space;\frac{P(B|A)P(A)}{P(B)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(A|B)&space;=&space;\frac{P(B|A)P(A)}{P(B)}" title="P(A|B) = \frac{P(B|A)P(A)}{P(B)}" /></a> 
where A and B are events. 

For this problem we need to find out what is the probability of class **deceptive** given a review and the probability of class **truthful** given a review. 

<a href="https://www.codecogs.com/eqnedit.php?latex=P(deceptive|review)&space;=&space;\frac{P(review|deceptive)P(deceptive)}{P(review)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(deceptive|review)&space;=&space;\frac{P(review|deceptive)P(deceptive)}{P(review)}" title="P(deceptive|review) = \frac{P(review|deceptive)P(deceptive)}{P(review)}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=P(truthful|review)&space;=&space;\frac{P(review|truthful)P(truthful)}{P(review)}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(truthful|review)&space;=&space;\frac{P(review|truthful)P(truthful)}{P(review)}" title="P(truthful|review) = \frac{P(review|truthful)P(truthful)}{P(review)}" /></a>

Since in this problem the denominators are the same they can be ignored.

To calculate the probability of deceptive and truthful:

<a href="https://www.codecogs.com/eqnedit.php?latex=P(deceptive)&space;=&space;\frac{No.&space;of&space;reviews&space;in&space;deceptive}{Total&space;No.&space;of&space;reviews}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(deceptive)&space;=&space;\frac{No.&space;of&space;reviews&space;in&space;deceptive}{Total&space;No.&space;of&space;reviews}" title="P(deceptive) = \frac{No. of reviews in deceptive}{Total No. of reviews}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=P(truthful)&space;=&space;\frac{No.&space;of&space;reviews&space;in&space;truthful}{Total&space;No.&space;of&space;reviews}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(truthful)&space;=&space;\frac{No.&space;of&space;reviews&space;in&space;truthful}{Total&space;No.&space;of&space;reviews}" title="P(truthful) = \frac{No. of reviews in truthful}{Total No. of reviews}" /></a>

To calculate the probability of review given a class:

<a href="https://www.codecogs.com/eqnedit.php?latex=P(review|class)&space;=&space;\frac{No.&space;of&space;times&space;review&space;appears&space;in&space;that&space;class}{Total&space;No.&space;of&space;reviews&space;in&space;that&space;class}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(review|class)&space;=&space;\frac{No.&space;of&space;times&space;review&space;appears&space;in&space;that&space;class}{Total&space;No.&space;of&space;reviews&space;in&space;that&space;class}" title="P(review|class) = \frac{No. of times review appears in that class}{Total No. of reviews in that class}" /></a>

The above cannot be calculates **as the number of times the review appears in that class can be zero** (a particular review may not repeat). Therefore, we modify the problem by **splitting the review into words**. 

Now:

<a href="https://www.codecogs.com/eqnedit.php?latex=P(deceptive|w_1,&space;w_2...w_n)&space;=&space;P(w_1|deceptive)P(w_2|deceptive)...P(w_n|deceptive)&space;P(deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(deceptive|w_1,&space;w_2...w_n)&space;=&space;P(w_1|deceptive)P(w_2|deceptive)...P(w_n|deceptive)&space;P(deceptive)" title="P(deceptive|w_1, w_2...w_n) = P(w_1|deceptive)P(w_2|deceptive)...P(w_n|deceptive) P(deceptive)" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=P(truthful|w_1,&space;w_2...w_n)&space;=&space;P(w_1|truthful)P(w_2|truthful)...P(w_n|truthful)&space;P(deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(truthful|w_1,&space;w_2...w_n)&space;=&space;P(w_1|truthful)P(w_2|truthful)...P(w_n|truthful)&space;P(deceptive)" title="P(truthful|w_1, w_2...w_n) = P(w_1|truthful)P(w_2|truthful)...P(w_n|truthful) P(deceptive)" /></a>

Probability of deceptive  <a href="https://www.codecogs.com/eqnedit.php?latex=P(deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(deceptive)" title="P(deceptive)" /></a> and probability of truthful <a href="https://www.codecogs.com/eqnedit.php?latex=P(truthful)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(truthful)" title="P(truthful)" /></a> is calculated by

```
prior_dec = total_deceptive / (total_deceptive+total_truthful)
prior_tru = total_truthful / (total_deceptive+total_truthful)
```
In a dictionary frequency of each word appearing in deceptive reviews and truthful reviews respectfully is stored where the key of the dictionary is the word and the value is the frequency. 

Therefore, now to calculate the liklihood of the word in the given class: 

<a href="https://www.codecogs.com/eqnedit.php?latex=P(w_{i}|deceptive)=&space;\frac{No.&space;of&space;times&space;word&space;appears&space;in&space;deceptive}{Total&space;No.&space;of&space;deceptive&space;words}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(w_{i}|deceptive)=&space;\frac{No.&space;of&space;times&space;word&space;appears&space;in&space;deceptive}{Total&space;No.&space;of&space;deceptive&space;words}" title="P(w_{i}|deceptive)= \frac{No. of times word appears in deceptive}{Total No. of words in deceptive}" /></a>

<a href="https://www.codecogs.com/eqnedit.php?latex=P(w_{i}|truthful)=&space;\frac{No.&space;of&space;times&space;word&space;appears&space;in&space;truthful}{Total&space;No.&space;of&space;words&space;in&space;truthful}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(w_{i}|truthful)=&space;\frac{No.&space;of&space;times&space;word&space;appears&space;in&space;truthful}{Total&space;No.&space;of&space;words&space;in&space;truthful}" title="P(w_{i}|truthful)= \frac{No. of times word appears in truthful}{Total No. of words in truthful}" /></a>

```
    #likelihood of words belonging to deceptive 
    for key,value in deceptive_dict.items():
        deceptive_likelihood[key] = (value + 1)/(n_deceptive + v_deceptive)
        
    #likelihood of words belongging to truthful  
    for key,value in truthful_dict.items():
        truthful_likelihood[key] = (value + 1)/(n_truthful + v_truthful)
```        
 Now we have derived all the values from the training data so we load the test data and perform the pre-processing as done for the train data (removing special characters, extra white spaces and converting to lower case) and the sentences are split into words and stores in a dictionary. 
 
 Now for testing we take each word and check if they belong to either deceptive or/and truthful. 
 This is equivalent to computing
 
 <a href="https://www.codecogs.com/eqnedit.php?latex=P(deceptive)P(w_i|deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(deceptive)P(w_i|deceptive)" title="P(deceptive)P(w_i|deceptive)" /></a>
 
 and 
 
 <a href="https://www.codecogs.com/eqnedit.php?latex=P(truthful)P(w_i|truthful)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?P(truthful)P(w_i|truthful)" title="P(truthful)P(w_i|truthful)" /></a>
 
 instead we calculate by taking log
 
 <a href="https://www.codecogs.com/eqnedit.php?latex=log&space;P(deceptive)&plus;&space;log&space;P(w_i|deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log&space;P(deceptive)&plus;&space;log&space;P(w_i|deceptive)" title="log P(deceptive)+ log P(w_i|deceptive)" /></a>
 
 and
 
 <a href="https://www.codecogs.com/eqnedit.php?latex=log&space;P(truthful)&plus;&space;log&space;P(w_i|truthful)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log&space;P(truthful)&plus;&space;log&space;P(w_i|truthful)" title="log P(truthful)+ log P(w_i|truthful)" /></a>
 
 ```
 weight_deceptive = math.log(prior_dec) #log value of P(deceptive)

 weight_truthful = math.log(prior_tru)  #log value of P(truthful)
 
 #for each word in the list if the word is present in the deceptive likelihood dictionary then calculate the score by
        #adding the log value of P(deceptive) and log value of the liklihood for that word stored in deceptive_likelihood dictionary

        for each_word in each_line:

            if each_word in deceptive_likelihood.keys(): 
                weight_deceptive = weight_deceptive + math.log(deceptive_likelihood[each_word])

            #if the word is present in the truthful likelihood dictionary then calculate the score by
            #adding the log value of P(truthful) and log value of the liklihood for that word stored in truthful_likelihood dictionary    

            if each_word in truthful_likelihood.keys():
                weight_truthful = weight_truthful + math.log(truthful_likelihood[each_word])
```
Now we compare the two scores. 
If <a href="https://www.codecogs.com/eqnedit.php?latex=log&space;P(deceptive)&plus;&space;log&space;P(w_i|deceptive)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log&space;P(deceptive)&plus;&space;log&space;P(w_i|deceptive)" title="log P(deceptive)+ log P(w_i|deceptive)" /></a>
is **greater than** <a href="https://www.codecogs.com/eqnedit.php?latex=log&space;P(truthful)&plus;&space;log&space;P(w_i|truthful)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?log&space;P(truthful)&plus;&space;log&space;P(w_i|truthful)" title="log P(truthful)+ log P(w_i|truthful)" /></a> 
***then it belongs to the deceptive class else it belongs to truthful class.***

```
        if(weight_deceptive > weight_truthful):

            test_label.append(test_data["classes"][0])
        else:

            test_label.append(test_data["classes"][1])

    return test_label
    
```    
