# build file list l['<ubvu_id.tif>']='/dspace_storage/export/krt/56/<ubvu_id>.tig'
# open csv metadata list
# open sftp connection
# walk through csv rows
# upload tif per row
from config import FTP_HOST, FTP_PASSWORD, FTP_USER, CSV_LIST, FILENAME_COLUMN
import csv
import sys
import glob
import os
from ftplib import FTP


class FtpKlokan():
    sizeWritten = 0
    totalSize = 0
    lastShownPercent = 0

    def __init__(self):
        self.host = FTP_HOST
        self.user = FTP_USER
        self.password = FTP_PASSWORD
        self.connection = None

    def close(self):
        self.connection.close()

    def _connect(self):
        if self.connection == None:
            self.connection = FTP(FTP_HOST)
            self.connection.login(FTP_USER, FTP_PASSWORD)
            self.connection.set_debuglevel(2)

    def _download(self, path, filename, local_path):
        self._connect()
        self.connection.retrbinary('%s%s' % (path, filename), local_path + filename)
        return filename

    def _handle(self, block):
        self.sizeWritten += 1024
        percentComplete = round((self.sizeWritten / self.totalSize) * 100)
        if (self.lastShownPercent != percentComplete):
            self.lastShownPercent = percentComplete
            # print("\r" + str(percentComplete) + " percent complete", end='')

    def upload(self, remote_path, local_file, filename):
        self._connect()
        self.connection.cwd(remote_path)
        with open(local_file, 'rb') as fp:
            self.connection.storbinary('STOR ' + filename, fp, 1024, self._handle)

    def dir(self, path):
        self._connect()
        dir = self.connection.nlst(path)
        return dir


list = {}
for filename in glob.iglob('/dspace-storage/export/krt/**/*.tif', recursive=True):
    basename = os.path.basename(filename)
    list[basename] = filename

lol = csv.reader(open(CSV_LIST, 'rt', encoding='utf8'), delimiter=',')

# 1699,0106051013001,0106051013001.tif,http://imagebase.ubvu.vu.nl/cdm/ref/collection/krt/id/2977,http://imagebase.ubvu.vu.nl/cdm/deepzoom/collection/krt/id/2977,"Gallia, vulgo la France / [Nicolaes Visscher]",1677,Annotatie: Origineel is Blad 12 in atlas factice,"Visscher, Nicolaes (1618-1679)",[Amsterdam : ex officina Nicolai Visscher],46,56,2500000,300,52,41,8,-6,,
s = FtpKlokan()
remote_list = s.dir('')
header = True
missing = []
grandtotal = 0
for line in lol:
    filename = line[FILENAME_COLUMN]  # or whatever column it is
    if filename not in remote_list:
        try:
            totalSize = os.path.getsize(list[filename])
            s.lastShownPercent = 0
            s.sizeWritten = 0
            s.totalSize = totalSize
            print(list[filename])
            print('Total file size : ' + str(round(totalSize / 1024 / 1024, 1)) + ' Mb')
            grandtotal = grandtotal + totalSize
            s.upload('/', list[filename], filename)
        except:
            print("Unexpected error uploading " + filename + ":", sys.exc_info()[0])
            missing.append(filename)
    else:
        print(filename + ' already uploaded, skip.')
print(missing)

print('Grand total file size : ' + str(round(grandtotal / 1024 / 1024 / 1024, 1)) + ' Gb')
s.close()

# eerste pluk 101.4GB
# alles 589GB
