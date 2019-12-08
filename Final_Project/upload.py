# author: Toby Chappell
# date: 12/9/19
# assignment: Final Project conversion from TSV into CSV

import pandas as pd
csv.field_size_limit(sys.maxsize)


r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/name.basics.tsv'
w_filenameCSV ='names.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.akas.tsv'
w_filenameCSV ='akas.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.crew.tsv'
w_filenameCSV ='crew.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.episode.tsv'
w_filenameCSV ='episode.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.principals.tsv'
w_filenameCSV ='principals.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.basics.tsv'
w_filenameCSV ='titles.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)

r_filenameTSV = '/Users/tobychappell/Documents/CPSC_Courses/CPSC_408/Final_Project/Data/Original_TSV/title.ratings.tsv'
w_filenameCSV ='ratings.csv'
df = pd.read_csv(r_filenameTSV, '\t')
df.to_csv(w_filenameCSV, header=False, index=False)
