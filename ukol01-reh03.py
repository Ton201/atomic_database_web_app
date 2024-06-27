from urllib.parse import parse_qs
from models import db, Isotopes, Elements
import sqlite3
from support_fcions import isotope_selector, selection_union

# WSGI-klient
def application(environ, start_response):
    # query string (to za http://localhost:8080/?)
    print('QUERY_STRING =', environ['QUERY_STRING'])
    # totéž zparsované do slovníku
    form = parse_qs(environ['QUERY_STRING'])
    print(form)
    # Ptáme se na něco?
    if ('jméno' in form) and ("isotopy" in form):
        query1 = form['jméno'][0].lower()
        styl1 = 'background-color: lightgreen;'
        query2 = form['isotopy'][0].lower()
        styl2 = 'background-color: lightblue;'
    elif 'jméno' in form:
        query1 = form['jméno'][0].lower()
        styl1 = 'background-color: lightgreen;'
        query2, styl2 = 0,''
    elif "isotopy" in form:
        query2 = form['isotopy'][0].lower()
        styl2 = 'background-color: lightblue;'
        query1, styl1 = '',''
    else:
        query1, query2, styl1, styl2 = '', 0,'', ''
    # odpověď serveru (HTML-stránka)
    body = f'''
        <form>
            <label for="jméno">Jméno prvku:</label>
            <input name="jméno" type="text" value="{query1}">
            <input type="submit" value="odešli">
            <label for="isotopy">Minimální počet isotopů:</label>
            <input name="isotopy" type="text" value="{query2}">
            <input type="submit" value="odešli">
        </form>
        <table border>
            <cols>
                <col style="{styl1}"/>
                <col/>
                <col/>
                <col/>
                <col/>
                <col style="{styl2}"/>
                <col/>
            </cols>
            <tr>
                <th>name</th>
                <th>symbol</th>
                <th>group</th>
                <th>period</th>
                <th>block</th>
                <th>Isotopes</th>
                <th>Stable</th>
            </tr>
    '''
    
    # with orm.db_session:
        # for elem in orm.select(e for e in Elements if e.name.lower().startswith(query)):
            # body += '<tr>'
            # body += '  <td>' + elem.name + '</td>'
            # body += '  <td>' + elem.symbol + '</td>'
            # body += '  <td>' + elem.group + '</td>'
            # body += '  <td>' + elem.period + '</td>'
            # body += '  <td>' + elem.block + '</td>'
            # body += '</tr>'
    
    #SQLite výběr
    connection = sqlite3.connect("izotopy.db")
    cursor = connection.cursor()
    Q1 = """
                SELECT name, symbol, "group", period, block
                FROM Elements
                WHERE lower(name) LIKE ?
    """
    Q2 = """
                SELECT name, symbol, period, "group", block
                FROM Elements
    """
    if query1 != "":
        cursor.execute(Q1,(query1+"%",))
    else:
        cursor.execute(Q2)
    selection = cursor.fetchall()
    
    symbols = []
    for i in range(len(selection)):
        symbols.append(selection[i][1])
    
    iso = isotope_selector(symbols)
    stab_iso = isotope_selector(symbols, stable=True)
    result = selection_union(selection, iso, stab_iso)
    
    for elem in result:
        if int(elem[5]) >= int(query2):
            body += '<tr>'
            body += '  <td>' + elem[0] + '</td>'
            body += '  <td>' + elem[1] + '</td>'
            body += '  <td>' + elem[2] + '</td>'
            body += '  <td>' + elem[3] + '</td>'
            body += '  <td>' + elem[4] + '</td>'
            body += '  <td>' + elem[5] + '</td>'
            body += '  <td>' + elem[6] + '</td>'
            body += '</tr>'
    
    # ukončení HTML-tabulky
    body += '</table>'
    # vlastní odpověď serveru
    body_bytes = body.encode('utf-8')
    response_headers = [
        ("Content-type", "text/html; charset=UTF-8"),
        ("Content-length", str(len(body_bytes)) ),
    ]
    start_response("200 OK", response_headers)
    return (body_bytes,)
 
# WSGI-server (spuštěn pro jednu odpověď)
if __name__ == '__main__':
    # spojení na databázi
    db.bind(provider='sqlite', filename='izotopy.db')
    db.generate_mapping()
    # nahození webového serveru
    from wsgiref.simple_server import make_server
    server = make_server('localhost', 8080, application)
    server.serve_forever()
