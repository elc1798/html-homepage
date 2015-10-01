# This is a script to load the 'calendar' section of the StuyHack website.
# This script is invoked by devploy.sh, which handles deploying the site.

# This script handles adding calendar events and generating the calendar.
# DO NOT EDIT THE EVENTS FILE (fullcalendar/demos/DEVPLOY_EVENTS) MANUALLY!

import os, sys
import argparse

# Load file path constants

PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
FULLCALENDAR_EXTENDED_DIR = PARENT_DIR + "/fullcalendar/demos/"
DEVPLOY_PRE = FULLCALENDAR_EXTENDED_DIR + "DEVPLOY_PREFIX.html"
DEVPLOY_SUF = FULLCALENDAR_EXTENDED_DIR + "DEVPLOY_SUFFIX.html"
DEVPLOY_EV = FULLCALENDAR_EXTENDED_DIR + "DEVPLOY_EVENTS"
DEVPLOY_CAL = FULLCALENDAR_EXTENDED_DIR + "theme.html"

# The add_event function should signal a crash via this method if dates are
# in an invalid format.
def assert_valid_time_length(start_date, end_date):
    # Dates should be in the format yyyy-mm-dd
    assert(len(start_date) == 10 and len(end_date) == 10)
    # Check for the dashes
    assert(start_date[4:5] == '-')
    assert(start_date[7:8] == '-')
    assert(end_date[4:5] == '-')
    assert(end_date[7:8] == '-')

    # Check if yyyy, mm, and dd are valid ints
    # This will crash with a Native Python Exception
    start_year = int(start_date[0:4])
    start_month = int(start_date[5:7])
    start_day = int(start_date[8:10])
    end_year=int(end_date[0:4])
    end_month = int(end_date[5:7])
    end_day = int(end_date[8:10])

    # Check if months make sense
    assert(1 <= start_month and start_month <= 12)
    assert(1 <= end_month and end_month <= 12)

    # Check if the day is valid for the given month
    if start_month in [1, 3, 5, 7, 8, 10, 12]:
        assert(1 <= start_day and start_day <= 31)
    elif start_month in [4, 6, 9, 11]:
        assert(1 <= start_day and start_day <= 30)
    else:
        assert(start_month == 2)
        if (start_year % 4 == 0):
            # Leap year
            assert(1 <= start_day and start_day <= 29)
        else:
            assert(1 <= start_day and start_day <= 28)

    if end_month in [1, 3, 5, 7, 8, 10, 12]:
        assert(1 <= end_day and end_day <= 31)
    elif end_month in [4, 6, 9, 11]:
        assert(1 <= end_day and end_day <= 30)
    else:
        assert(end_month == 2)
        if (end_year % 4 == 0):
            # Leap year
            assert(1 <= end_day and end_day <= 29)
        else:
            assert(1 <= end_day and end_day <= 28)

    # Assert the length makes logical sense
    # Check if the month is an actual month
    assert(start_year <= end_year)
    assert(start_year < end_year or start_month <= end_month)
    assert(start_year < end_year or start_month < end_month or start_day <= end_day)

def add_event(contents, start_date, end_date):
    assert_valid_time_length(start_date, end_date)
    tabulation = " " * 16
    new_event = tabulation + ",{\n"
    new_event += tabulation + "    title: "
    new_event += repr(contents) + ",\n" # Abuse repr() to generate to quotes
    new_event += tabulation + "    start: "
    new_event += repr(start_date) + ",\n"
    new_event += tabulation + "    end: "
    new_event += repr(end_date) + "\n"
    new_event += tabulation  + "}\n"

    events_file = open(DEVPLOY_EV , 'a') # Open with 'append' protocol
    events_file.write(new_event)
    events_file.close()

def generate_calendar():
    prefix_file = open(DEVPLOY_PRE , 'r')
    events_file = open(DEVPLOY_EV , 'r')
    suffix_file = open(DEVPLOY_SUF , 'r')
    cal_file = open(DEVPLOY_CAL , 'w')

    cal_file.write(prefix_file.read() + events_file.read() + suffix_file.read())
    prefix_file.close()
    events_file.close()
    suffix_file.close()
    cal_file.close()

def interactive_add():
    start_date = str(raw_input("Start date in yyyy-mm-dd format: "))
    end_date = str(raw_input("End date in yyyy-mm-dd format (Leave blank if same as start date): "))
    if end_date == "":
        end_date = start_date
    assert_valid_time_length(start_date, end_date)
    event_title = str(raw_input("Event title (keep it short!): "))
    if len(event_title) > 20:
        print("Full title of event may not display on site")
    add_event(event_title, start_date, end_date)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--add",
        help="Opens an interactive prompt for add an event",
        action="store_true"
    )
    parser.add_argument(
        "-g",
        "--generate",
        help="Generate theme.html",
        action="store_true"
    )
    args = parser.parse_args()
    if args.add:
        interactive_add()
    elif args.generate:
        generate_calendar()
    else:
        print("Invalid flag.")
        exit(1)

if __name__ == "__main__":
    main()
