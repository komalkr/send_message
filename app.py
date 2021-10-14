from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'my_db',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
db.create_all()

migrate = Migrate(app, db)


@app.route('/')
def home():
    return """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>SMS Messenger</title>
            </head>
            <body>
            <h1>SMS Messenger</h1>
            <form action="message" method='Post'>
                <label>Enter Sender Number </label>
                <input type="text" name="senderPhone" value="" required>
                <label>Enter Recipient Number</label>
                <input type="text" name="receiverPhone" value="" required>
                <label>Enter Message </label>
                <input type="text" name="messageText" value="" required>
                <input type="submit" value="Submit">
            </form>  
            </body>
            </html>
    """


@app.route('/message', methods=['POST', 'GET'])
def handle_message():
    from model import Intent
    if request.method == 'POST':
        if request.form:
            data = request.form
            receiverPhone = data['receiverPhone'].split(',')
            if len(receiverPhone)>0:
                for reciever in receiverPhone:
                    intent = Intent(senderPhone=data['senderPhone'], receiverPhone=reciever, messageText=data['messageText'])
                    db.session.add(intent)
                    db.session.commit()
            return {"message": f"message {intent.receiverPhone} has been sent successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        intents = Intent.query.all()
        results = [
            {
                "senderPhone": intent.senderPhone,
                "receiverPhone": intent.receiverPhone,
                "messageText": intent.messageText,
                "time": intent.timestamp
            } for intent in intents]

        return {"count": len(intents), "results":results}


@app.route('/show_message/', methods=['GET'])
def show_message():
    from model import Intent
    intents = Intent.query.all()
    results = [
        {
            "senderPhone": intent.senderPhone,
            "receiverPhone": intent.receiverPhone,
            "messageText": intent.messageText,
            "time": intent.timestamp
        } for intent in intents]
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run()
