"""
to get the file name from the given url
# os.path.basename(url)
"""


"""
from  six.moves import urllib
it use for download the data and store it into location
urllib.request.urlretrieve(download_url,tgz_file_path)
"""

"""to extract tar file and get the data and store that data into location

with tarfile.open(tgz_file_path) as housing_tgz_file_path_obj :
                housing_tgz_file_path_obj.extractall(path=raw_data_dir)
"""

"""to know the file present inside the give dir_path
file_name = os.listdir(raw_data_dir)[0]
"""


    
