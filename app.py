from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
#Создаём базу данных (БД)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Делаем один элемент в БД с названием "Имя"
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Item %r' %self.id
#Создаём страницу с добавлением имён в БД
@app.route('/', methods=['POST', 'GET'])
def jsonb():
    if request.method == 'POST':
        name = request.form['name']
        item = Item(name=name)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении имени произошла ошибка!'
    else:
        return render_template('jsonb.html')
#Создаём страницу с выводом всех имён имеющихся в БД
@app.route('/names')
def names():
    names1 = Item.query.order_by().all()
    return render_template('names.html', names1=names1)
#Часть с создания БД
if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()