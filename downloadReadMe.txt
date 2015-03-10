Run download.py to update all the text files in the data folder specified in the dataSource.csv file.
dataSource.csv := <dataEntry>*
<dataEntry> := <update>,<url>,<language>,<outputFileName>
<update> If the file should be updated := “true”|anythingelse
<url> := “http://”<lang domain>”.wikipedia.org/wiki/”<articleName>
<language>:= {“English”,”German”,”Kurdish”…}
<outputFileName> := any Text
