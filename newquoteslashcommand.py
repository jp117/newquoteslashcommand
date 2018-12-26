import os
from os import path
import credentials
import json
import datetime 

from flask import abort, Flask, jsonify, request

app = Flask(__name__)

#gets the year 
def year():
    mny = datetime.datetime.now()
    return mny.strftime("%Y")


def data_file():
    filename = str(year())
    with open(filename+'_quotedata.json', 'a+') as outfile:
        json.dump(quote_data(), outfile)

#func write json data 
def quote_data():
    data = {}
    data['quote'] = []
    data['quote'].append(
        {
        'salesman':request.form['user_name'],
        'job name': datasplitter()[0],
        'amount': '{:,}'.format(int(datasplitter()[1]))
        })
    return data

def is_request_valid(request):
    is_token_valid = request.form['token'].strip()  == credentials.newquote_token
    is_team_id_valid = request.form['team_id'].strip() == credentials.team_id
    return is_token_valid and is_team_id_valid

def datasplitter():
    text = request.form['text']
    return text.split('::')

@app.route('/newquote', methods=['POST'])
def newquote():
    if not is_request_valid(request):
        abort(400)
    #check if text entered is in the proper format with a ::
    if "::" in request.form['text'] and datasplitter()[1].strip().isdigit():
        data_file()
        return jsonify(
            response_type='in_channel',
            text=request.form['user_name'] + ' quoted ' + datasplitter()[0] + '", for $' + '{:,}'.format(int(datasplitter()[1])) + ' dollars')
    else:
        return jsonify(
            response_type='in_channel',
            text='You did not input the quote in the correct format.  Make sure you type the name and/or address followed by \"::\" with the dollar amount in digits only')