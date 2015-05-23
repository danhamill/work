import xlrd
import csv
from glob import glob
import os

root = "C:/workspace/Reach_4a/grain_size/Bed_Codes"
out = "C:/workspace/Reach_4a/grain_size/Bed_Codes/csv/"

def csv_from_excel(afile, dest):
    wb = xlrd.open_workbook(afile)
    sh = wb.sheet_by_name('Sheet1')
    your_csv_file = open(dest, 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_NONE)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()

list = glob (root + '\*xls')

for afile in list:
    print os.path.basename(os.path.splitext(afile)[0]) +'\n'
    nakedname = os.path.basename(os.path.splitext(afile)[0])
    dest = out + nakedname + '.csv'
    print dest + '\n'
    csv_from_excel(afile,dest)