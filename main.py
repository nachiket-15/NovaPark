#Parking management system done by 112103034 & 112103026 

# REQUIREMENTS 
from flask import Flask, render_template, request , session , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import datetime
import json
from flask_mail import Mail


#REGARDING BILL 
from io import BytesIO

from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas



#Open file name config.json in read mode using open() function and assign file objcet to variable c 
with open('config.json','r')as c:
    #Use json.load() function to load contents of file as json object and extract value associated with key params 
    params=json.load(c)["params"]


#This indicates that application is being run on local  deployment server
local_server=True


#It creates new instance of Flask class with name of current module as its argument 
app = Flask(__name__)

#Set secret key for flask application - It is used to securely sign & encrypt session cookies & other data that application stores on client side
app.secret_key = 'super-secret-key'



#Configure & initialize the instance of flask mail
#app.config.update() method updates applications configuration settings with specified values for email server & credentials 
app.config.update(
    #Mail server is selected to be Gmails smtp server
    MAIL_SERVER = 'smtp.gmail.com',
    #Port number connects to SMTP server , 465 is SSL encrypted SMTP port for gmail
    #SSL is secure sockets layer which is a protocol for establishing secure links
    MAIL_PORT = '465',
    #Boolean value that indicates whether to use SSL encryption
    MAIL_USE_SSL = True,
    #Boolean value that indicates whether to use TLS encryption-Transport Layer security
    MAIL_USE_TLS = False,
    #Email account used to send email messages 
    MAIL_USERNAME = 'developernachiket@gmail.com',
    #Password for email
    MAIL_PASSWORD=  'rssqpznwvusseaxr'
)

#After updated mail configuration settings , Mail() constructor is called Flask application instance 'app' as its argument
mail=Mail(app)


# configure the MySQL database
if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

db = SQLAlchemy(app) 

# CLASSES 
# CONTACTS SECTION

class Contacts(db.Model):
    __tablename__ = 'Contacts' # set the table name
    Serial_num = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Phone_no = db.Column(db.String(45), nullable=False)
    Message = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(30), nullable=True)
    Email = db.Column(db.String(35), nullable=False)


class AddVehicle(db.Model):
    __tablename__='AddVehicle' 
    Serial_num = db.Column(db.Integer, primary_key=True)
    Vehicle_name = db.Column(db.String(80), unique=False, nullable=False)
    Vehicle_num = db.Column(db.String(80), unique=False, nullable=False)
    Owner_name = db.Column(db.String(80), unique=False, nullable=False)
    Phone_no = db.Column(db.String(45), nullable=False)
    Total_slots = db.Column(db.String(45), nullable=False)
    Entry_time = db.Column(db.String(30), nullable=True)
    Vehicle_type=db.Column(db.String(80), unique=False, nullable=False)
    Date = db.Column(db.String(30), nullable=True)



# 

#







@app.route("/")
def home():
    return render_template("index.html")






@app.route("/about")
def about():
    return render_template("about.html")







# LOGIN SECTION 
@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    #If user is already logged in into session
    if ('user' in session and session['user']==params['admin_user']):
        return render_template("dashboard.html")
    
    if request.method=='POST':
        # Redirect to admin panel
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if(username==params['admin_user'] and userpass==params['admin_pass']):
            #Set the session variable
            session['user']=username
            return render_template("dashboard.html")

    return render_template("login.html")








now = datetime.datetime.now()
##

#SLOTS

no_of_slots=5



##
@app.route("/addvehicle", methods=['GET','POST'])
def add_vehicle():
    vehiclename = ''  # Initialize vehiclename with a default value

    # check if the AddVehicle table is empty
    if not AddVehicle.query.first():
    # if it's empty, add an initial entry with 10 available parking slots
        entry = AddVehicle(Vehicle_name='Test',Vehicle_num='Test', Phone_no='1234',Owner_name='Test' , Total_slots=no_of_slots ,Entry_time=0,Vehicle_type="CAR",Date=datetime.now()) 
        db.session.add(entry)
        db.session.commit()

    # Fetch the current number of available parking slots from the database
    total_slots = AddVehicle.query.with_entities(AddVehicle.Total_slots).first()[0]

    if request.method == 'POST':
        vehiclenum = request.form.get('vehiclenum')
        vehiclename = request.form.get('vehiclename')        
        phone = request.form.get('phone')        
        ownername = request.form.get('ownername') 
        entry_time=request.form.get('entrytime') 
        vehicle_type=request.form.get('vtype')


        if total_slots <= 0:
            message = "Sorry! All slots are filled. No more slots available for parking."
            return render_template("addvehicle.html", message=message)
        
        # Decrement the number of available parking slots and update the database
        updated_slots = total_slots - 1
        AddVehicle.query.filter(AddVehicle.Total_slots == total_slots).update({"Total_slots": updated_slots})
        db.session.commit() 

        entry = AddVehicle(Vehicle_name=vehiclename,Vehicle_num=vehiclenum, Phone_no=phone,Owner_name=ownername , Entry_time=entry_time, Total_slots=updated_slots,Vehicle_type=vehicle_type,Date=datetime.datetime.now()) 
        db.session.add(entry)
        db.session.commit() 

    # Fetch the updated number of available parking slots from the database
    total_slots = AddVehicle.query.with_entities(AddVehicle.Total_slots).first()[0]

    message=f"Vehicle added successfully , Go and park at slot number {total_slots+1}"
    return render_template("addvehicle.html", Total_slots=total_slots,message=message)










@app.route("/removevehicle", methods=['GET','POST'])
def remove_vehicle():
    # Fetch the current number of available parking slots from the database
    total_slots = AddVehicle.query.with_entities(AddVehicle.Total_slots).first()[0]

    if request.method == 'POST':
        vehiclenum = request.form.get('vehiclenum')

        # Find the entry for the given vehicle number in the database
        entry = AddVehicle.query.filter_by(Vehicle_num=vehiclenum).first()
        if entry is None:
            message = f"Vehicle {vehiclenum} not found in the parking lot"
            return render_template("removevehicle.html", message=message, Total_slots=total_slots)

        # Get the current time
        exit_time = int(request.form.get('exittime'))
        
        # Calculate the duration of the vehicle's stay
        entry_time =entry.Entry_time
        duration=(exit_time-entry_time)
        vtype=request.form.get('vtype')
        no_of_day=int(request.form.get('days'))


        # Calculate the bill amount based on the duration of stay

        if(vtype=="car"):
            rate_per_hour = 10
            day_charge=240

        elif(vtype=="bike"):
            rate_per_hour=5
            day_charge=120
        
        bill_amount =(duration * rate_per_hour) + (day_charge * no_of_day)

        # Increment the number of available parking slots and update the database
        updated_slots = total_slots + 1
        AddVehicle.query.filter(AddVehicle.Total_slots == total_slots).update({"Total_slots": updated_slots})
        db.session.commit()

        # Remove the entry from the database
        db.session.delete(entry)
        db.session.commit()







        # Generate a PDF bill for the user

        #buffer is an object of class BytesIO - BytesIO expects byte like objects & produces byte like objects - These objects are used for manual control over handling of text data

        buffer = BytesIO()

        #canvas is a module from reportlab.pdf gen library that allows us to create pdf 

        #into that module ive accessed Canvas class and provided to it buffer object and given a parameter of pagesize as letter - which is the standard 8.5 x 11 inch paper size used in the US.

        #using these we created a object named p
        p = canvas.Canvas(buffer, pagesize=letter)

        # p.drawString() method is used to write header and details of parking bills on PDF canvas 
        # This method takes 3 arguments - x,y co-ordinates of where to place text on canvas & the actual text to write  
        p.drawString(100, 700, "VEHICLE PARKING BILL")
        p.drawString(100, 670, f"Vehicle Number: {vehiclenum}")
        p.drawString(100, 640, f"Entry Time: {entry_time}:00 HRS")
        p.drawString(100, 610, f"Exit Time: {exit_time}:00 HRS")
        p.drawString(100, 580, f"Duration of Stay:{no_of_day} days {duration} hours")
        p.drawString(100, 550, f"Rate per hour: {rate_per_hour}")
        p.drawString(100, 520, f"Bill Amount: {bill_amount} INR")

        # Save the PDF bill to a buffer and send it as a response
        p.showPage()
        p.save()

        #Set buffers position to beginning 
        buffer.seek(0)

        #make_responce() method is used to create Flask responce object containing the pdf data in buffer 
        response = make_response(buffer.getvalue())

        #Responce objects headers are set to indicate that it contains a pdf file
        response.headers["Content-Disposition"] = "attachment; filename=parkingbill.pdf"
        response.headers["Content-Type"] = "application/pdf"

        #Finally the responce object is returned from flask view function , sending pdf file to users browser for download
        return response

    return render_template("removevehicle.html", Total_slots=total_slots)







@app.route("/contact", methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')        
        phone = request.form.get('phone')        
        message = request.form.get('message')  

        entry = Contacts(Name=name, Email=email, Phone_no=phone, Message=message, Date=datetime.now()) 
        db.session.add(entry)
        db.session.commit()  
        mail.send_message('New message from '+ name+'parking management system',sender=email,recipients=[params['gmail-user']],
                        body=message+"\n\nContact Number: "+phone)   

    return render_template("contact.html")







@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')






@app.route("/index")
def homee():
    return render_template("index.html")







@app.route("/details")
def details():
    return render_template("details.html")








@app.route("/parkedvehicles", methods=['GET','POST'])
def parkedvehicles():
    if ('user' in session and session['user']==params['admin_user']):
        posts=AddVehicle.query.all();
        return render_template("parkedvehicles.html",posts=posts,params=params)
    
    if request.method=='POST':
        # Redirect to admin panel
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if(username==params['admin_user'] and userpass==params['admin_pass']):
            #Set the session variable
            session['user']=username
            posts=AddVehicle.query.all();
            return render_template("parkedvehicles.html",posts=posts,params=params)

        

    



if __name__ == '__main__':
    app.run(debug=True)
