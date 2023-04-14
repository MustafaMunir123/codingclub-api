from typing import List
from datetime import datetime as dt
from codingclub_api.apps.enums import Date
from codingclub_api.apps.clubs.enums import EventStatus


def update_event_status(events: List, date_today):
    updated_events = []
    for event in events:
        if event.start_date <= date_today < event.end_date:
            event.registration_status = EventStatus.ONGOING.value
            event.save()
            updated_events.append(event)
        elif date_today < event.start_date:
            event.registration_status = EventStatus.UPCOMMING.value
            event.save()
            updated_events.append(event)
        else:
            event.registration_status = EventStatus.PREVIOUS.value
            event.save()
            updated_events.append(event)
    return updated_events


def structure_event(events: List):
    months = {}
    years = {}
    new_months = {}
    year_now = dt.today().date().year
    for event in events:
        date = event["start_date"]
        upc_date = dt.strptime(date, Date.DATE_FORMAT.value).date()
        month = upc_date.strftime("%B")
        year = upc_date.year
        if year == year_now:
            if month in months:
                months[month].append(event)
            else:
                months[month] = [event]
            if year in years:
                years[year].append(months)
            else:
                years[year] = [months]
        else:
            if month in new_months:
                new_months[month].append(event)
            else:
                new_months[month] = [event]
            if year in years:
                years[year].append(new_months)
            else:
                years[year] = [new_months]
    return years
