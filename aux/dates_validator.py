import datetime
def start_date_formatter(start):
    start = start + ' 00:00:00'
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    return start

def end_date_formatter(end):
    end = end + ' 23:59:59'
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    return end

def date_validator(start, end):
    start_date = start_date_formatter(start)
    end_date = end_date_formatter(end)
    if (start_date < end_date):
        return True
    return False

def date_formatter(date):
    current_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    return current_date

def date_in_range(start, end, current):
    start_date = start_date_formatter(start)
    end_date = end_date_formatter(end)
    current_date = date_formatter(current)
    if start_date <= current_date <= end_date:
        return True
    return False