from typing import List
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
