import datetime
from typing import List, Dict, Any
from datetime import datetime as dt
from codingclub_api.apps.enums import Date
from codingclub_api.apps.email_service import send_email
from codingclub_api.apps.clubs.enums import EventStatus
from codingclub_api.apps.users.models import User
from codingclub_api.apps.clubs.models import ClubEvent, EventRegistration


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


def event_name_url(events: List) -> List:
    return [
        {"event_name": event["name"], "image_url": event["banner"]} for event in events
    ]


class EventRegistrationService:
    @staticmethod
    def email_to_all(registrations):
        for registration in registrations:
            pass

    @staticmethod
    def structure_registrations(registrations) -> Any:
        registrations_json = []
        errors = []
        event = ClubEvent.objects.get(id=registrations["of_event_id"])
        for no_of_registration in range(len(registrations["registration_for_user"])):
            # check if user exists or not
            if not User.objects.filter(
                email=registrations["registration_for_user"][no_of_registration]
            ).exists():
                raise ValueError(
                    f"User with email {registrations['registration_for_user'][no_of_registration]} does not exists"
                )

            # Get user if it exists
            user = User.objects.get(
                email=registrations["registration_for_user"][no_of_registration]
            )
            if EventRegistration.objects.filter(
                registration_for_user=user, of_event=event
            ).exists():
                errors.append(f"{user.first_name} {user.last_name}")
            else:
                registrations_json.append(
                    {
                        "of_event_id": registrations["of_event_id"],
                        "registration_for_user_id": user.user_id,
                        "registering_user_email": registrations[
                            "registering_user_email"
                        ],
                    }
                )
                body = (
                    f"Event registration successful for user: {user.first_name} {user.last_name} \n"
                    f"Registering user email: {registrations['registering_user_email']}"
                )
                send_email(
                    to=user.email, subject=f"Registration for event {event}", body=body
                )
        return registrations_json, errors

    @staticmethod
    def check_seats_limit(
        registrations: List, registered_seats: int, total_seats: int
    ) -> bool:
        if len(registrations) + registered_seats > total_seats:
            return True
        return False
