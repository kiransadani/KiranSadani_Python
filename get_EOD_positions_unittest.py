import unittest
from validationfunctions import *

class TestValidations(unittest.TestCase):

  def test_input_validation(self):
    arg_list = ['get_EOD_positions.py','1537277231233_Input_Transactions.txt', '1537277231233_Input_Transactions.txt']
    self.assertTrue( input_validation( arg_list ), msg='Valid files and valid no of arguments' )

    arg_list = ['get_EOD_positions.py','Dummy_Input_Transactions.txt', '1537277231233_Input_Transactions.txt']
    self.assertFalse( input_validation( arg_list ), msg='Invalid file or invalid no of arguments' )

  def test_json_file_validation(self):
    self.assertTrue( json_file_validation('1537277231233_Input_Transactions.txt'), msg='Valid Json')
    self.assertFalse( json_file_validation('Input_StartOfDay_Positions.txt'), msg='Invalid Json')

  def test_column_name_validator(self):
    self.assertTrue( column_name_validator(['Instrument', 'Account', 'AccountType', 'Quantity'], 'start_position'), msg='Valid columns')
    self.assertFalse( column_name_validator(['Instrument', 'Account', 'AccountType', 'QuantityDummy'], 'start_position'), msg='Invalid columns')


if __name__ == '__main__':
  unittest.main()

