from datetime import date, timedelta

tdifference = date.today() - date(2019, 1, 14)

if tdifference < timedelta(days=30):
    print('true')
else:
    print('false')