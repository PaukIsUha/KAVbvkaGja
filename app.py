from flask import Flask, render_template, redirect, url_for, request
import database as db

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start():
    data = db.get_orders_last_comment()
    return render_template('table.html', data=data)


@app.route('/update_comment', methods=['POST'])
def update_comment():
    data_id = request.form.get('data_id')
    new_comment = request.form.get('comment')
    db.add_comment(order_id=data_id,
                   comment=new_comment)

    print(f"{data_id}: {new_comment}")
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.run(debug=True)
