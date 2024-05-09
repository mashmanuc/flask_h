from flask import Blueprint, render_template, url_for, redirect, request
from uroki.forms_ur import NameForm
from flask_login import current_user, login_required
from cread_app import app
from func import *
title = 'Goooooo'
uroki = Blueprint('uroki', __name__, template_folder='templates')

from model import find_temi_by_test, find_temi_by_predmet, find_Tema_test_by_id, ob1_ob2, mass_ans, first_tema_test, find_temy_site, min_max_test_id, tes_ans, find_test
from models import users_collection, user_test_collection, add_user_test, user_test, user_res_test, dinamic,   find_vid, vidsotok

@uroki.app_template_filter('zip')
def jinja2_zip(a, b):
    return zip(a, b)

@uroki.route('/')
def index_ur():
    data = find_temi_by_test(1)
    temma = find_Tema_test_by_id(1)
    form = NameForm()
    m_ans = mass_ans(1)
    return render_template('testes_ur.html', data=data, m_ans=m_ans, temma=temma, form=form)

@uroki.route('/predmet_ur/<int:predmet_id>')
def predmet_ur(predmet_id=2):
    claass_list = ob1_ob2(predmet_id)
    return render_template('predmet_ad.html', title=title, claass_list=claass_list)

@uroki.route('/tema_test_ur/<int:id>')
def tema_test_ur(id):
    per_page = 20
    page = request.args.get('page', type=int, default=1)
    test_names = find_temi_by_predmet(id)
    pagination_info = paginate_query(test_names, page, per_page)
    return render_template('tema_test_ad.html', pagination=pagination_info, id=id)

@uroki.route('/testes_ur/<int:id>')
def testes_ur(id):
    data = find_temi_by_test(id)
    m_ans = mass_ans(id)
    return render_template('testes_ur.html', data=data, m_ans=m_ans)

@uroki.route('/testes_ur/<int:tema_test_id>/<int:test_id>/<string:an>/')
def save_test(tema_test_id, test_id, an):
    users_id = current_user.name
    tema_test_id = 1
    temma = find_Tema_test_by_id(tema_test_id)
    data = find_temi_by_test(tema_test_id)
    test_obj = data[test_id - 1]
    num_quest = int(test_obj['num_quest'].split()[-1])
    pr_vid = test_obj['vidpov']
    add_user_test(users_id, num_quest, tema_test_id, test_id, an, pr_vid)
    tata = user_test(users_id, tema_test_id)
    form = NameForm()
    m_ans = mass_ans(tema_test_id)
    return render_template('testes_ur.html', data=data, m_ans=m_ans, temma=temma, form=form, tata=tata)

@uroki.route('/urok_test/')
def urok_test():
    if current_user.is_authenticated:
        temma = find_temy_site()
        return render_template('page_test/urok_test.html', temma=temma)
    else:
        return redirect(url_for('login'))

@uroki.route('/page_test/<int:tema_test_id>/')
def page_test(tema_test_id):
    users_id = current_user.name
    temma = find_Tema_test_by_id(tema_test_id)
    test = first_tema_test(tema_test_id)
    m_ans = tes_ans(test['id'])
    tata = find_vid(users_id, tema_test_id, test['id'])
    min_max_t = min_max_test_id(tema_test_id)
    dinamics = dinamic(users_id, tema_test_id)
    return render_template('page_test/page_test.html', tata=tata, dinamics=dinamics, test=test, m_ans=m_ans, temma=temma, min_max_t=min_max_t)

@uroki.route('/show_question/<int:tema_test_id>/<int:test_id>/<string:an>/')
def show_question(tema_test_id, test_id, an):
    temma = find_Tema_test_by_id(tema_test_id)
    test = find_test(test_id)
    users_id = current_user.name
    pr_vid = test['vidpov']
    num_quest = test['num_quest']
    add_user_test(users_id, num_quest, tema_test_id, test_id, an, pr_vid)
    tata = find_vid(users_id, tema_test_id, test['id'])
    m_ans = tes_ans(test_id)
    dinamics = dinamic(users_id, tema_test_id)
    min_max_t = min_max_test_id(tema_test_id)
    return render_template('page_test/page_test.html', dinamics=dinamics, tata=tata, test=test, m_ans=m_ans, temma=temma, min_max_t=min_max_t)

@uroki.route('/show_next_quest/<int:tema_test_id>/<int:test_id>')
def show_next_quest(tema_test_id, test_id):
    temma = find_Tema_test_by_id(tema_test_id)
    users_id = current_user.name
    next_test_id = test_id + 1
    next_test = find_test(next_test_id)
    tata = find_vid(users_id, tema_test_id, next_test['id'])
    m_ans = tes_ans(next_test_id)
    min_max_t = min_max_test_id(tema_test_id)
    dinamics = dinamic(users_id, tema_test_id)
    return render_template('page_test/page_test.html', dinamics=dinamics, test=next_test, tata=tata, m_ans=m_ans, temma=temma, min_max_t=min_max_t)

@uroki.route('/show_res/<int:tema_test_id>')
def show_res(tema_test_id):
    temma = find_Tema_test_by_id(tema_test_id)
    users_id = current_user.name
    vids = vidsotok(users_id, tema_test_id)
    ress = user_res_test(users_id, tema_test_id)
    return render_template('page_test/page_res.html', vids=vids, ress=ress, temma=temma)












