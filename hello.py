"""Cloud Foundry test"""
from flask import Flask,render_template,request
import os
import json
import couchdb

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/')
def hello_world():
    p="<html><head><h1>Enter your user name</h1><br><form action='connect' method='POST'>"
    p+="Fname<input type='text' name='fnm'><br>Lname<input type='text' name='lnm'><input type='submit'></form></head></html>"
    return p
    #return render_template("temps.html",name="Boss")

@app.route('/connect',methods=['GET','POST'])
def cloud_connt():
    #Acquire the user name and password
    couchInfo = json.loads(os.environ['VCAP_SERVICES'])['cloudantNoSQLDB'][0]
    creds=couchInfo['credentials']
    user=creds['username']
    passw=creds['password']
    url=creds['url']
    #Create a instance of the cloudant database
    couchint=couchdb.Server(url)
    couchint.resource.credentials=(user,passw)

    #accessing a db
    #db=couchint.create('demotext') for creating a db
    db=couchint['demotext']
    
    fnm=request.form['fnm']
    lnm=request.form['lnm']

    doc_id,doc_rev=db.save({
        'fname':fnm,
        'lname':lnm
        })
    
    p="<html><body><h3>Data stored in the databse</h3><form action='view' method='post'><input type='hidden' value=db name='dbs'><input type='submit'></form></body></html>"
    return p
@app.route('/view',methods=['POST'])
def viewing():
    #Acquire the user name and password
    couchInfo = json.loads(os.environ['VCAP_SERVICES'])['cloudantNoSQLDB'][0]
    creds=couchInfo['credentials']
    user=creds['username']
    passw=creds['password']
    url=creds['url']
    #Create a instance of the cloudant database
    couchint=couchdb.Server(url)
    couchint.resource.credentials=(user,passw)

    #accessing a db
    #db=couchint.create('demotext') for creating a db
    db=couchint['demotext']

    pst="<html><body><h3>Contents of a Database</h3>"
    for doc in db.view('docviews/generic'):
        pst+=str(doc.key)+":"+str(doc.value)+"<br>"
    pst+="</body></html>"
    return pst
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
