import json
import requests
import time


# Set conf to environment from config.json (test, android or ios)
with open('config.json') as json_data:
    data = json.load(json_data)

cf_site = data['site']
cf_login = data['login']
cf_password = data['password']
json_header = {'Accept': 'application/json'}


search_label = raw_input("Enter the Label to search: \n")

def get_cases_by_label(label_name):
    search_params = {'labels': label_name}
    r = requests.get(cf_site + '/api/v2/cases/search', headers=json_header, params=search_params, auth=(cf_login, cf_password))
    js = json.loads(r.content)

    # print(json.dumps(js, indent=2))

    message_links = []
    for case in js['_embedded']['entries']:
        message_links.append(case['_links']['message']['href'])
    print(message_links)

    messages = []
    for link in message_links:
        r = requests.get(cf_site + link, headers=json_header,auth=(cf_login, cf_password))
        js = json.loads(r.content)

        try:
            messages.append(js['body'])
        except KeyError:
            print(json.dumps(js, indent=2))

    trimmed_messages = []

    counter = 0
    for message in messages:
        first_part_of_message = message\
            .split('-App-')[0]\
            .split('--')[0] \
            .split('Thank you')[0] \
            .split('Kind regards')[0] \
            .split('Extra Data:')[0] \
            .split('System information:')[0] \
            .split('Sent from my iPad')[0] \
            .split('Regards')[0] \
            .split('Extra Data:')[0] \
            .split('The diagnostic info below will help us with resolving your problem:')[0] \
            .split('The information below will help us to better understand your query:')[0]

        counter += 1

        trimmed_messages.append(first_part_of_message.strip())
    print counter

    counter1 = str(counter)

    output = open('Feedback.txt', 'w')
    output.write("FEEDBACK RESPONSE FOR LABEL (" + label_name.upper() + ") - " + time.strftime("%d/%m/%Y %H:%M:%S"))
    output.write('\n')
    output.write('(Number of cases found = ' + counter1 + ')')
    output.write('\n================================================================================\n')
    output.write('\n')

    for finished_message in trimmed_messages:
        output.write(finished_message.encode('utf-8'))
        output.write('\n')
        output.write('*' * 40 + '\n')
        output.write('\n')

    output.close()

    print ('\n')
    print 'Search completed - please check text file!'
    print ('\n')


get_cases_by_label(search_label)

#INA - Offline reading problems
#ANA - Offline reading problems
#ANA - General feedback
#IDE - Missing crosswords on Mondays

