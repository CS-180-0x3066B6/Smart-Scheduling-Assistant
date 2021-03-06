import datetime
import json
import dateutil.parser as parser
import dateutil.relativedelta as rel


weekdays = [("Mon", "Monday"),
            ("Tue", "Tuesday"),
            ("Wed", "Wednesday"),
            ("Thu", "Thursday"),
            ("Fri", "Friday"),
            ("Sat", "Saturday"),
            ("Sun", "Sunday")]
months= [['Jan', 'January'], 
        ['Feb', 'February'], 
        ['Mar', 'March'], 
        ['Apr', 'April'], 
        ['May', 'May'], 
        ['Jun', 'June'], 
        ['Jul', 'July'], 
        ['Aug', 'August'], 
        ['Sep', 'Sept', 'September'], 
        ['Oct', 'October'], 
        ['Nov', 'November'], 
        ['Dec', 'December']]
# make a list of the months list but not in a tuple
months_list = []
for month in months:
    months_list.append(month[0].lower())
    months_list.append(month[1].lower())
    months_list.append("september")
months_30 = ['january', 'march', 'may', 'july', 'august', 'october', 'december']
months_31 = ['april', 'june', 'september', 'november']
days = [['1', '1st'],
        ['2', '2nd'],
        ['3', '3rd'],
        ['4', '4th'],
        ['5', '5th'],
        ['6', '6th'],
        ['7', '7th'],
        ['8', '8th'],
        ['9', '9th'],
        ['10', '10th'],
        ['11', '11th'],
        ['12', '12th'],
        ['13', '13th'],
        ['14', '14th'],
        ['15', '15th'],
        ['16', '16th'],
        ['17', '17th'],
        ['18', '18th'],
        ['19', '19th'],
        ['20', '20th'],
        ['21', '21st'],
        ['22', '22nd'],
        ['23', '23rd'],
        ['24', '24th'],
        ['25', '25th'],
        ['26', '26th'],
        ['27', '27th'],
        ['28', '28th'],
        ['29', '29th'],
        ['30', '30th'],
        ['31', '31st']]
days_list = []
for day in days:
    days_list.append(day[0])
    days_list.append(day[1])
conjunctions = ["and", "or", "but", "for", "nor", "yet", "so", "\n", "to","$"]





def check_misspelling(date_str):
    # Create a dictionary of months as values and possible misspellings as keys 
    date_str_list = date_str.split()
    master = {}
    with open('misspellings.txt', 'r') as file:
        master = json.load(file)
    # Check the date_str if it contains the key of the months dictionary. If it does, replace the key with the value
    for item in date_str_list:
        if item.lower() in master:
            date_str = date_str.replace(item, master[item.lower()])
    return date_str



def parseCategorizer(image_text, current_date):
    print("Image Text: " + image_text)
    """
    Finds the date of the image.
    """
    date_str = image_text

    date_format = "%m-%d-%Y" # Initialize default date_format
    date = None # Initialize date variable
    dates = []
    try:
        parser.parse(date_str, fuzzy = True)
        parsed_dates, date_formats = coreParser(date_str, current_date)
        for parsedDate in parsed_dates:
            if parsedDate != None:
                if parsedDate >= current_date and parsedDate < datetime.datetime(year=2050, month=12, day=31):
                    dates.append(parsedDate.strftime(date_formats[parsedDate]))

    # If the date is not found by dateutil.parser, statically check for date insights
    except parser.ParserError:
        date = dateInsightChecking(date_str, current_date)
        if date != None:
            if date >= current_date and date < datetime.datetime(year=2050, month=12, day=31):
                dates.append(date.strftime(date_format))

    # If multiple dates are found by dateutil.parser, split the string and parse each string
    except parser.ParserError2:
        if(date_str.split()[0] == date_str):
            mult_dates = []
        else:
            mult_dates = find_date(date_str, current_date)
        dates.extend(mult_dates)

    except parser.ParserError3:
        str_words = date_str.split()

        firstHalf = str_words[:-1]
        secondHalf = str_words[-1:]
        
        while True:
            try:
                nextItem = firstHalf.pop()
                secondHalf.insert(0, nextItem)
                parser.parse(" ".join(secondHalf), fuzzy = True)
                
            except parser.ParserError2:
                firstHalf.append(secondHalf.pop(0))
            except parser.ParserError:      # If it gets an error about the date being invalid, just continue
                pass
            except parser.ParserError3:      # If it gets an error about the date being invalid, just continue
                firstHalf.append(secondHalf.pop(0))
                break
            except IndexError:
                break
        
        parsed_dates, date_formats = coreParser(" ".join(firstHalf), current_date)
        for parsedDate in parsed_dates:
            if parsedDate != None:
                if parsedDate >= current_date and parsedDate < datetime.datetime(year=2050, month=12, day=31):
                    dates.append(parsedDate.strftime(date_formats[parsedDate]))
        

    return dates



def remove_alphanumerics(date_str: str)->str:
    print("Accessing Alphanumeric Remover")
    words = date_str.split()
    numeric = [str(x) for x in range(10)]+[",",".","/","-"]
    for word_index in range(len(words)):
        word: str = words[word_index] 
        contains_non_numeric = False
        contains_numeric = False
        for character in word:
            if character in numeric:
                contains_numeric = True
            if character not in numeric:
                contains_non_numeric = True
        if contains_non_numeric and contains_numeric:
            print("Removing ",word)
            words[word_index] = ""

    print(words)
    return " ".join(words)


def replace_characters(date_str: str)->str:
    # Check for the number of words in date_str
    date_str = date_str.replace('????', ' ')
    date_str = date_str.replace('\\', ' ')
    date_str = date_str.replace('.', ' ')
    date_str = date_str.replace(',', ' ')
    date_str = date_str.replace('$', '9999')
    date_str = date_str.replace('??', '9999')
    date_str = date_str.replace('&', '9999')
    date_str = date_str.replace('%', '9999')
    date_str = date_str.replace('#', '9999')
    date_str = date_str.replace('@', '9999')
    date_str = date_str.replace("???", " ")
    return date_str


def find_date(date_str, current_date):
    print(date_str)
    assert(current_date != None)
    date_str = check_misspelling(date_str)
    date_str = remove_alphanumerics(date_str)
    date_str = replace_characters(date_str)
    firstHalf, secondHalf = dateSplit(date_str)

    str1 = " ".join(firstHalf)
    str1 = str1.replace('-', ' to ')
    str1 = str1.replace('/', ' ')
    str2 = " ".join(secondHalf)
    str2 = str2.replace('-', ' to ')
    str2 = str2.replace('/', ' ')
    # Try for first half of the string
    dates1 = parseCategorizer(str1, current_date)
    # Try for second half of the string
    dates2 = parseCategorizer(str2, current_date)

    return dates1 + dates2


def dateValidity(str_words):
    for i in range(len(str_words)):
        try:
            intNextItem = int(str_words[i])
            # if intNextItem is greater than 2000 and less than 1900, remove it from the string and replace with a space
            if intNextItem > 3000 or intNextItem < 1900:
                if intNextItem > 31:
                    str_words[i] = " "
                else:
                    try:
                        # check if this is a day. If it is not preceded or followed by a month, change it to space
                        if str_words[i-1].lower() not in months_list and str_words[i+1].lower() not in months_list and str_words[i+1] != "of":
                            str_words[i] = " "
                        else:
                            # Check if the day for the month is valid
                            if str_words[i+1] == "of":
                                pass

                            if intNextItem > 30 and (str_words[i-1].lower() not in months_31 or str_words[i+1].lower() not in months_31):
                                str_words[i] = " "
                            
                            elif intNextItem > 29 and (str_words[i-1].lower() in "february" or str_words[i+1].lower() in "february"):
                                str_words[i] = " "
                    except:
                        pass
        except:
            if str_words[i] in days_list:
                # Check if it is a day. if it is not preceded or followed by a month, change it to space
                try:
                    if str_words[i-1].lower() not in months_list and str_words[i+1].lower() not in months_list and str_words[i+1] != "of":
                        str_words[i] = " "
                        # Remove the suffix of the day like 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th and change to 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
                except:
                    pass
            elif "-" in str_words[i]:
                try:
                    # Count number of "-" in the string
                    dashIdx = str_words[i].index("-")
                    if str_words[i].count("-") == 1:
                        if dashIdx == 2:
                            str_words[i] = str_words[i][0:2]
                except:
                    pass
    return str_words

def dateSplit(date_str):
    str_words = date_str.split()
    str_words = dateValidity(str_words)
    firstHalf = str_words[:1]
    secondHalf = str_words[1:]
    while True:
        try:
            nextItem = secondHalf.pop(0)
            if nextItem.lower() in conjunctions:
                secondHalf.insert(0, nextItem)
                break
            
            
            firstHalf.append(nextItem)
            parser.parse(" ".join(firstHalf), fuzzy = True)
        except parser.ParserError2:
            secondHalf.insert(0, firstHalf.pop())
            break
        except parser.ParserError:      # If it gets an error about the date being invalid, just continue
            pass
        except parser.ParserError3:      # If it gets an error about the date being invalid, just continue
            pass
        except IndexError:
            break
    
    print("HERE")
    print(firstHalf)
    return firstHalf, secondHalf

def dateInsightChecking(date_str, current_date):
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
            return current_date+ offset
    return None




def dateElementChecking(date_str, date, current_date):
    # Boolean placeholders for whether a month or a day is found in the string
    isMonth = True
    isDay = True

    # Basis for checking 
    today = datetime.date.today()

    # only Remove month and/or day if there is no Weekday in string. "On Friday" means that the month and day are important
    for weekday in weekdays[date.weekday()]:
        if weekday not in date_str:         # If there is no weekday but there is a month or day, it could be just a Month and Year or just a Year
            if today.month == date.month:       # which will happen if the month is the same, thus we check if the current month is in the string
                # Check if month really exists in string
                for month in months[today.month-1]:
                    if month.lower() not in date_str:
                        isMonth = False
                    else:
                        break

            if today.day == date.day:
                # Check if day really exists in string
                for day in days[today.day-1]:
                    if day.lower() not in date_str:
                        isDay = False
                    else:
                        break
        else:
            isMonth = True
            isDay = True

    # Check if the year is the current year, if yes, then check the string if the year is really there, if not, change it to the year from current_date
    if date.year == today.year:
        date_str = date_str.replace(str(date.day),"",1)
        year_str = str(date.year)
        year_str = year_str[-2:]
            
        if year_str not in date_str:
            date = date.replace(year=current_date.year)
        else:
            date = date.replace(year=today.year)

    # Select date format appropriate based on the given date elements
    if isMonth and isDay:
        return "%m-%d-%Y", date
    elif isDay:
        # get the month from currentDate and replace the month in date with the current month
        return "%m-%d-%Y", date.replace(month=current_date.month)
    elif isMonth:
        return "%m-%Y", date
    else:
        return "%Y", date





def coreParser(date_str, current_date):
    """
    Date parsing using dateutil.parser
    - Check for dates in the string (only works when one date in string)
    - Return date_format depending on the only existing date elements in the string (If only "January 2020" is passed, return "%m %Y")
    """
    # Split the string into a list separated by newlines
    str_words = date_str.splitlines()
    dates_in_string = []
    date_formats = {}
    for i in str_words:
        print(i)
        try:
            date = parser.parse( 
                                timestr = i, 
                                fuzzy = True)
            # Check for the only existing date elements in the image text.
            date_format, date = dateElementChecking(date_str, date, current_date)
            dates_in_string.append(date)
            date_formats[date] = date_format

        except parser.ParserError: # No date found
            continue

        except parser.ParserError3:
            continue
  
    
    return dates_in_string, date_formats


print(find_date("fos Angeles Times eo0en 10-111-200", datetime.datetime(1972, 1, 1)))