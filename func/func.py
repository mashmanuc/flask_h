def serch_p(slovo,text):
    m_slovo = [word[:-2].lower() if len(word) > 3 else word for word in slovo.split()]
    m_text = [word[:-2].lower() if len(word) > 3 else word for word in text.split()]
    for i in m_slovo:
        fl=False
        if (len(i)<4) or (i in m_text):
             fl=True
        else:
            fl=False
            break
    if fl==True:
        return text
def paginate_query(query, page, per_page):
    if page < 1:
        page = 1

    total = len(query)
    max_page = (total - 1) // per_page + 1

    if page > max_page:
        page = max_page

    items = query[(page - 1) * per_page:page * per_page]

    return [items, {
        'page': page,
        'per_page': per_page,
        'total': total,
        'max_page': max_page
    }]

# mass=[i*i for i in range(1, 101)]
# print(paginate_query(mass, 2,10))
