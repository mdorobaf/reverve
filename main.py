from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "\x82\xdc\x15\xc6\x179m\xbf}SxM7}\xb0o\xa2\x87\xfd\t;3\xf6\xc4"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.sqlite'
db = SQLAlchemy(app)
app.app_context().push()

# Define the Table model
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_reserved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Table {self.number}>'

class Reserve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    
    

# Create the database tables
db.create_all()

# Route to display the reservation form
@app.route('/')
def index():
    tables = Table.query.filter_by(is_reserved=False).all()
    return render_template('index.html', tables=tables)

@app.route('/create_table',methods=['POST'])
def create_table():
    number = request.form.get('number')
    capacity = request.form.get('capacity')
    
    table = Table(number=number, capacity=capacity)
    db.session.add(table)
    db.session.commit()
    
    return redirect(url_for('index'))

# Route to handle the reservation request
@app.route('/reserve', methods=['POST'])
def reserve():
    table_id = request.form.get('table_id')
    name = request.form.get('name')
    date = request.form.get('date')
    time = request.form.get('time')
    phone = request.form.get('phone')
    
    table = Table.query.get(table_id)
    if table:
        table.is_reserved = True
        
        reserve = Reserve(table_id=table_id ,name=name ,date=date ,time=time ,phone=phone)
        db.session.add(reserve)
        
        db.session.commit()
        
        flash("your request saved")
        return redirect(url_for('index'))
    return 'Table not found', 404

if __name__ == '__main__':
    app.run(debug=True)
