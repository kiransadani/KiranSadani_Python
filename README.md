This is an assignment project based on position calculation process

Main file is:
get_EOD_positions.py

============================================================================================================
EXAMPLE: 
python get_EOD_positions.py Input_StartOfDay_Positions.txt 1537277231233_Input_Transactions.txt
============================================================================================================

get_EOD_positions.py: Implementation of Position Calculation Process.
It takes start of day positions and transaction files as input, apply transactions on positions 
based on transaction type (B/S) and account type (I/E), and computes end of day positions.

Please ensure that validationfunctions.py is present is same dir as this script

Process: Load start_position file in a dataframe and transaction file in another dataframe
Merge the above 2 frames, with all rows from transaction frame (left join on transaction frame)
Apply the get_delta() function so that we get the +/- quantities that need to be added/subtracted respectively
Aggregate Instrument,Account, AccountType over the above delta values
Add this delta to the Quantity column of start_position





