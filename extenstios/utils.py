from. import jalali

def django_jalali(time):
    jmonths = [
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند"
    ]

    time_month = None

    time_str = f"{time.year},{time.month},{time.day}"
  

    for index, month in enumerate(jmonths):
            if  time.month == index + 1:
                time_month = month

  

    return f"{time.year},{time_month},{time.day}"

def jalalitime(time):
    output = jalali.Gregorian(time).persian_string()

    return f'{output}'