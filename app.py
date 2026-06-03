from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import pymysql

pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL

from werkzeug.utils import secure_filename

import os
import bcrypt

from datetime import timedelta
app = Flask(__name__)

# SECRET KEY

app.secret_key = 'fashionhub_secret_key_2026'

# SESSION TIMEOUT

app.permanent_session_lifetime = timedelta(minutes=30)

# IMAGE UPLOAD FOLDER

app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MYSQL CONFIGURATION

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rootanjali123'
app.config['MYSQL_DB'] = 'fashionhub'

mysql = MySQL(app)

# ALLOWED IMAGE EXTENSIONS

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    return render_template(
        'index.html',
        products=products
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # HASH PASSWORD

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        cur = mysql.connection.cursor()

        cur.execute("""

        INSERT INTO users
        (name, email, password)

        VALUES(%s, %s, %s)

        """, (

            name,
            email,
            hashed_password

        ))

        mysql.connection.commit()

        cur.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute("""

        SELECT * FROM users
        WHERE email=%s

        """, (email,))

        user = cur.fetchone()

        cur.close()

        if user:

            stored_password = user[3]

            if bcrypt.checkpw(

                password.encode('utf-8'),

                stored_password.encode('utf-8')

            ):

                # STORE USER EMAIL

                session['user'] = user[2]

                return redirect('/')

        return "Invalid Email or Password"

    return render_template('login.html')


@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


@app.route('/admin')
def admin():

    if 'user' not in session:

        return redirect('/login')

    # ADMIN ACCESS ONLY

    if session['user'] != 'admin@gmail.com':

        return "Access Denied"

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM products")
    products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.close()

    return render_template(
        'admin.html',
        products=products,
        orders=orders,
        users=users
    )

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    # LOGIN CHECK

    if 'user' not in session:

        return redirect('/login')

    # FORM SUBMIT

    if request.method == 'POST':

        # GET FORM DATA

        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']

        # IMAGE FILE

        image = request.files['image']

        # CHECK IMAGE

        if image and allowed_file(image.filename):

            # SECURE FILE NAME

            filename = secure_filename(image.filename)

            # IMAGE SAVE PATH

            image_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            # SAVE IMAGE

            image.save(image_path)

            # DATABASE IMAGE PATH

            db_image_path = 'uploads/' + filename

        else:

            db_image_path = 'uploads/default.jpg'

        # DATABASE CONNECTION

        cur = mysql.connection.cursor()

        # INSERT PRODUCT

        cur.execute("""

        INSERT INTO products
        (name, price, category, image, description)

        VALUES(%s, %s, %s, %s, %s)

        """, (

            name,
            price,
            category,
            db_image_path,
            description

        ))

        # SAVE DATABASE

        mysql.connection.commit()

        # CLOSE CURSOR

        cur.close()

        # REDIRECT

        return redirect('/')

    return render_template('add_product.html')


@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM products
    WHERE id=%s
    """,(id,))

    product = cur.fetchone()

    cur.execute("""
    INSERT INTO cart
    (product_id,product_name,price,image)
    VALUES(%s,%s,%s,%s)
    """,(
        product[0],
        product[1],
        product[2],
        product[4]
    ))

    mysql.connection.commit()

    return redirect('/cart')


@app.route('/cart')
def cart():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM cart")

    cart_items = cur.fetchall()

    total = 0

    for item in cart_items:

        total += item[3]

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total
    )


@app.route('/remove_cart/<int:id>')
def remove_cart(id):

    cur = mysql.connection.cursor()

    cur.execute("""
    DELETE FROM cart
    WHERE id=%s
    """,(id,))

    mysql.connection.commit()

    return redirect('/cart')
@app.route('/search')
def search():

    search = request.args.get('search')
    category = request.args.get('category')

    cur = mysql.connection.cursor()

    if search and category:

        cur.execute("""
        SELECT * FROM products
        WHERE name LIKE %s
        AND category=%s
        """,('%'+search+'%', category))

    elif search:

        cur.execute("""
        SELECT * FROM products
        WHERE name LIKE %s
        """,('%'+search+'%',))

    elif category:

        cur.execute("""
        SELECT * FROM products
        WHERE category=%s
        """,(category,))

    else:

        cur.execute("SELECT * FROM products")

    products = cur.fetchall()

    return render_template(
        'index.html',
        products=products
    )
@app.route('/checkout', methods=['GET','POST'])
def checkout():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM cart")

    cart_items = cur.fetchall()

    total = 0

    for item in cart_items:

        total += item[3]

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        cur.execute("""
        INSERT INTO orders
        (customer_name,email,address,phone,total_price)
        VALUES(%s,%s,%s,%s,%s)
        """,(
            customer_name,
            email,
            address,
            phone,
            total
        ))

        mysql.connection.commit()

        cur.execute("DELETE FROM cart")

        mysql.connection.commit()

        return redirect('/order_success')

    return render_template(
        'checkout.html',
        total=total
    )


@app.route('/order_success')
def order_success():

    return render_template('order_success.html')
@app.route('/orders')
def orders():

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM orders")

    orders = cur.fetchall()

    return render_template(
        'orders.html',
        orders=orders
    )


@app.route('/delete_order/<int:id>')
def delete_order(id):

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    DELETE FROM orders
    WHERE id=%s
    """,(id,))

    mysql.connection.commit()

    return redirect('/orders')
@app.route('/delete_product/<int:id>')
def delete_product(id):

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    DELETE FROM products
    WHERE id=%s
    """,(id,))

    mysql.connection.commit()

    return redirect('/')
@app.route('/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM products
    WHERE id=%s
    """,(id,))

    product = cur.fetchone()

    if request.method == 'POST':

        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']

        image = request.files['image']

        if image.filename != '':

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                )
            )

            image_path = 'uploads/' + filename

            cur.execute("""
            UPDATE products
            SET name=%s,
                price=%s,
                category=%s,
                image=%s,
                description=%s
            WHERE id=%s
            """,(
                name,
                price,
                category,
                image_path,
                description,
                id
            ))

        else:

            cur.execute("""
            UPDATE products
            SET name=%s,
                price=%s,
                category=%s,
                description=%s
            WHERE id=%s
            """,(
                name,
                price,
                category,
                description,
                id
            ))

        mysql.connection.commit()

        return redirect('/')

    return render_template(
        'edit_product.html',
        product=product
    )
@app.route('/history')
def history():

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM orders
    WHERE email=%s
    """,(session['user'],))

    orders = cur.fetchall()

    return render_template(
        'history.html',
        orders=orders
    )
@app.route('/product/<int:id>', methods=['GET','POST'])
def product_details(id):

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM products
    WHERE id=%s
    """,(id,))

    product = cur.fetchone()

    if request.method == 'POST':

        if 'user' not in session:

            return redirect('/login')

        rating = request.form['rating']
        review = request.form['review']

        cur.execute("""
        INSERT INTO reviews
        (product_id,username,rating,review)
        VALUES(%s,%s,%s,%s)
        """,(
            id,
            session['user'],
            rating,
            review
        ))

        mysql.connection.commit()

        return redirect(f'/product/{id}')

    cur.execute("""
    SELECT * FROM reviews
    WHERE product_id=%s
    """,(id,))

    reviews = cur.fetchall()

    return render_template(
        'product_details.html',
        product=product,
        reviews=reviews
    )  
@app.route('/add_wishlist/<int:id>')
def add_wishlist(id):

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM products
    WHERE id=%s
    """,(id,))

    product = cur.fetchone()

    cur.execute("""
    INSERT INTO wishlist
    (username,product_id,product_name,price,image)
    VALUES(%s,%s,%s,%s,%s)
    """,(
        session['user'],
        product[0],
        product[1],
        product[2],
        product[4]
    ))

    mysql.connection.commit()

    return redirect('/wishlist')


@app.route('/wishlist')
def wishlist():

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    SELECT * FROM wishlist
    WHERE username=%s
    """,(session['user'],))

    wishlist = cur.fetchall()

    return render_template(
        'wishlist.html',
        wishlist=wishlist
    )


@app.route('/remove_wishlist/<int:id>')
def remove_wishlist(id):

    if 'user' not in session:

        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("""
    DELETE FROM wishlist
    WHERE id=%s
    """,(id,))

    mysql.connection.commit()

    return redirect('/wishlist') 


if __name__ == '__main__':
    app.run(debug=True)