from flask import Blueprint, render_template, url_for, redirect, request, flash
# SQLALCHEMY_DATABASE_URI ='mysql+mysqlconnector://mash:123mMm321@mash.mysql.database.azure.com:3306/prosto'
from admin.forms import TestForm
from model import get_all_items,add_oun_temy_site, Predmet, Claass,update_test,delete_tema_test_and_tests,find_test_to_slovo,find_claass, Tema_test, Test, find_temi_by_test, find_temi_by_predmet, find_Tema_test_by_id, ob1_ob2, mass_ans, first_tema_test, find_temy_site, min_max_test_id, tes_ans, find_test

# from admin.model_ad import *
from admin.func_ad import paginate_query
title='Goooooo'
admin = Blueprint('admin', __name__, template_folder='templates')



@admin.app_template_filter('zip')
def jinja2_zip(a, b):
    return zip(a, b)
predmets = get_all_items(Predmet)
claasses = get_all_items(Claass)
tema_test=get_all_items(Tema_test)
testes=get_all_items(Test)
@admin.route('/')
def index_ad():

    return render_template('index_ad.html',title=title, predmetes=predmets)

@admin.route('/predmet_ad/<int:predmet_id>')
def predmet_ad(predmet_id=2):
    # Create a new SQLAlchemy session
    claass_list = ob1_ob2(classs=Predmet,id=predmet_id)
    return render_template('predmet_ad.html',title=title,  claass_list=claass_list)


@admin.route('/claass_ad')
def claass_ad():
    return render_template('claass_ad.html',title=title,claasses=claasses)

@admin.route('/tema_test_ad/<int:id>')
def tema_test_ad(id):
    per_page = 20  # You can adjust this to the desired number of items per page
    page = request.args.get('page', type=int, default=1)
    test_names = find_temi_by_predmet(id)
    pre=find_claass(test_names[0].claass_id)
    pagination_info = paginate_query(test_names, page, per_page)
    return render_template('tema_test_ad.html',  pagination=pagination_info, id=id,pre=pre)


@admin.route('/testes_ad/<int:id>')
def testes_ad(id):
    data=find_temi_by_test(id)
    temma=find_Tema_test_by_id(id)

    m_ans=mass_ans(id)
    return render_template('testes_ad.html',data=data, m_ans= m_ans, temma=temma)
@admin.route('/add_temy_site/<int:id>')
def add_temy_site(id):
    if request.method == 'GET':
        
        try:
            add_oun_temy_site(id)
            return redirect(url_for('admin.tema_test_ad', id=id))
        except Exception as e:
            print(f"Помилка додавання предмету: {e}")

    elif request.method == 'GET':
        return redirect(url_for('admin.tema_test_ad'))


@admin.route('/admin/dell_test_tema_ad/<int:id>', methods=['GET', 'POST'])
def dell_test_tema_ad(id):
    if request.method == 'GET':
        delete_tema_test_and_tests(id)
        return redirect(url_for( "admin.index_ad"))


@admin.route('/edit_test/<int:test_id>', methods=['GET', 'POST'])
def edit_test(test_id):
    test = find_test(test_id)  # Retrieve the test object
    form = TestForm()

    if request.method == 'GET':
        form.num_quest.data = test.num_quest
        form.quest_img.data = test.quest_img
        form.quest_text.data = test.quest_text
        form.ans_data.data = test.ans_data
        form.vidpov.data = test.vidpov

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(test)
        update_test(test.id, test.num_quest, test.quest_img, test.quest_text, test.ans_data, test.vidpov)
        return redirect(url_for('admin.testes_ad', id=test.tema_test_id))
    else:
    # Відобразити помилки валідації, якщо такі є
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Field: {field}, Error: {error}")

    return render_template('edit_test.html', form=form, test=test)



@admin.route('/serch_ad', methods=['POST', 'GET'])
def sersh_ad():
    slovo = None
    page = request.args.get('page', type=int, default=1)  # Отримуємо параметр сторінки
    per_page = 20  # Кількість елементів на сторінці

    if request.method == "GET":
        slovo = request.args.get("title_sersh")
    # Виконуємо пошук і отримуємо результати запиту
    items = find_test_to_slovo(slovo)
    paginated_items = paginate_query(items, page, per_page)
    return render_template('serch_ad.html', items=paginated_items, slovo=slovo)
