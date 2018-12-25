import os
import credentials
#import locale #don't think this is needed
import json
import datetime 

from flask import abort, Flask, jsonify, request

app = Flask(__name__)

#func get the month and the year

#func check for a file month + year .txt, if one doesn't exist, make one

#func write json data 

# func dump json data to correct file

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
        return jsonify(
            response_type='in_channel',
            text='job name/address is "' + datasplitter()[0] + '", quote was for $' + '{:,}'.format(int(datasplitter()[1])) + ' dollars')
    else:
        return jsonify(
            response_type='in_channel',
            text='you did not input in the quote in the proper format')