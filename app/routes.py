from flask import render_template, url_for
from app import app
from app.models import Douyu
from flask import request


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    rooms = Douyu.query.order_by(Douyu.popularity.desc()).paginate(page, app.config['ROOMS_PER_PAGE'], False)
    next_url = url_for('index', page=rooms.next_num) if rooms.has_next else None
    prev_url = url_for('index', page=rooms.prev_num) if rooms.has_prev else None
    return render_template('index.html', rooms=rooms.items, next_url=next_url, prev_url=prev_url)


if __name__ == '__main__':
    app.run(debug=True)
