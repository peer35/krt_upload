# Upload Map Collection to Klokan
## Export collection
On pdspc001.vu.nl 

Make an export folder
```
sudo mkdir /dspace-storage/export/krt
sudo chmown -R tomcat:tomcat /dspace-storage/export/krt
```
Export the collection:
```
sudo -u tomcat ./dspace export -t COLLECTION -i 123456789/1127 -d /dspace-storage/export/krt -n 1
```
Note `123456789/1127` is the collection handle

## Upload
Rename `config.template.py` to `config.py` and fill in the correct password, the csv filename and the column containing the filenames (starting at 0)

Use klokan_upload.py to upload the files.