### File HTML report processor

This project takes the resulting HTML report file from NiraSoft's folder_changes_view application:

https://www.nirsoft.net/utils/folder_changes_view.html

And does the following:

- Hash the filenames
- Remove the Path and File Owner information
- Export a randomly generated encryption key saved to a file
- Save the resulting data in a text file in an encrypted string

Doing this will anonymize the data and encrypts the results JSON string before writing it to a file, this allows it to 
be sent securely.

Inversely the tools can take the resulting file with the key and decrypt the data to a JSON file.

The JSON file can then be imported into Python Pandas for analysis. For example:

 ```
 import pandas as pd
 
 dataframe = pd.from_json(r'C:\path\to\json_file.json)
   
 dataframe.head()
```

It is recommended to use folder_changes_view and the my application on a dedicated VM with an account **Read Only** 
permissions

I have no concerns over either application; however, you cannot be too careful.

This tool's GUI is made with PySimpleGUI, it's a great GUI framework, check them out here:

https://pysimplegui.readthedocs.io/en/latest/ 