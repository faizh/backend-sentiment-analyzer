import datetime
from posixpath import split

date = '2022-06-23'
date = date.split('-')
date = datetime(date[0], date[1], date[2])
output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
print(output_date)