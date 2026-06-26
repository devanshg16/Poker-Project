# Poker-Project
An easy way to know your win probability in a poker round. Simply input your hand and the number of players. The code will simulate random cards for the other players and for the board.

## Version 1 (requires Pydealer and Treys libraries)
This code is very simple, outsources most of the heavy lifting to the **Pydealer** and **Treys** libraries. Simply download the V1 file and run it.

## Version 2 (requires Pydealer library)
Much more of the work is now done by my code, which has eliminated the need for the **Treys** library. This code is run through the main V2 file. 3 additional files are utilised for this, which are the 2 CSV files and the evaluate_scores python file. The 2 CSV files act as precomputed lookup tables for the strength of each hand.
*Note: an additional file (fill_tables.py) has been included as part of V2. This code is NOT necessary, and was used to produce the 2 CSV files.*
