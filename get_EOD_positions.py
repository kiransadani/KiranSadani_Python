#!/opt/anaconda3/bin/python
''' 
get_EOD_positions.py: Implementation of Position Calculation Process.  
It takes start of day positions and transaction files as input, apply transactions on positions 
based on transaction type (B/S) and account type (I/E), and computes end of day positions.

Please ensure that validationfunctions.py is present is same dir as this script

Process: Load start_position file in a dataframe and transaction file in another dataframe
Merge the above 2 frames, with all rows from transaction frame (left join on transaction frame)
Apply the get_delta() function so that we get the +/- quantities that need to be added/subtracted respectively
Aggregate Instrument,Account, AccountType over the above delta values
Add this delta to the Quantity column of start_position

EXAMPLE : python get_EOD_positions.py Input_StartOfDay_Positions.txt 1537277231233_Input_Transactions.txt

'''
__author__  = "Kiran Sadani"
__version__ = "2.7.6"
__email__ = "kirans1312@gmail.com"


import pandas as pd
import sys
import os
import json
from validationfunctions import *

pd.set_option('display.expand_frame_repr', False)

# Main function to calculate the position
def get_delta(x):
  if(x['TransactionType']=='B' and x['AccountType']=='E'):
    return int( '+' + str(x['TransactionQuantity']) )
  elif(x['TransactionType']=='B' and x['AccountType']=='I'):
    return int( '-' + str(x['TransactionQuantity']) )
  elif(x['TransactionType']=='S' and x['AccountType']=='E'):
    return int( '-' + str(x['TransactionQuantity']) )
  elif(x['TransactionType']=='S' and x['AccountType']=='I'):
    return int( '+' + str(x['TransactionQuantity']) )
    

# Validation1 : Check Input Exists and File Exists
if ( input_validation(sys.argv) == False):
  sys.exit(0)

position_file = sys.argv[1]
transaction_file = sys.argv[2]

# Validation2 : Check if file is a proper json file
if( json_file_validation( transaction_file ) == False ) :
  sys.exit(0)

# Load data, on loading validate the data
start_position_df = pd.read_csv( position_file, sep="," )
transaction_df = pd.read_json( transaction_file )
expected_end_position_df = pd.read_csv('Expected_EndOfDay_Positions.txt', sep=",")

# Validation3 : Validate the column names. Check if required columns are present
if( column_name_validator( start_position_df.columns, 'start_position' ) == False or column_name_validator( transaction_df.columns, 'transaction' ) == False):
  sys.exit(0)

# Validation4 : Check AccountType and TransactionType values
if( account_type_validation(start_position_df)==False or transaction_type_validation(transaction_df)==False ):
  sys.exit(0)

# Validation5 : Check if a valid Instrument is involved in Transaction
if ( un_initiated_column_validation( start_position_df, transaction_df, 'Instrument') == False ):
  sys.exit(0)

# Getting start position data for every row of transaction, hence left join on transaction_df
operation_df = pd.merge(transaction_df,start_position_df,on='Instrument',how='left')

# Apply get_delta() to return result in Delta (where Delta is the quantity added or subtracted with +/- sign)
operation_df = operation_df.assign(Delta=operation_df.apply(get_delta, axis=1))

# Aggregating all transactions: Once you have all rows with add/subtract quantities, add them up(Minus sign will take care of reduction).
end_position_df = operation_df.groupby(['Instrument','Account','AccountType'],as_index=False).agg({'Delta':'sum'})

# You need start_position data in groupby dataframe to add delta to Quantity
end_position_df = pd.merge(start_position_df, end_position_df, on=['Instrument','Account','AccountType'],how='left')

# For those rows of start_position_df where transaction did not happen and joining resulted into Nan column values
end_position_df = end_position_df.fillna(0)

# Final Quantity
end_position_df['Quantity'] = end_position_df['Quantity'] + end_position_df['Delta']

# Typecasting as python 2.7 is converting INT to float in Delta column during join operation
end_position_df[['Delta','Quantity']] = end_position_df[['Delta','Quantity']].astype(int)

# Sorting values so that comparing is simpler with expected one
end_position_df = end_position_df.sort_values(by='Instrument')
print('---------- Calculated ----------')
print(end_position_df)

# Exporting to csv
end_position_df.to_csv('Calculated_EndOfDay_Positions.txt', sep=",", index=None)

# Sorting values so that comparing is simpler with calculated one
expected_end_position_df = expected_end_position_df.sort_values(by='Instrument')
print('---------- Expected -----------')
print(expected_end_position_df)

