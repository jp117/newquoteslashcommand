import os
import credentials

from flask import abort, Flask, jsonify, request

app = Flask(__name__)

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
            text='job name/address is ' + datasplitter()[0] + ', quote was for ' + datasplitter()[1] + ' dollars')
    else:
        return jsonify(
            response_type='in_channel',
            text='you did not input in the quote in the proper format')