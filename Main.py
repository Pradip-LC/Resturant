from flask import Flask, render_template, url_for, redirect,session, request,flash
from flask_mysqldb import MySQL
from sqlalchemy import func
from database.models import db, MenuItem, Payment, ResturantOwner, User, Order, OrderItem

app = Flask(__name__)
app.secret_key = '324^%^&67ghuagd^&%^&#$&*6876q3ggsad78as6d'
#database
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/foodbook'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
except Exception as e:
    print("error in database",e)

#checkSession
@app.route('/')
def index():
    if 'Account' in session and session['Role']=='user':
        return redirect(url_for('home'))
    elif 'Account' in session and session['Role']=='resturant':
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

#login page
@app.route('/login',methods=['GET','POST'])
def login():
    if 'Account' in session and session['Role']=='user':
        return redirect(url_for('home'))
    elif 'Account' in session and session['Role']=='resturant':
        return redirect(url_for('dashboard'))
    if request.method=="POST":
        username = request.form['name']
        password = request.form['password']
        #check if user exinst in either user or resturant table
        Current_user = User.query.filter_by(name=username).first()
        if not Current_user:
            Current_user = ResturantOwner.query.filter_by(name=username).first()
        #check if password is correct and put session details
        if Current_user and Current_user.pass_hass==password and Current_user.role=='user':
            session['Account'] = Current_user.id
            session['Role']= Current_user.role
            return redirect(url_for('home'))
        elif Current_user and Current_user.pass_hass==password and Current_user.role=='resturant':
            session['Account'] = Current_user.id
            session['Role']= Current_user.role
            return redirect(url_for('dashboard'))
        else:   
            flash("invalid username or password")
            return redirect(url_for('login'))   
              
    else:
        return render_template('login.html')
    
    
#signup(user and resturant owner)
@app.route('/signupUSR',methods=['GET','POST'] )
def signupUSR():
    if request.method=="POST":
        username = request.form['name']
        mail = request.form['email']
        Phone = request.form['phone']
        Password = request.form['password']
        Cpassword = request.form['confirm_password']
        if Password!=Cpassword:
            flash("password does not match")
            return render_template('sign_up.html')
        else:
            try:
                user = User(name=username,email=mail,phone=Phone,pass_hass=Password,role='user')
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                return render_template('sign_up.html')
    else:
        return render_template('sign_up.html')
    
@app.route('/signupRES',methods=['GET','POST'] )
def signupRES():
    if request.method=="POST":
        username = request.form['resturant_name']
        mail = request.form['email']
        Phone = request.form['phone']
        address = request.form['address']
        Password = request.form['password']
        Cpassword = request.form['confirm_password']
        if Password!=Cpassword:
            flash("password does not match")
            return render_template('sign_up.html')
        else:
            try:
                user = ResturantOwner(name=username,password=Password,address=address,is_active='',email=mail,phone=Phone,role='resturant')
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                print(e)
                return render_template('sign_up.html')
    else:
        return render_template('sign_up.html')

#passReset
@app.route('/reset')
def reset():
    return render_template('passReset.html')

#logout
@app.route('/logout')
def logout():
    session.pop('Account',None)
    return redirect(url_for('login'))

#Userhomepage
@app.route('/home')
def home():
    if 'Account' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('User/User_home.html')

#profile
@app.route('/profile')
def profile():
    if 'Account' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('profile.html')

@app.route('/cart')
def cart():
    if 'Account' not in session:
        return redirect(url_for('login'))
    else:
        return render_template('User/cart.html')

@app.route('/dashboard')
def dashboard():
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
            target_date = func.date(func.now())
            total_amount = db.session.query(func.sum(Payment.amount)).filter(func.date(Payment.date_time) == target_date, Order.resturant_id == session['Account']).scalar()
            if total_amount is None:
                total_amount = 0

            total_order_completed = db.session.query(func.count(Order.id)).filter(Order.status == 'order-complete', Order.resturant_id == session['Account']).scalar()
            if total_order_completed is None:
                total_order_completed = 0

            total_order_active = db.session.query(func.count(Order.id)).filter(Order.status == 'preparing', Order.resturant_id == session['Account']).scalar()
            if total_order_active is None:
                total_order_active = 0
            
            total_order_pending = db.session.query(func.count(Order.id)).filter(Order.status == 'pending', Order.resturant_id == session['Account']).scalar()
            if total_order_pending is None:
                total_order_pending = 0
            
            recent_payments = Order.query.filter_by(resturant_id= session['Account'] ).order_by(Order.date_time.desc()).limit(3).all()
            if recent_payments is None:
                recent_payments = []
            
            return render_template('Resturant/dashboard.html',order_history=recent_payments, Total_amount=total_amount, Total_order_completed=total_order_completed, Total_order_active=total_order_active, Total_order_pending=total_order_pending)
    
@app.route('/report')
def report():
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
        return render_template('Resturant/report.html')

@app.route('/Menu' ,methods=['GET','POST'])
def Menu():
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
        #new menu item creation
        if request.method=='POST':
            name = request.form['item_name']
            price = request.form['item_price']
            description = request.form['item_description']
            try:
                item = MenuItem(name=name,price=price,description=description,resturant_id=session['Account'])
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('Menu'))
            except Exception as e:
                print(e)
                return redirect(url_for('Menu'))
            
        items = MenuItem.query.filter_by(resturant_id=session['Account']).all()
        return render_template('Resturant/Menu.html',items=items)

@app.route('/delete/<int:item_id>',methods=['GET','POST'])
def delete(item_id):
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
        item = MenuItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('Menu'))

@app.route('/edit/<int:item_id>',methods=['GET','POST'])
def edit(item_id):
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
        item = MenuItem.query.get_or_404(item_id)
        if request.method=='POST':
            item.name = request.form['item_name']
            item.price = request.form['item_price']
            item.description = request.form['item_description']
            db.session.commit()
            return redirect(url_for('Menu'))
        return render_template('Resturant/edit.html',item=item)

@app.route('/Orders')
def Orders():
    if 'Account' not in session or session['Role']!='resturant':
        return redirect(url_for('login'))
    else:
        return render_template('Resturant/Orders.html')


if __name__ == '__main__':
    app.run(debug=True)

 
