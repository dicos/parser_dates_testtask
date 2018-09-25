import re
from datetime import datetime

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


MONTH_NAMES = (
    ('январь', 'янв'),
    ('февраль', 'фев'),
    ('март', 'мар'),
    ('апрель', 'апр'),
    ('май', 'май'),
    ('июнь', 'июн'),
    ('июль', 'июл'),
    ('август', 'авг'),
    ('сентябрь', 'сен'),
    ('октябрь', 'окт'),
    ('ноябрь', 'ноя'),
    ('декабрь', 'дек'),
)


def remove_year(date_str_input):
    return date_str_input.replace('..', '.').replace('г.', '').replace('г', '').strip()


def replace_ru_month(date_str_input):
    """ Заменяем русское название месяца на его номер """
    date_str = date_str_input.lower()
    for index, tokens in enumerate(MONTH_NAMES):
        for token in tokens:
            if token in date_str:
                return remove_year(date_str.replace(token, str(index + 1)))
    raise ValueError


def date_period(str_date):
    years = [int(s) for s in str_date.split() if s.isdigit()]
    return datetime.now() + relativedelta(years=years[0])



DATE_FORMATS = (
    (re.compile(r'^[0-3]?\d/\d{4} ?(г(\.)?)?$', re.I | re.U), lambda x: datetime.strptime(remove_year(x), '%m/%Y')),
    (re.compile(r'^[^0-9]*\d{2}( г.)?$'), lambda x: datetime.strptime(replace_ru_month(x), '%m %y')),
    (re.compile(r'^[^0-9]*\d{2}( г.)?$'), lambda x: datetime.strptime(replace_ru_month(x), '%m.%y')),
    (re.compile(r'^[^0-9]*\d{4}( г.)?$'), lambda x: datetime.strptime(replace_ru_month(x), '%m %Y')),
    (re.compile(r'^[0-3]?\d\.\d{4}.[0-3]?\d\.\d{4}$'), lambda x: datetime.strptime(x[:7], '%m.%Y')),
    (re.compile(r'^\d{2}\.\d{2}\.\d{2}$'), lambda x: datetime.strptime(x, '%d.%m.%y')),
    (re.compile(r'^\d{2},\d{2}\.\d{4}$'), lambda x: datetime.strptime(x, '%d,%m.%Y')),
    (re.compile(r'^\d+/\d{4} ?(г(\.)?)?$'), lambda x: datetime.strptime(remove_year(x), '%d/%Y')),
    (re.compile(r'^\d{3}/\d{4} ?(г(\.)?)?$'), lambda x: datetime.strptime(remove_year(x).split('/')[1], '%Y')),
    (re.compile(r'^\d{2}\.\d{2}\.\d{2}$'), lambda x: datetime.strptime(x[3:], '%m.%y')),
    (re.compile(r'^\d+[^0-9]{2,}$'), date_period),
    (re.compile(r''), lambda x: parse(remove_year(x))),
)


if __name__ == '__main__':
    import csv
    with open('unparsered.txt', 'w') as unparsered:
        with open('file_result.txt', 'w') as file_result:
            csv_reader = csv.reader(open('dates.csv', 'r'))
            for row in csv_reader:
                str_date = row[0].strip()
                if 'данных' in str_date.lower() or 'ожидается' in str_date.lower():
                    continue
                parsered = False
                for pattern, converter in DATE_FORMATS:
                    if pattern.match(str_date):
                        try:
                            date_obj = converter(str_date)
                        except ValueError:
                            continue
                        else:
                            file_result.write(converter(str_date).strftime('01.%m.%Y') + '\n')
                            parsered = True
                            break
                if not parsered:
                    unparsered.write(str_date + '\n')