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
    password = request.form.get('password_hash')

    status, p_role = db.isin_users(login=username, hash_password=password)
    print(status, p_role)
    if status == db.ERRNO_USERS_DB.ok:
        session['user'] = username
        session['role_id'] = p_role
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
    filter_buyer = request.args.get('filter_buyer')

    role = session.get('role_id', 'user')

    order_numbers, pos, names, vendors, buyers = db.get_unique_cols_order()
    data = db.get_orders_last_comment(
        table='comments',
        filters={
            "order_number": filter_order_number,
            "po": filter_po,
            "name": filter_name,
            "vendor": filter_vendor,
            "buyer": filter_buyer
        })
    return render_template('table.html', data=data,
                           order_numbers=order_numbers,
                           pos=pos,
                           names=names,
                           vendors=vendors,
                           buyers=buyers,
                           role=role)


@app.route('/update_comment', methods=['POST'])
def update_comment():
    data_id = request.form.get('data_id')
    new_comment = request.form.get('comment')
    db.add_comment(order_id=data_id,
                   comment=new_comment)

    print(f"{data_id}: {new_comment}")
    referer = request.headers.get("Referer")
    return redirect(referer if referer else url_for('oracle'))


@app.route('/update_comment_pc', methods=['POST'])
def update_comment_pc():
    data_id = request.form.get('data_id')
    new_comment_pc = request.form.get('comment_pc')
    db.add_comment_pc(order_id=data_id,
                      comment_pc=new_comment_pc)

    print(f"{data_id}: {new_comment_pc}")
    referer = request.headers.get("Referer")
    return redirect(referer if referer else url_for('oracle'))


@app.route('/update_shipped_value', methods=['POST'])
def update_shipped_value():
    data_id = request.form.get('data_id')
    new_shipped = request.form.get('shipped')
    db.update_shipped(order_id=data_id,
                      shipped=new_shipped)

    referer = request.headers.get("Referer")
    return redirect(referer if referer else url_for('oracle'))


@app.route('/update_trans_data', methods=['POST'])
def update_trans_data():
    data_id = request.form.get('data_id')
    new_trans_data = request.form.get('trans_data')
    db.update_trans_data(order_id=data_id,
                         trans_data=new_trans_data)

    referer = request.headers.get("Referer")
    return redirect(referer if referer else url_for('oracle'))


if __name__ == '__main__':
    app.run(debug=True)
