import datetime
from typing import List, Dict
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


def events_by_months(year: str, years: Dict, month: str, event: Dict):
    if year not in years:
        years[year] = {month: [event["start_date"]]}
    else:
        if month in years[year]:
            years[year][month].append(event["start_date"])
        else:
            years[year][month] = [event["start_date"]]


def structure_event(events):
    years = {}
    year_now = dt.today().date().year
    for event in events:
        date = event["start_date"]
        upc_date = dt.strptime(date, Date.DATE_FORMAT.value).date()
        month = upc_date.strftime("%B")
        year = str(upc_date.year)
        if year == year_now:
            events_by_months(year=year, years=years, month=month, event=event)
        else:
            events_by_months(year=year, years=years, month=month, event=event)
    sorted_years = dict(sorted(years.items(), key=lambda x: int(x[0])))
    for year, months in sorted_years.items():
        sorted_months = dict(
            sorted(months.items(), key=lambda x: datetime.datetime.strptime(x[0], "%B"))
        )
        sorted_years[year] = sorted_months
    return sorted_years
