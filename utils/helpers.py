import datetime

def format_date(date):
    return date.strftime('%B %d, %Y')

def generate_slug(title):
    return title.lower().replace(' ', '-')