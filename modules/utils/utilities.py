import os 
def strip_path(path : str, directory_name : str) -> str:

    stripped_file_name = strip_after_substring(path, directory_name)
    
    return stripped_file_name + directory_name

def get_needed_path(file_path , destination_directory : str , path_to_append : str) -> str:

    return strip_path(file_path, destination_directory) + path_to_append


def strip_after_substring(str : str, substring : str) -> str:
    
    return str.split(substring)[0]
