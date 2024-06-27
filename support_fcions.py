from pprint import pprint
import sqlite3

#selekce izotopů
def isotope_selector(list_of_args, stable=False):
    isotope_count = []
    if stable == False:
        for i in range(len(list_of_args)):
            _connection = sqlite3.connect("izotopy.db")
            _cursor = _connection.cursor()
            _query = """
                        SELECT element
                        FROM Isotopes
                        WHERE element = ?"""
            _cursor.execute(_query, (list_of_args[i],))
            
            _selection = _cursor.fetchall()
            _answer = len(_selection)
            isotope_count.append(str(_answer))
            _connection.close()
    else:
        for i in range(len(list_of_args)):
            _connection = sqlite3.connect("izotopy.db")
            _cursor = _connection.cursor()
            _query = """
                        SELECT element
                        FROM Isotopes
                        WHERE element = ? AND T = 'STABLE'"""
            _cursor.execute(_query, (list_of_args[i],))
            
            _selection = _cursor.fetchall()
            answer = len(_selection)
            isotope_count.append(str(answer))
            _connection.close()
    return isotope_count

def selection_union(selection1, iso, stab_iso):
    #sjednoceni výběru + všechny isotopy
    _selection_and_isotopes = []
    for i in range(len(iso)):
        _selection_and_isotopes.append(selection1[i]+tuple(iso[i].split(",")))#první SELCET vrací list tuplů => ztupluju i další select

    selection_and_isotopes = [list() for i in _selection_and_isotopes]
    for j in range(len(_selection_and_isotopes)): #tuple je neměný datový typ => musím vytvořit nový list záznamů, kam údaje zapíši (raději jako stringy, kvůli snazšímu předání webové aplikaci)
        for i in range(len(_selection_and_isotopes[j])):
            selection_and_isotopes[j].append(str(_selection_and_isotopes[j][i]))

    #přidání stabilních izotopů
    for i in range(len(stab_iso)):
        selection_and_isotopes[i].append(stab_iso[i])
    return selection_and_isotopes

