import parser
from datetime import datetime

# Пример использования функции:
print(parser.apache_ip('245.80.209.29'))
print(parser.apache_date(datetime.strptime('17/Aug/1973:14:09:40 +0300', '%d/%b/%Y:%H:%M:%S %z')))
print(parser.apache_date_range(datetime.strptime('17/Aug/1973:14:09:40 +0300', '%d/%b/%Y:%H:%M:%S %z'), datetime.strptime('20/Sep/2037:16:02:54 +0300', '%d/%b/%Y:%H:%M:%S %z')))
print(parser.json_ip('192.168.2.34'))
print(parser.json_date('1991-01-10'))
print(parser.json_date_range('1991-01-10', '2019-07-25'))