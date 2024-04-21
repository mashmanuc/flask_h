


from cread_app import db,app, create_tables


class Predmet(db.Model):
    __tablename__ = 'predmet'
    id = db.Column(db.Integer, primary_key=True)
    predmet_name = db.Column(db.String(255))
    claass_list = db.relationship("Claass", back_populates="predmet")

class Claass(db.Model):
    __tablename__ = 'claass'
    id = db.Column(db.Integer, primary_key=True)
    claass_name = db.Column(db.String(255))
    predmet_id = db.Column(db.Integer, db.ForeignKey('predmet.id'))
    predmet = db.relationship("Predmet", back_populates="claass_list")
    tema_test_list = db.relationship("Tema_test", back_populates="claass")

class Tema_test(db.Model):
    __tablename__ = 'tema_test'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255))
    claass_id = db.Column(db.Integer, db.ForeignKey('claass.id'))
    claass = db.relationship("Claass", back_populates="tema_test_list")
    test_list = db.relationship("Test", back_populates="tema_test")

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    num_quest = db.Column(db.String(255))
    quest_img = db.Column(db.String(255))
    quest_text = db.Column(db.String(255))
    ans_data = db.Column(db.String(255))
    vidpov = db.Column(db.String(255))
    tema_test_id = db.Column(db.Integer, db.ForeignKey('tema_test.id'))
    tema_test = db.relationship("Tema_test", back_populates="test_list")

class Temy_site(db.Model):
    __tablename__ = 'tema_site'
    id = db.Column(db.Integer, primary_key=True)
    tema_test_id = db.Column(db.Integer)
create_tables()
def add_predmet(predmet_name):
    try:
        new_predmet = Predmet(predmet_name=predmet_name)
        db.session.add(new_predmet)
        db.session.commit()
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")

def add_claass(claass_name, predmet_id):
    try:
        new_claass = Claass(claass_name=claass_name, predmet_id=predmet_id)
        db.session.add(new_claass)
        db.session.commit()
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")

# Додайте інші функції аналогічно...
# ...

def add_Tema_test(test_name, claass_id):
    try:
        new_Tema_test = Tema_test(test_name=test_name, claass_id=claass_id)
        db.session.add(new_Tema_test)
        db.session.commit()
    except Exception as e:
        print(f"Помилка додавання теми: {e}")

def add_temy_site(id_):
    try:
        new_temy = Temy_site(tema_test_id=id_)
        db.session.add(new_temy)
        db.session.commit()
    except Exception as e:
        print(f"Помилка додавання предмету: {e}")

def find_temy_site():
    mass = []
    try:
        t_site = Temy_site.query.all()
        for i in t_site:
            obj = find_Tema_test_by_id(i.tema_test_id)
            mass.append(obj)
        print(t_site)
    except Exception as e:
        print(f"Пока тем не існує: {e}")

    return mass


# Додайте інші функції аналогічно...

def ob1_ob2(classs=Predmet, id=1):
    predmet = classs.query.filter_by(id=id).first()
    return predmet.claass_list

def ob2_ob3(classs=Claass, id=1):
    claass = classs.query.filter_by(id=id).first()
    return claass.tema_test_list

def find_last_Tema_test():
    return Tema_test.query.order_by(Tema_test.id.desc()).first()

def find_claass(id):
    return Claass.query.filter_by(id=id).first()

def find_Tema_test_by_id(Tema_test_id):
    return Tema_test.query.filter_by(id=Tema_test_id).first()

def find_temi_by_predmet(id):
    return Tema_test.query.filter(Tema_test.claass_id == id).all()

def find_temi_by_test(id):
    return Test.query.filter(Test.tema_test_id == id).all()

def find_test_to_slovo(slovo):
    mass = []
    m_slovo = [word[:-2].lower() if len(word) > 3 else word for word in slovo.split()]
    try:
        last_Tema_test = Tema_test.query.all()
        for tema in last_Tema_test:
            m_text = [word[:-2].lower() if len(word) > 3 else word for word in tema.test_name.split()]
            fl = False
            for i in m_slovo:
                if (len(i) < 4) or (i in m_text):
                    fl = True
                else:
                    fl = False
                    break
            if fl:
                mass.append(tema)
        return mass
    except Exception as e:
        print(f"Помилка пошуку останньої теми: {e}")


def mass_ans(id):
    return [item.ans_data.replace("\n", "").replace('\r', '').replace('\xa0', '').split('!') for item in find_temi_by_test(id)]

def tes_ans(id_):
    try:
        test = Test.query.filter_by(id=id_).first()
        return test.ans_data.replace("\n", "").replace('\r', '').replace('\xa0', '').split('!')
    except Exception as e:
        print(f"Помилка пошуку тем за предметом: {e}")
        return []

def find_test(id_):
    return Test.query.filter_by(id=id_).first()

def first_tema_test(tema_test_id):
    return Test.query.filter_by(tema_test_id=tema_test_id).first()

def add_test(num_quest, quest_img, quest_text, ans_data, vidpov, tema_test_id):
    try:
        new_test = Test(
            num_quest=num_quest,
            quest_img=quest_img,
            quest_text=quest_text,
            ans_data=ans_data,
            vidpov=vidpov,
            tema_test_id=tema_test_id
        )
        db.session.add(new_test)
        db.session.commit()
    except Exception as e:
        print(f"Помилка додавання тесту: {e}")

def update_test(test_id, num_quest, quest_img, quest_text, ans_data, vidpov):
    try:
        test = Test.query.get(test_id)
        test.num_quest = num_quest
        test.quest_img = quest_img
        test.quest_text = quest_text
        test.ans_data = ans_data
        test.vidpov = vidpov
        db.session.commit()
    except Exception as e:
        print(f"Помилка зміни тесту: {e}")

def update_by_id(class_, id_, update_data):
    try:
        item = class_.query.filter_by(id=id_).first()
        if item:
            for key, value in update_data.items():
                setattr(item, key, value)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Помилка оновлення запису: {e}")
        return False

def delete_by_id(class_, id_):
    try:
        item = class_.query.filter_by(id=id_).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Помилка видалення запису: {e}")
        return False

def find_test(id_):
    return Test.query.filter_by(id=id_).first()

def find_by_id(class_, id_):
    try:
        item = class_.query.filter_by(id=id_).first()
        if item:
            if class_ == Predmet:
                item.claass_list
            elif class_ == Claass:
                item.tema_test_list
        return item
    except Exception as e:
        print(f"Помилка пошуку запису: {e}")
        return None

def get_all_items(class_):
    try:
        items = class_.query.all()
        if class_ == Predmet:
            for item in items:
                item.claass_list
        elif class_ == Claass:
            for item in items:
                item.tema_test_list
        return items
    except Exception as e:
        print(f"Помилка отримання всіх записів: {e}")
        return []

def delete_tema_test_and_tests(tema_test_id):
    with db.session.begin():
        Test.query.filter_by(tema_test_id=tema_test_id).delete()
        Tema_test.query.filter_by(id=tema_test_id).delete()

def update_test_num_quest(test_id, num_quest):
    try:
        test = Test.query.get(test_id)
        test.num_quest = num_quest
        db.session.commit()
    except Exception as e:
        print(f"Помилка зміни тесту: {e}")

def find_last_test():
    return Test.query.order_by(Test.num_quest.desc()).first()

def min_max_test_id(tema_test_id):
    try:
        record = find_temi_by_test(tema_test_id)
        if record:
            return [m.id for m in record]
    except Exception as e:
        print(f"Помилка пошуку останнього тесту: {e}")
        return None

with app.app_context():
    db.create_all()

