import datetime
import dateutil.parser as parser
import dateutil.relativedelta as rel


def find_date(image_text:str):
    """
    Finds the date of the image.
    """
    date_str = image_text

    # Initialize variables
    dates = []
    tokens = ''
    date_format = "%m-%d-%Y" # Initialize default date_format
    date = None # Initialize date variable


    try:
        date, date_format = coreParser(date_str)
        if date != None:
            dates.append(date.strftime(date_format))

    # If the date is not found by dateutil.parser, statically check for date insights
    except parser.ParserError:
        print("Error 1: No date format found, checking for date insights...")
        date = dateInsightChecking(date_str)
        if date != None:
            dates.append(date.strftime(date_format))

    # If multiple dates are found by dateutil.parser, split the string and parse each string
    except parser.ParserError2:
        print("Error 2: Multiple dates found, splitting string...")
        mult_dates = dateSplit(date_str)
        dates.extend(mult_dates)



    # Return the dates.
    return dates





def dateSplit(date_str):
    # Check for the number of words in date_str
    str_words = date_str.split()
    strlen = len(str_words)

    splitIndx = strlen//2
    str1 = ' '.join(str_words[:splitIndx])
    str2 = ' '.join(str_words[splitIndx:])

    try:
        date1, date_format1 = coreParser(str1)
        date2, date_format2 = coreParser(str2)

    except parser.ParserError:
        print("Error: No date format found.")
        date1 = dateInsightChecking(str1)

    except parser.ParserError2:
        print("Error: Multiple dates found.")
        mult_dates = dateSplit(str2)

    print(date2)
    return []








def dateInsightChecking(date_str):
    """
    Static Inference Section
    - Check for date insights like:
        - "tomorrow", "next week", "next month", "next year"
    """
    # Current date insights that are checked for
    date_ins = {
        "tomorrow": rel.relativedelta(days=+1), 
        "next week": rel.relativedelta(weeks=+1), 
        "next month": rel.relativedelta(months=+1), 
        "next year": rel.relativedelta(years=+1)}

    # If date_ins is in the unused_string, add the date_ins to the date.
    for insight, offset in date_ins.items():
        if insight in date_str.lower():
            return datetime.date.today() + offset
    return None




def dateElementChecking(date_str, date):
    # Boolean placeholders for whether a month or a day is found in the string
    isMonth = True
    isDay = True

    weekdays = [("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
            ("Sat", "Saturday"),
            ("Sun", "Sunday")]
    months= [('Jan', 'January'), 
            ('Feb', 'February'), 
            ('Mar', 'March'), 
            ('Apr', 'April'), 
            ('May', 'May'), 
            ('Jun', 'June'), 
            ('Jul', 'July'), 
            ('Aug', 'August'), 
            ('Sep', 'Sept', 'September'), 
            ('Oct', 'October'), 
            ('Nov', 'November'), 
            ('Dec', 'December')]
    days = [('1', '1st'),
            ('2', '2nd'),
            ('3', '3rd'),
            ('4', '4th'),
            ('5', '5th'),
            ('6', '6th'),
            ('7', '7th'),
            ('8', '8th'),
            ('9', '9th'),
            ('10', '10th'),
            ('11', '11th'),
            ('12', '12th'),
            ('13', '13th'),
            ('14', '14th'),
            ('15', '15th'),
            ('16', '16th'),
            ('17', '17th'),
            ('18', '18th'),
            ('19', '19th'),
            ('20', '20th'),
            ('21', '21st'),
            ('22', '22nd'),
            ('23', '23rd'),
            ('24', '24th'),
            ('25', '25th'),
            ('26', '26th'),
            ('27', '27th'),
            ('28', '28th'),
            ('29', '29th'),
            ('30', '30th'),
            ('31', '31st')]

    # Basis for checking 
    today = datetime.date.today()

    # only Remove month and/or day if there is no Weekday in string. "On Friday" means that the month and day are important
    for weekday in weekdays[date.weekday()]:
        if weekday not in date_str:         # If there is no weekday but there is a month or day, it could be just a Month and Year or just a Year
            if today.month == date.month:       # which will happen if the month is the same, thus we check if the current month is in the string
                # Check if month really exists in string
                for month in months[today.month-1]:
                    if month not in date_str:
                        isMonth = False
                        break

            if today.day == date.day:
                # Check if day really exists in string
                for day in days[today.day-1]:
                    if day not in date_str:
                        isDay = False
                        break
        else:
            isMonth = True
            isDay = True

    # Select date format appropriate based on the given date elements
    if isMonth and isDay:
        date_format = "%m-%d-%Y"
    elif isDay:
        date_format = "%m-%d-%Y"
    elif isMonth:
        date_format = "%m-%Y"
    else:
        date_format = "%Y"

    return date_format




def coreParser(date_str):
    """
    Date parsing using dateutil.parser
    - Check for dates in the string (only works when one date in string)
    - Return date_format depending on the only existing date elements in the string (If only "January 2020" is passed, return "%m %Y")
    """
    # Parse the date from the date_str
    date, tokens = parser.parse(date_str, fuzzy_with_tokens = True)



    # Check for the only existing date elements in the image text.
    date_format = dateElementChecking(date_str, date)
    

    return date,date_format













# Tests
print(find_date("Your bill is due on the 28th of February"))
print(find_date("Your bill is due on the 28th of May"))
print(find_date("The concert will be on Thursday"))
print(find_date("The deadline is on 2030"))
print(find_date("Dear Sir, tomorrow we will have a meeting"))
print(find_date("Dear Sir, next week we will have a meeting"))
print(find_date("Our meeting will be held next month"))
print(find_date("Next year will be the year of giving"))
print(find_date("Next time"))
# print(find_date("June 19 2022 2023 May")) 