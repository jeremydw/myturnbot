#!/usr/bin/python3
import requests
from datetime import datetime, timedelta

date_format = '%Y-%m-%d'

url = "https://api.myturn.ca.gov/public/locations/a2ut0000006eUhiAAE/availability"

payload = {
    'vaccineData': 'WyJhM3F0MDAwMDAwMDFBZExBQVUiXQ==',
    'doseNumber': 1,
    'url': 'https://myturn.ca.gov/appointment-select'
}

headers = {
  'Content-Type': 'application/json',
  'Cookie': 'ak_bmsc=ABCCA0D94E1D434C5C91DE8CCBCB6AB0B81CDBDE176B000032104B60AD8BE900~plQR29tOQ/HcPPmAQ1XjLuPmzL6vij7jQiDx6NSTEZuUmYBkrw67NhmctYPlqNX4iBtDe35eBWuQ8PlffOb8pBCYp7OaP+U5buZN7OkInSekN5+DAtR/ULdXA+SPyjnQMmkO6JV0rNDSzKhHKMEumNFOQvLzbqjhBL1Ci7/tV0kvuh8yJx3TEz0GWD2MD9mr4C7zoNphesWv6SlamQzLyvhCmuhqhLVPTmBqhrDzkisdw=; bm_sz=CAE44E75F08380FDBF010A699FFA6049~YAAQ3tscuCxZHhN4AQAAgUY3JQttf0KJ+/MJsTgZTXUSygSAGM4IdxW6kVOce2vZhYuTP8SWFeyxqM8OyzT0GOzGhvcg+fCX4WP877FxhheHfc03mJsfKMLatQmLGTYrcfAdsosdrLVWLMXdB8j4Lc2mwfRSoZMEZNjPBKY8QL27jeNn68qk1VuBfH8=; _abck=4C820600C383E54905DA497D3AB1E339~-1~YAAQ3tscuC1ZHhN4AQAAgUY3JQWjD0Z5IbC1kufJdinq1C/PIiTPhlzMiS80stkQSLOHf39ZbrnRt5D9m5OExAr+XJKrR799CmLS3d26EF7KDEfZ3IpQ+2WlGpMXDjwNbOI1VpZOTM0BtLEjKaGKZ/lGrZErDacBHmonPNwXf9p7smJxihkPxyKDrzSvTks7zel8qMWmdbTHhIgZpsnTUr+269xLhI3xkV7ZuUFKMFGkoEkerWxGkUwHYpHPR8oiwfkep32W4TorIkJZdisbFAUddg4Ywr174ML3cgxYnf5xpaRTx/Id8K7s+5NimpCOKHBrgBP+hwf/qkwiTrHu8Rvfra6kAwf27ZVcZh92ACD8iiGHMw==~-1~-1~-1; bm_sv=10E30DF0EAFC7FC159560B8F1E882EA4~dze7LjZ4upxPiqJlO8Oszkl7DloCfIM9fOnLCbldBd0aXwPdaDu43rpsiRob2f+X2erMd7HGFbTIdEf2obGtU/1CXvj/3nl09lXgtiahucXyKDGa0SNHBv74V+vAhtnWY/v2mLBSUQNuzerEXs0hiZ7YTI6y+nGR+W5gWGpUB2o='
}

date = '2021-03-22'

def get_slots(date_opt):
    global date
    if date_opt:
        date = date_opt
    else:
        date = input('Enter the date you are searching for (format \'YYYY-MM-DD\'): ')
    print(date)
    request_url = "https://api.myturn.ca.gov/public/locations/a2ut0000006eUhiAAE/date/" + date + "/slots"
    response = requests.request("POST", request_url, headers=headers, json=payload)
    slots = []
    for slot in response.json()['slotsWithAvailability']:
        slots.append(slot['localStartTime'])

    if not slots:
        print('No times are available for ' + date + '. Please try another date.')
        get_slots(False)
    else:
        print('Available times are: ', slots)

def reserve(dose):
    slot = input('Enter the time slot you wish to reserve (format HH:MM:SS): ')
    request_payload = {
        'date': date,
        'dose': dose,
        'localStartTime': slot,
        'locationExtId': 'a2ut0000006eUhiAAE',
        'url': 'https://myturn.ca.gov/appointment-select',
        'vaccineData': 'WyJhM3F0MDAwMDAwMDFBZExBQVUiXQ==',
    }
    request_url = "https://api.myturn.ca.gov/public/locations/a2ut0000006eUhiAAE/date/" + date + "/slots/reserve"

    response = requests.request("POST", request_url, headers=headers, json=request_payload)
    return response.json()['reservationId']

final_request = ''
def code_issue(res):
    global final_request

    first_name = 'Julie' or input('First name: ')
    last_name = 'Zhou' or input('Last name: ')
    birthday = '1985-09-27' or input('Birth day (format YYYY-MM-DD): ')
    mothers_first_name = 'Alice' or input('Mother\'s first name: ')
    gender = 'Female' or input('Gender (Male/Female): ' )
    email = 'julie.yi.zhou@gmail.com' or input('Email: ')
    phone = '14156694685' or input('Phone (format 1112223333)')

    final_request = {
    	"personalDetails": [{
    		"id": "q.patient.firstname",
    		"value": first_name,
    		"type": "text"
    	}, {
    		"id": "q.patient.lastname",
    		"value": last_name,
    		"type": "text"
    	}, {
    		"id": "q.patient.suffix",
    		"type": "text"
    	}, {
    		"id": "q.patient.birthday",
    		"value": birthday,
    		"type": "date"
    	}, {
    		"id": "q.patient.mothersfirstname",
    		"value": mothers_first_name,
    		"type": "text"
    	}, {
    		"id": "q.patient.gender",
    		"value": gender,
    		"type": "single-select"
    	}, {
    		"id": "q.patient.race",
    		"value": "Chinese",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.ethnicity",
    		"value": "Not of Hispanic, Latino or Spanish origin",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.email",
    		"value": email,
    		"type": "email"
    	}, {
    		"id": "q.patient.mobile",
    		"value": "+1"+phone,
    		"type": "mobile-phone"
    	}, {
    		"id": "q.patient.address",
    		"value": "59 Iris Ave",
    		"type": "text"
    	}, {
    		"id": "q.patient.city",
    		"value": "San Francisco",
    		"type": "text"
    	}, {
    		"id": "q.patient.zip.code",
    		"value": "94118",
    		"type": "text"
    	}, {
    		"id": "q.patient.industry",
    		"value": "Government operations / community based essential functions",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.health.insurance",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.primary.carrier",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.primary.holder",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.policy.number",
    		"type": "text"
    	}, {
    		"id": "q.patient.primary.holder.first.name",
    		"type": "text"
    	}, {
    		"id": "q.patient.primary.holder.middle.name",
    		"type": "text"
    	}, {
    		"id": "q.patient.primary.holder.last.name",
    		"type": "text"
    	}, {
    		"id": "q.patient.primary.date.of.birth",
    		"type": "date"
    	}, {
    		"id": "q.patient.primary.relationship",
    		"type": "text"
    	}, {
    		"id": "q.patient.group.number",
    		"type": "text"
    	}, {
    		"id": "q.patient.workforce.number",
    		"type": "text"
    	}, {
    		"id": "q.patient.sick.today",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.serious.reaction",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.long.term.health.issue",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.immune.system.problem",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.familial.immune.system.issue",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.immune.system.medication",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.nervous.system.issue",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.blood.transfusion",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.pregnant",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.recently.vaccinated",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.allergies",
    		"value": "No",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.reasonable.accommodation",
    		"value": ["I do not require any accommodation during my appointment"],
    		"type": "multi-select"
    	}, {
    		"id": "q.patient.reasonable.accommodation.option",
    		"type": "single-select"
    	}, {
    		"id": "q.patient.reasonable.accommodation.information.text",
    		"type": "text"
    	}, {
    		"id": "q.patient.reasonable.accommodation.specify.text",
    		"type": "text"
    	}],
    	"locale": "en_US",
    	"context": {
    		"type": "reservation",
    		"value": res
    	},
    	"url": "https://myturn.ca.gov/verify-identity"
    }

    request_url = "https://api.myturn.ca.gov/public/public/onetimecode/issue"
    response = requests.request("POST", request_url, headers=headers, json=final_request)
    print(response.text)
    return response.json()['id']

def finalize(id):
    final_response['eligibilityQuestionResponse'] = [{
        "id": "q.screening.18.yr.of.age",
	    "value": ["q.screening.18.yr.of.age"],
	    "type": "multi-select"
    }, {
        "id": "q.screening.health.data",
	    "value": ["q.screening.health.data"],
	    "type": "multi-select"
    }, {
	    "id": "q.screening.privacy.statement",
	    "value": ["q.screening.privacy.statement"],
	    "type": "multi-select"
    }, {
	    "id": "q.screening.eligibility.age.range",
	    "value": "50-64",
	    "type": "single-select"
    }, {
	    "id": "q.screening.eligibility.industry",
	    "value": "Education and childcare",
	    "type": "single-select"
    }, {
	    "id": "q.screening.eligibility.county",
	    "value": "San Francisco",
	    "type": "single-select"
    }, {
	    "id": "q.screening.underlying.health.condition",
	    "value": "No",
	    "type": "single-select"
    }, {
	    "id": "q.screening.accessibility.code",
	    "type": "text"
    }]

    final_response['reservationIds'] = [res1, res2]
    del final_response['context']

    code = input('What is the six-digit code: ')
    final_response['oneTime'] = {
        'id': id,
        'code': code
    }

    request_url = "https://api.myturn.ca.gov/public/public/appointments"
    response = requests.request("POST", request_url, headers=headers, json=final_request)

    print(response.json()['confirmationCode'])

get_slots(False)
res1 = reserve(1)
date2 = (datetime.strptime(date, date_format) + timedelta(days=21)).strftime(date_format)
get_slots(date2)
res2 = reserve(2)
id = code_issue(res1)
finalize(id)
