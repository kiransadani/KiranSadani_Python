import os
import sys
import json

def input_validation(input):
  if( len(input) != 3 ):
    print('Check syntax\nSYNTAX : python ' + input[0] + ' <StartOfDay_Positions_File>  <Transaction_File>')
    print('EXAMPLE : python get_EOD_positions.py Input_StartOfDay_Positions.txt 1537277231233_Input_Transactions.txt')
    return False
  elif( os.path.isfile(input[1]) == False ):
    print('Start of day file (' + input[1] + ') does not exists')
    return False
  elif( os.path.isfile(input[2]) == False ):
    print('Transaction file (' + input[2] + ') does not exists')
    return False
  else:
    return True

def json_file_validation( json_file ):
  try:
    with open(json_file,'r') as f:
      content = f.read()
    json.loads( content )
    return True
  except ValueError as error:
    print( error )
    return False

def account_type_validation( df ):
  other_accounts = df.loc[ ~df['AccountType'].isin(['I','E']) ].shape[0]
  if other_accounts > 0:
    print('Please ensure that AccountType is E or I')
    return False
  else:
    return True

def transaction_type_validation( df ):
  other_transactions = df.loc[ ~df['TransactionType'].isin(['S','B']) ].shape[0]
  if other_transactions > 0:
    print('Please ensure that TransactionType is B(Buy) or S(Sell)')
    return False
  else:
    return True

def un_initiated_column_validation( haystack_df, needle_df, column ):
  # Example: Get those transaction.Instrument(needle) values which are not present in position.Instrument(haystack)
  un_initiated_count = needle_df.loc[ ~needle_df[column].isin( haystack_df[column].to_dict().values() ) ].shape[0]
  if un_initiated_count > 0:
    return False
  else:
    return True

def column_name_validator( column_list, data_type ):
  if data_type == 'start_position':
    reqd_columns = ['Instrument', 'Account', 'AccountType', 'Quantity']
  elif data_type == 'transaction':
    reqd_columns = ['TransactionId', 'Instrument', 'TransactionType', 'TransactionQuantity']

  # Find which column of reqd_columns is not in column_list
  missing_col_list = list(set(reqd_columns)-set(column_list))
  if len(missing_col_list) > 0:
    return False
  else:
    return True

