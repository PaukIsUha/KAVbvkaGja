from flask import Flask, render_template, redirect, url_for, request, session, flash
import database as db

app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'test' and password == '1234':
        session['user'] = username
        return redirect(url_for('bases'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('login'))


@app.route('/bases')
def bases():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('bases.html')


@app.route('/oracle')
def oracle():
    if 'user' not in session:
        return redirect(url_for('login'))
    filter_order_number = request.args.get('filter_order_number')
    filter_po = request.args.get('filter_po')
    filter_name = request.args.get('filter_name')
    filter_vendor = request.args.get('filter_vendor')

    order_numbers, pos, names, vendors = db.get_unique_cols_order()
    data = db.get_orders_last_comment(filters={
        "order_number": filter_order_number,
        "po": filter_po,
        "name": filter_name,
        "vendor": filter_vendor,
    })
    print(data)
    return render_template('table.html', data=data,
                           order_numbers=order_numbers,
                           pos=pos,
                           names=names,
                           vendors=vendors)


@app.route('/update_comment', methods=['POST'])
def update_comment():
    data_id = request.form.get('data_id')
    new_comment = request.form.get('comment')
    db.add_comment(order_id=data_id,
                   comment=new_comment)

    print(f"{data_id}: {new_comment}")
    return redirect(url_for('oracle'))


if __name__ == '__main__':
    app.run(debug=True)
