from datetime import datetime, timedelta


def working_hours_per_week(start_date, end_date):
    print(start_date)
    # Define working hours
    start_hour = 8
    end_hour = 16

    # Initialize a dictionary to hold hours per week
    hours_per_week = {}

    # Function to calculate working hours in a day
    def calculate_daily_hours(date):
        # If it's the start date or end date, calculate hours differently
        if date.date() == start_date.date():
            daily_start = max(start_date.hour, start_hour)
        else:
            daily_start = start_hour

        if date.date() == end_date.date():
            daily_end = min(end_date.hour, end_hour)
        else:
            daily_end = end_hour

        return max(0, daily_end - daily_start)

    # Iterate over each day between start and end dates
    current = start_date
    while current <= end_date:
        # Check if current day is a weekday (Monday=0, Sunday=6)
        if current.weekday() < 5:
            daily_hours = calculate_daily_hours(current)

            # Week of the month and month calculation
            week_of_month = (current.day - 1) // 7 + 1
            month = current.strftime('%B')
            year = current.strftime('%Y')

            # Add hours to the respective week and month
            week_key = f"{week_of_month}{'st' if week_of_month == 1 else 'nd' if week_of_month == 2 else 'rd' if week_of_month == 3 else 'th'} week of {month}, {year}"
            hours_per_week[week_key] = hours_per_week.get(week_key, 0) + daily_hours

        # Move to the next day
        current += timedelta(days=1)
        current = current.replace(hour=0)

    return hours_per_week
