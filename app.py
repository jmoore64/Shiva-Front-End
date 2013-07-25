from flask import abort,json,jsonify,send_file,session,Response
from __init__ import app,db
import os,random,sys,urllib,urllib2
from re import findall
from models import User

@app.route('/user=<name>/pass=<passwd>')
def main_login(name=None, passwd=None):
	if "token" in session:
		return "Already Logged in as %s" % session['user']
	
	if name and passwd:
		try:
			u = User.query.get(name)
			if u.password == passwd: #and u.token==-1:
				
				x = random.getrandbits(16)
				while User.query.filter_by(token=x).first():
					x = random.getrandbits(16)	
#				session["token"] = x
#				session["user"] = name
#				u.token = session["token"]
				u.token = x
				db.session.commit()
#				return jsonify(port=u.port,token=session["token"])
				return jsonify(port=u.port,token=u.token)
		except:
			print sys.exc_info()

	abort(401)

@app.route('/token=<t>/logout')
def main_logout(t=None):
#	if "token" in session:
#		n = session["user"]
	if t:
		u = User.query.filter_by(token=t).first()
		if u:
			n = u.username
			u.token = -1
			db.session.commit()
			return "Completed Logout Procedures, %s" %n
#		session.clear()
		
	abort(401)
	
@app.route('/token=<t>/artists')
def main_artists(t=None):
	if t:
#		u = User.query.filter_by(token=session['token']).first()
		u = User.query.filter_by(token=t).first()
		if u:
			port = u.port
			x = json.loads(str(urllib2.urlopen("http://xstream.cloudapp.net:%i/artists"%port).read()))
			return Response(json.dumps(x),mimetype='application/json')
	abort(401)


@app.route('/token=<t>/albums/artist=<num>')
def main_albums(t = None, num = None):
	if t and num:
		u = User.query.filter_by(token=t).first()
		if u:
			port = u.port
			x = json.loads(str(urllib2.urlopen("http://xstream.cloudapp.net:%i/albums?artist=%s"%(port,num)).read()))
			return Response(json.dumps(x),mimetype='application/json')
	abort(401)	

@app.route('/token=<t>/tracks/album=<num>')
def main_tracks(t = None, num = None):
	if t and num:
		u = User.query.filter_by(token=t).first()
		if u:
			port = u.port
			x = json.loads(str(urllib2.urlopen("http://xstream.cloudapp.net:%i/tracks?album=%s"%(port,num)).read()))
			return Response(json.dumps(x),mimetype='application/json')
	abort(401)

@app.route('/token=<t>/track/url=<path:url>')
def main_track(t = None, url=None):
	if t and url:
		u = User.query.filter_by(token=t).first()
		if u:
			base = os.path.join(os.getcwd(),os.path.dirname(__file__),"temp",u.username)
			if not os.path.exists(base):
				os.mkdir(base)
			urllib.urlretrieve(url,os.path.join(base,"tmp.mp3"))
			return send_file(os.path.join(base,"tmp.mp3"))
		

	abort(401)
	


if __name__ == '__main__':
	try:
        	port = int(sys.argv[1])
    	except:
        	port = 9001
    	app.run(host='0.0.0.0', port=port, debug=True)
