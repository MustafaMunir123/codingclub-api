from codingclub_api.apps.clubs.enums import EventStatus
CLUB_ROLES = (
    ('Member', 'Member'),
    ('Lead', 'Lead'),
    ('Co-Lead', 'Co-Lead'),
    ('Director', 'Director'),
    ('Co-Director', 'Co-Director'),
    ('Volunteer', 'Volunteer'),
    ('Manager', 'Manager')
)

EVENT_STATUS = (
    ('Ongoing', EventStatus.ONGOING.value),
    ('Up-Coming', EventStatus.UPCOMMING.value),
    ('Past', EventStatus.PAST.value)
)
