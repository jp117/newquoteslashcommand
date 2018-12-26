import os
import credentials
import json
import datetime 
from flask import abort, Flask, jsonify, request

app = Flask(__name__)

#Checks if the datafile exists, if it does not, creates it.  Dumps the data into the file
def data_file():
    with open(str(datetime.datetime.today().year)+'_quotedata.json', 'a+') as outfile:
        json.dump(quote_data(), outfile, indent=4)
        #indent=4 pretifies json code to make it more readable

#Writes JSON data to be dumped into the data_file
def quote_data():
    data = {}
    data['quote'] = []
    data['quote'].append(
        {
        'date': str(datetime.datetime.today().strftime("%m/%d/%Y")),
        'salesman':request.form['user_name'],
        'job name': datasplitter()[0],
        'amount': '{:,}'.format(int(datasplitter()[1]))
        })
    return data

#Checks that my credentials are correct for my slack channel
def is_request_valid(request):
    is_token_valid = request.form['token'].strip()  == credentials.newquote_token
    is_team_id_valid = request.form['team_id'].strip() == credentials.team_id
    return is_token_valid and is_team_id_valid

#Divides the data entered into the textbox into the two parts by the divider key set in Slack 
def datasplitter():
    text = request.form['text']
    return text.split('::')

#If someone enters the app route /newquote (deployed to a website/newquote), execute the function below 
@app.route('/newquote', methods=['POST'])
def newquote():
    #Check if credentials match
    if not is_request_valid(request):
        abort(400)
    #check if text entered is in the proper format with a ::
    if "::" in request.form['text'] and datasplitter()[1].strip().isdigit():
        data_file()
        return jsonify(
            response_type='in_channel',
            text=request.form['user_name'] + ' quoted ' + datasplitter()[0] + '", for $ ' + '{:,}'.format(int(datasplitter()[1])) + ' dollars')
    #Give error message because data was wrong    
    else:
        return jsonify(
            response_type='in_channel',
            text='You did not input the quote in the correct format.  Make sure you type the name and/or address followed by \"::\" with the dollar amount in digits only')