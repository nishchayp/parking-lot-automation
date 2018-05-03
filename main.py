from flask import Flask, render_template, request, flash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired
from flaskext.mysql import MySQL
import math

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'abc'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'PLAUser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'PLAPassword'
app.config['MYSQL_DATABASE_DB'] = 'PLADb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class ReusableForm(Form):
	first_name = StringField('First Name:', validators=[DataRequired()])
	last_name = StringField('Last Name:', validators=[DataRequired()])
	mobile_no = StringField('Mobile Number:', validators=[DataRequired(), validators.Length(10)])
	vehicle_no = StringField('Vehicle Number:', validators=[DataRequired(), validators.Length(13)])
	vehicle_type = StringField('Vehicle Type:', validators=[DataRequired()])


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/newEntry', methods=['GET', 'POST'])
def newEntry():
	
	form = ReusableForm(request.form)
	
	if request.method == 'POST' and form.validate():

		con = mysql.connect()
		cursor = con.cursor()

		sql_stmt1 = "INSERT INTO customer VALUES('{}', '{}', {}, '{}', '{}')".format(request.form['first_name'], request.form['last_name'], request.form['mobile_no'], request.form['vehicle_no'], request.form['vehicle_type'])
			
		sql_stmt2 = "UPDATE parking_slot SET isOccupied = 'Y' WHERE parking_slot_id = '{}'".format(request.form['given_slot'])

		sql_stmt3 = "INSERT INTO slot(parking_slot_id, vehicle_number) VALUES('{}', '{}')".format(request.form['given_slot'], request.form['vehicle_no']);

		try:
			cursor.execute(sql_stmt1)
			con.commit()
			cursor.execute(sql_stmt2)
			con.commit()
			cursor.execute(sql_stmt3)
			con.commit()
			flash('Customer added!')
		except Exception as e:
			flash(e)
		finally:
			con.close()

		return render_template('new-entry.html', form=form)
	
	flash('Welcome! Please enter customer details.')


	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT parking_slot_id FROM parking_slot WHERE isOccupied = 'N' ORDER BY parking_slot_id DESC"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	return render_template('new-entry.html', form=form, results=results)


@app.route('/queries')
def queries():
	return render_template('queries.html')

@app.route('/showAll')
def showAll():

	title = "Show all the customers"
	description = "Displays details of all the customers in the parking lot"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM customer"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['First Name', 'Last Name', 'Mobile No', 'Vehicle No', 'Vehicle Type']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)


@app.route('/showAllRate')
def showAllRate():

	title = "Show all the Rates per hour"
	description = "Displays details of rates"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM rate"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['Basic Cost','Vehicle NO']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)




@app.route('/showAllSp')
def showAllSp():

	title = "Show all the special customers"
	description = "Displays details of all the special customers in the parking facility"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT  * FROM customer WHERE vehicle_number IN(SELECT  vehicle_number FROM special);"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['First Name', 'Last Name', 'Mobile No', 'Vehicle No', 'Vehicle Type']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)	

@app.route('/showAllRg')
def showAllRg():

	title = "Show all the regular customers"
	description = "Displays details of all the regular customers in the parking facility"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT  * FROM customer WHERE vehicle_number NOT IN (SELECT  vehicle_number FROM special);"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['First Name', 'Last Name', 'Mobile No', 'Vehicle No', 'Vehicle Type']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)		

@app.route('/showAllP')
def showAllP():

	title = "Show all the parking slots"
	description = "Displays details of all the parking slots in the parking lot"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM parking_slot"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['Parking Slot ID', 'Floor No', 'Parking Type', 'Is Occupied']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)

@app.route('/showAllPA')
def showAllPA():

	title = "Show all the available parking slots"
	description = "Displays details of all the available parking slots in the parking lot"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM parking_slot where Isoccupied = 'N'"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['Parking Slot ID', 'Floor No', 'Parking Type', 'Is Occupied']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)




@app.route('/showAllByFloor/<floor>')
def showAllByFloor(floor):

	title = "Show all parking spots"
	description = "Displays details of all the available parking spots in the parking lot"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM parking_slot where floor_no = " + floor
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['Parking Slot ID', 'Floor No', 'Parking Type', 'Is Occupied']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)


@app.route('/showAllByFloorA/<floor>')
def showAllByFloorA(floor):

	title = "Show all parking spots"
	description = "Displays details of all the available parking spots in the parking lot"

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT * FROM parking_slot where isOccupied = 'N' and floor_no = " + floor
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	table_headings=['Parking Slot ID', 'Floor No', 'Parking Type', 'Is Occupied']

	return render_template('query-result.html', title=title, description=description, sql_stmt=sql_stmt, results=results, table_headings=table_headings)


@app.route('/generateTicket', methods=['GET', 'POST'])
def generateTicket():

	cursor = mysql.connect().cursor()
	
	sql_stmt = "SELECT vehicle_number FROM customer"
	
	cursor.execute(sql_stmt)
	results = cursor.fetchall()

	return render_template('generate-ticket.html', results=results)

@app.route('/getTicket', methods=['POST'])
def getTicket():


	con = mysql.connect()
	cursor = con.cursor()

	sql_stmt1 = "SELECT * FROM customer WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])
	
	cursor.execute(sql_stmt1)
	customer_details = cursor.fetchall()

	table_headings_customer=['FIRST NAME', 'LAST NAME', 'MOBILE NO', 'VEHICLE NO', 'VEHICLE TYPE']

	sql_stmt2 = "SELECT parking_slot_id FROM slot WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])
	
	cursor.execute(sql_stmt2)
	psi_result = cursor.fetchall()
	
	parking_slot_id = psi_result[0][0]
	print(parking_slot_id)

	sql_stmt3 = "SELECT entry_date_time FROM slot WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])
	
	cursor.execute(sql_stmt3)
	edt_result = cursor.fetchall()
	
	t_entry = edt_result[0][0]
	print(t_entry)


	sql_stmt_sf = "INSERT INTO parking_slip(parking_slot_id, t_entry, vehicle_number) VALUES('{}', '{}', '{}')".format(parking_slot_id, t_entry, request.form['vehicle_no'])

	cursor.execute(sql_stmt_sf)
	con.commit()

	sql_stmt4 = "SELECT t_entry, t_exit FROM parking_slip WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])
	
	cursor.execute(sql_stmt4)
	ee_result = cursor.fetchall()

	t_en = ee_result[0][0]
	print(t_en)

	t_ex = ee_result[0][1]
	print(t_ex)


	sql_stmt5 = "SELECT TIME_TO_SEC(TIMEDIFF( '{}', '{}')) / 3600".format(t_ex,t_en)
	
	cursor.execute(sql_stmt5)
	td_result = cursor.fetchall()

	print(td_result[0][0])
	hours_spent = math.ceil(td_result[0][0])
	print(hours_spent)


	sql_stmt6 = "UPDATE parking_slip SET discount = 5 WHERE vehicle_number IN (SELECT vehicle_number FROM special)"

	cursor.execute(sql_stmt6)
	con.commit()


	sql_stmt7 = "SELECT basic_cost FROM rate WHERE vehicle_type = (SELECT vehicle_type FROM customer WHERE customer.vehicle_number = '{}')".format(request.form['vehicle_no'])

	cursor.execute(sql_stmt7)
	bc_result = cursor.fetchall()

	basic_cost = bc_result[0][0]
	print(basic_cost)

	sql_stmt_pf = "UPDATE parking_slip SET basic_cost = {}".format(basic_cost)

	cursor.execute(sql_stmt_pf)
	con.commit()

	sql_stmt8 = "SELECT discount FROM parking_slip WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])

	cursor.execute(sql_stmt8)
	disc_result = cursor.fetchall()

	discount = int(disc_result[0][0])
	print(discount)

	total_cost = (int(hours_spent) * int(basic_cost)) * (1.0 - (int(discount)/100))
	print(total_cost) 


	sql_stmt_f = "UPDATE parking_slip SET total = {}".format(total_cost)

	cursor.execute(sql_stmt_f)
	con.commit()

	sql_stmt_clean0 = "UPDATE parking_slip SET t_entry = '{}' WHERE vehicle_number = '{}'".format(t_entry, request.form['vehicle_no'])
	print(t_entry)

	cursor.execute(sql_stmt_clean0)
	con.commit()
	
	sql_stmt_last = "SELECT * FROM parking_slip WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])
	
	cursor.execute(sql_stmt_last)
	slip_details = cursor.fetchall()

	table_headings_slip=['ID', 'SLOT', 'VEHICLE NO', 'ENTRY TIME', 'EXIT TIME', 'COST/HR', 'DISCOUNT(%)', 'AMOUNT PAYABLE']


	sql_stmt_clean1 = "UPDATE parking_slot SET isOccupied = 'N' WHERE parking_slot_id = (SELECT parking_slot_id FROM slot WHERE vehicle_number = '{}')".format(request.form['vehicle_no'])

	cursor.execute(sql_stmt_clean1)
	con.commit()

	sql_stmt_clean2 = "DELETE FROM customer WHERE vehicle_number = '{}'".format(request.form['vehicle_no'])

	cursor.execute(sql_stmt_clean2)
	con.commit()


	return render_template('ticket.html', customer_details=customer_details, table_headings_customer=table_headings_customer, slip_details=slip_details, table_headings_slip=table_headings_slip)



if __name__ == '__main__':
	app.run(debug=True)
