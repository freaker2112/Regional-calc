import math
from scipy.special import erfinv
import tbaapiv3client
from pprint import pprint
from tbaapiv3client.rest import ApiException
import json
from operator import itemgetter


with open('creds', 'r') as file:
    creds = file.read()


team_key = input("please enter the TBA team key")

configuration = tbaapiv3client.Configuration(
    host = "https://www.thebluealliance.com/api/v3",
    api_key = {
        'X-TBA-Auth-Key': creds
    }
)



with tbaapiv3client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tbaapiv3client.EventApi(api_client)
    year = 2024 # int | Competition Year (or Season). Must be 4 digits.
    try:
        api_response = api_instance.get_team_events_by_year_simple(team_key, year)
        #print(api_response)
    except ApiException as e:
        print("Exception when calling EventApi->get_team_events_by_year_simple: %s\n" % e)
        quit()


relevant_events = [event for event in api_response if event.event_type == 0] 


eventkey1 = ((relevant_events[0]).key)
eventkey2 = ((relevant_events[1]).key)

with tbaapiv3client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tbaapiv3client.EventApi(api_client)
    try:
        event_api_response1 = api_instance.get_team_event_status(team_key, eventkey1)
        #pprint(event_api_response1)
    except ApiException as e:
        print("Exception when calling EventApi->get_event: %s\n" % e)
        quit()
with tbaapiv3client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = tbaapiv3client.EventApi(api_client)
    try:
        event_api_response2 = api_instance.get_team_event_status(team_key, eventkey2)
        #pprint(event_api_response2)
    except ApiException as e:
        print("Exception when calling EventApi->get_event: %s\n" % e)
        quit()



qualteams1=(event_api_response1.qual.num_teams)
qualteams2=(event_api_response2.qual.num_teams)

qualrank1=(event_api_response1.qual.ranking.rank)
qualrank2=(event_api_response2.qual.ranking.rank)

if event_api_response1.alliance_status_str != "--":
    draft1=(event_api_response1.alliance.pick)
    if event_api_response1.alliance.pick == 0:
        draft1=(event_api_response1.alliance.number)
if event_api_response2.alliance_status_str != "--":
    draft2=(event_api_response2.alliance.pick)
    if event_api_response2.alliance.pick == 0:
        draft2=(event_api_response2.alliance.number)

playwon=3
won=3

if event_api_response1.alliance_status_str != "--":
    if event_api_response1.playoff.status == "won":
        place1=1
    if event_api_response1.playoff.status == "eliminated" and event_api_response1.playoff.level == "f":
        place1=2
    if event_api_response1.playoff.status == "eliminated" and event_api_response1.playoff_status_str == "<b>Eliminated in the Double Elimination Bracket (Round 5)</b> with a playoff record of <b>2-2-0</b>":
        place1=3
    if event_api_response1.playoff.status == "eliminated" and event_api_response1.playoff_status_str == "<b>Eliminated in the Double Elimination Bracket (Round 4)</b> with a playoff record of <b>2-2-0</b>":
        place1=4
if event_api_response1.alliance_status_str == "--":
    place1=0
    draft1=17
    fwins1=0


if event_api_response2.alliance_status_str != "--":
    if event_api_response2.playoff.status == "won":
        place2=1
    if event_api_response2.playoff.status == "eliminated" and event_api_response2.playoff.level == "f":
        place2=2
    if event_api_response2.playoff.status == "eliminated" and event_api_response2.playoff_status_str == "<b>Eliminated in the Double Elimination Bracket (Round 5)</b> with a playoff record of <b>2-2-0</b>":
        place2=3
    if event_api_response2.playoff.status == "eliminated" and event_api_response2.playoff_status_str == "<b>Eliminated in the Double Elimination Bracket (Round 4)</b> with a playoff record of <b>2-2-0</b>":
        place2=4
if event_api_response2.alliance_status_str == "--":
    place2=0
    draft2=17
    fwins2=0



if place1==1 or place1==2:
    placepts1=20
elif place1 == 3:
    placepts1 = 13
elif place1 == 4:
    placepts1 = 7
elif place1 == 0:
    placepts1 = 0

if place2==1 or place2==2:
    placepts2=20
elif place2 == 3:
    placepts2 = 13
elif place2 == 4:
    placepts2 = 7
elif place2 == 0:
    placepts2 = 0

if event_api_response1.alliance_status_str != "--":
    fwins1=(event_api_response1.playoff.current_level_record.wins)
if event_api_response2.alliance_status_str != "--":
    fwins2=(event_api_response2.playoff.current_level_record.wins)

awardpts=10

agepts=0

qualpts1 = erfinv((qualteams1-2*qualrank1+2)/(1.07*qualteams1))*((10)/(erfinv(1/1.07)))+12
qualpts2 = erfinv((qualteams2-2*qualrank2+2)/(1.07*qualteams2))*((10)/(erfinv(1/1.07)))+12

DEpts = ((playwon/won)*placepts1+(fwins1*5))+((playwon/won)*placepts2+(fwins2*5))

qualpts = qualpts1+qualpts2
draft = (17-draft1) + (17-draft2)


regional_points = qualpts + (17-draft) + DEpts + awardpts + agepts



print("Regional Pool Points:")
print(round(regional_points))
