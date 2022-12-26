import datetime
import requests
import pytz
import os 

from pytz import timezone
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('RDSDATABASEURI')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

def current_time_Istanbul():

    utc_now = datetime.datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')

    return aware_date.astimezone(turkey)

def send_msg(text,chat_id):

    token = os.environ.get('TELEBOTTOKEN') 
    
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text 
    requests.get(url_req)

class TblClients(db.Model):

	nClientId = db.Column(db.Integer, primary_key=True)
	codeStatus = db.Column(db.String(100), nullable=False)
	dtLastVisit = db.Column(db.DateTime(timezone=True),default=current_time_Istanbul(), onupdate=current_time_Istanbul(), nullable=False)
	chatId = db.Column(db.Integer, nullable=False)
	results = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Warner(status = {codeStatus}, lastVisit = {dtLastVisit})"

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("codeStatus", type=str, help="Status of the code", required=True)
user_put_args.add_argument("results", type=str, help="Results of the code", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("codeStatus", type=str, help="Status of the code", required=True)
user_update_args.add_argument("results", type=str, help="Results of the code", required=True)

resource_fields = {
	'nClientId': fields.Integer,
	'codeStatus': fields.String,
	'dtLastVisit': fields.DateTime,
	'chatId': fields.Integer,
	'results': fields.String
}

class Warner(Resource):

	@marshal_with(resource_fields)
	def get(self, user_id):

		result = TblClients.query.filter_by(nClientId=user_id).first()

		if not result:
			abort(404, message="Could not find user with that id")

		return result


	@marshal_with(resource_fields)
	def patch(self, user_id):

		args = user_update_args.parse_args()
		result = TblClients.query.filter_by(nClientId=user_id).first()

		if not result:
			abort(404, message="User doesn't exist, cannot update! Please register via Telegram")

		if args['codeStatus']:
			result.codeStatus = args['codeStatus']
		if args['results']:
			result.results = args['results']

		db.session.commit()

		return result


	def post(self, user_id):

		patch_result = self.patch(user_id)
		codeStatus = patch_result['codeStatus']
		result = patch_result['results']
		chatId = str(patch_result['chatId'])
		text = f"Dear Warner-Me user, Your code status is updated as {codeStatus} with results: {result}"
		send_msg(text,chatId)

api.add_resource(Warner, "/warnMe/<int:user_id>")

if __name__ == "__main__":
	
	app.run(debug=False)