import os
import sys

class HousingException(Exception):

    def __init__(self,error_msg:Exception,error_details:sys):
        super().__init__(error_msg)

        self.error_message = HousingException.get_detailed_error_message(error_msg=error_msg,error_details=error_details)
        self.error_details = error_details
    
    @staticmethod # Called the function without creating the class object
    def get_detailed_error_message(error_msg:Exception,error_details:sys)->str:
        
        """_summary_

        Args:
            error_msg (Exception): obj of Exception
            error_details (sys): obj of sys

        Returns:
            str: error_message
        """
        _,_,exec_tb = error_details.exc_info()
        line_number = exec_tb.tb_frame.f_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"Error occured in script: [{file_name}] at line number :[{line_number}] error_message :[{error_msg}]"
        return error_message

    def __str__(self) -> str:
        return self.error_message  

    def __repr__(self)->str:
        return HousingException.__name__.str()      