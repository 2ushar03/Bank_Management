from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    session,
    flash
)
from datetime import datetime as dt
from flask_mysqldb import MySQL
from form import (customerScreen, updateCustomer, 
deleteCustomer,withdrawMoney,
createaccount,deleteAccount,depositMoney,

customerStatusSearch,
accountStatusSearch,
accountSum,
login,
transferMoney)
from flask_mongoengine import MongoEngine
from config import Config
import sys
from model import Customer_Account,Transactions


app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)


@app.route('/home',methods =['GET','POST'] )
def home():
    return render_template("base.html")

@app.route('/logout',methods =['GET','POST'] )
def logout_out():
    form = login()
    session['id']=False
    return redirect(url_for('login_enter'))


@app.route('/', methods =['GET','POST'] )
def login_enter():
    form = login()
    username  =form.username.data
    password = form.password.data
    print(username,file=sys.stderr)
    
    if username=="admin" and password=="admin":
        session["id"]=1
        return render_template("base.html")

    return render_template("login.html",form = form)

#-------------------------------------Customer Management --------------------------------

@app.route('/createcustomer', methods=['GET','POST'])

def customer():
    form = customerScreen()
    if form.validate_on_submit():
        ssn_id = form.ssn_id.data
        customer_name = form.customer_name.data
        age = form.age.data
        address = form.address.data
        state = form.state.data
        city = form.city.data
        phone_number = form.phone_number.data
        email = form.email.data

        # Check if the SSN ID already exists and if it's numeric
        if Customer_Account.objects(ssn_id=ssn_id) or not ssn_id.isnumeric():
            flash("Sorry, please try again with a valid SSN ID.", 'danger')
        else:
            # Create the customer account
            customer = Customer_Account(
                ssn_id=ssn_id,
                customer_name=customer_name,
                age=age,
                address=address,
                state=state,
                city=city,
                phone=phone_number,
                email=email,
                account_type="",
                s_m=0,
                message="Customer created successfully",
                datetime=str(dt.now())
            )
            customer.save()
            flash("You have been successfully registered!", 'success')
    return render_template("customer_screen.html", form=form)


@app.route('/profiles')
def pro():
    return render_template("profile.html")

@app.route('/update', methods=['GET','POST'])
def update_customer():
    l = []
    form = updateCustomer()
    temp = form.customer_ssn_id.data
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id=temp):
            user = Customer_Account.objects(ssn_id=temp).first()
        else:
            user = None
        new_customer_name = form.new_customer_name.data
        new_address = form.new_address.data
        new_age = form.new_age.data
        new_phone_number = form.new_phone.data  # Get new phone number
        new_email = form.new_email.data  # Get new email
        if user:
            # Update the customer details if the user exists
            Customer_Account.objects(ssn_id=temp).update(
                customer_name=new_customer_name,
                age=new_age,
                address=new_address,
                phone=new_phone_number,  # Update phone number
                email=new_email,  # Update email
                message="Customer updated successfully",
                datetime=str(dt.now())
            )
            flash("Customer updation successful!", 'success')
        else:
            flash("Customer with the given SSN ID does not exist", 'danger')
    return render_template('update_customer.html', form=form, ssn_id=temp)


@app.route('/deletecustomer',methods=['GET','POST'])
def delete_customer():
        form = deleteCustomer()
        if form.validate_on_submit():
            ssn_id = form.ssn_id.data
            customer_name = form.customer_name.data
            age = form.age.data
            address = form.address.data
            if Customer_Account.objects(ssn_id = ssn_id):
                user =  Customer_Account.objects(ssn_id=ssn_id).first()
                old_name = user.customer_name
                old_age = user.age
            else:
                user=0            

            if user!=0 and customer_name==old_name and age==old_age:
                Customer_Account.objects(ssn_id=ssn_id).delete()
                flash("Customer Deleted successful!",'success')
            else:
                flash("Customer with the given SSN_ID does not exists",'danger')
        return render_template('delete_customer.html',form=form)

#-----------------------------------------------------------------------------------------
#----------------------------------------------status Details ----------------------------
@app.route('/customerstaus',methods=['GET','POST'])
def customer_status():
    form=customerStatusSearch()
    query= form.search_query.data
    accs = Customer_Account.objects(ssn_id=query)
    return render_template('customer_status.html',form=form,accs = accs)

@app.route('/accountstatus',methods=['GET','POST'])
def account_status():
    form = accountStatusSearch()
    query= form.search_query.data
    acc =Customer_Account.objects(ssn_id=query) 
    return render_template('account_status.html',form = form,acc=acc)

#--------------------------------------------------------------------------------------------------

#----------------------------------------------Account Management--------------------------------
@app.route('/createaccount',methods=['GET','POST'])
def create_account():
    form =createaccount()
    customer_ssn_id = form.customer_id.data
    account_type = form.account_type.data
    deposit_amount = form.deposit_amount.data 
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = customer_ssn_id):
                    user =  Customer_Account.objects(ssn_id=customer_ssn_id).first()
        else:
                user=0
        if (account_type=="savings" or account_type=='s') and user != 0:
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(account_type = account_type, s_m = deposit_amount, message = "Customer Savings Account Created successfully", datetime = str(dt.now()))
                    flash("Customer Savings Account Created successfully","success")
        elif (account_type=="current" or account_type=='c') and user != 0: 
            if Customer_Account.objects(ssn_id = customer_ssn_id ).first():
                    Customer_Account.objects(ssn_id = customer_ssn_id ).update(account_type = account_type, s_m= deposit_amount ,  message = "Customer Current Account Created successfully" ,datetime = str(dt.now()))
                    flash("Customer Current Account Created successfully","success")
        else:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('create_account.html',form=form )


@app.route('/deleteaccount', methods=['GET','POST'])
def delete_account():
    form = deleteAccount()
    account_id = form.account_id.data
    account_type = form.account_type.data
    if form.validate_on_submit():
         if Customer_Account.objects(ssn_id = account_id):
                    user =  Customer_Account.objects(ssn_id=account_id).first()
         else:
                user=0       
         if  user != 0 and ( account_type=="savings" or account_type=='s') :
                Customer_Account.objects(ssn_id = account_id ).update(account_type = "", s_m = 0 ,message = "Savings Account Deleted Successfully" ,datetime = str(dt.now()))
                flash("Customer Savings Account Deleted successfully","success")
         elif  user != 0 and  ( account_type=="current" or account_type=='c'):
                Customer_Account.objects(ssn_id = account_id ).update(account_type = "", c_m = 0 ,message = "Current Account Deleted Successfully" ,datetime = str(dt.now()))
                flash("Customer Current Account Deleted successfully","success")
         else:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('delete_Account.html',form = form)

#---------------------------------------------------------------------------------------------------------
#------------------------------------------ Account Operations ------------------------------------------

@app.route('/accountsummary',methods =['GET','POST'] )
def account_summary():
    form = accountSum()
    query= form.search_query.data
    acc =Transactions.objects(name=query)
    return render_template("account_summary.html",form = form,acc=acc)

@app.route('/depositmoney', methods = ['GET','POST'])
def deposit_money():
    form = depositMoney()
    account_id = form.account_id.data
    deposit_amount = form.deposit_amount.data
        
    if form.validate_on_submit():
       
        if Customer_Account.objects(ssn_id = account_id):
                    user =  Customer_Account.objects(ssn_id=account_id).first()
        else:
                user=0  
        if user !=0 :
            if Customer_Account.objects(ssn_id = account_id ).first():
                us = Customer_Account.objects(ssn_id = account_id ).first()
                Customer_Account.objects(ssn_id = account_id ).update(s_m = us.s_m+deposit_amount, message = "Money Deposited Successfully To Savings Account" ,datetime =  str(dt.now()))
                us = Customer_Account.objects(ssn_id = account_id ).first()
                bal = us.s_m
                id_no = Transactions.objects().count()+1
                Transactions(id_no = id_no , description = "Deposit",name = account_id,datetime = str(dt.now()), amount = deposit_amount  ).save()
                flash("Money Deposited Successfully To Savings Account","success")
                
        elif user == 0:
            flash("Customer with the given SSN_ID does not exists",'danger')
    return render_template('deposit_money.html',form = form)


from flask import render_template, flash
from model import Customer_Account, Transactions
from datetime import datetime as dt

@app.route('/transfermoney', methods=['GET', 'POST'])
def transfer_money():
    form = transferMoney()
    customer_ssn_id = form.customer_id.data
    receiver_ssn_id = form.receiver_id.data
    transfer_amount = form.transfer_amount.data 

    if form.validate_on_submit():
        # Check if customer SSN ID exists in the database
        if Customer_Account.objects(ssn_id=customer_ssn_id).first():
            # Check if receiver SSN ID exists in the database
            if Customer_Account.objects(ssn_id=receiver_ssn_id).first():
                sender_account = Customer_Account.objects(ssn_id=customer_ssn_id).first()
                receiver_account = Customer_Account.objects(ssn_id=receiver_ssn_id).first()

                # Ensure transfer amount is positive
                if transfer_amount > 0:
                    # Check if source account has sufficient balance
                    if sender_account.s_m >= transfer_amount:
                        # Perform transfer from source to target account
                        sender_account.update(s_m=sender_account.s_m - transfer_amount)
                        receiver_account.update(s_m=receiver_account.s_m + transfer_amount)

                        # Record transaction
                        transaction_id = Transactions.objects().count() + 1
                        Transactions(
                            id_no=transaction_id,
                            description="Transfer",
                            name=customer_ssn_id,
                            datetime=str(dt.now()),
                            amount=transfer_amount
                        ).save()

                        flash("Money Transfered Successfully", 'success')
                    else:
                        flash("Insufficient balance in the source account", 'danger')
                else:
                    flash("Transfer amount should be a positive value", 'danger')
            else:
                flash("Receiver SSN ID doesn't exist in the database", 'danger')
        else:
            flash("Customer SSN ID doesn't exist in the database", 'danger')
    
    return render_template('transfer_money.html', form=form)



@app.route('/withdrawmoney', methods = ['GET','POST'])
def withdraw_money():
    form = withdrawMoney()
    account_id = form.account_id.data
    withdraw_amount = form.withdraw_amount.data 
    
    if form.validate_on_submit():
        if Customer_Account.objects(ssn_id = account_id):
            user = Customer_Account.objects(ssn_id = account_id).first()
            if user.s_m >= withdraw_amount :
                    us = Customer_Account.objects(ssn_id = account_id ).first()
                    Customer_Account.objects(ssn_id = account_id ).update(s_m = us.s_m-withdraw_amount,message = "Money Withdrawn Successfully From Svaings Account" ,datetime = str(dt.now()))
                    us = Customer_Account.objects(ssn_id = account_id ).first()
                    bal = us.s_m       
                    id_no = Transactions.objects().count()+1
                    Transactions(id_no = id_no , description = "Withdraw",name = account_id,datetime = str(dt.now()), amount = withdraw_amount  ).save()
                    flash("Money Withdrawn Successfully From Savings Account",'success') 
            elif user.s_m < withdraw_amount:
                flash("You dont have sufficient balance in your account",'danger')      
        else:
            flash("Customer with the given SSN_ID does not exists","danger")
    return render_template('withdraw_money.html',form = form)


# trsanctionn summary
@app.route('/show_transactions', methods = ['GET','POST'])
def show_transactions():
    # Fetch all transactions and sort them by datetime
    transactions = Transactions.objects().order_by('-datetime')

    return render_template('transaction_summary.html', transactions=transactions)

@app.route('/filter_transactions', methods=['POST'])
def filter_transactions():
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    filtered_transactions = []
    if start_date_str != '' and end_date_str != '':
        # Convert the date strings to datetime objects
        start_date = dt.strptime(start_date_str, '%Y-%m-%d')
        end_date = dt.strptime(end_date_str, '%Y-%m-%d')

        # Fetch all transactions from the database
        all_transactions = Transactions.objects()

        # Filter transactions based on the date range
        for transaction in all_transactions:
            # Parse the date component from the datetime string
            transaction_date = dt.strptime(transaction.datetime.split()[0], '%Y-%m-%d')

            # Check if the transaction date falls between the start and end dates
            if start_date <= transaction_date <= end_date:
                filtered_transactions.append(transaction)
        filtered_transactions.reverse()

    return render_template('transaction_summary.html', transactions=filtered_transactions)