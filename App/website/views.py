from datetime import date
from statistics import mean

from flask import Blueprint, render_template, request, flash, jsonify, Response, Flask, session, redirect, url_for
from flask_cors import CORS
from flask_login import login_required, current_user
from markupsafe import Markup
from pdfkit import pdfkit
from sqlalchemy.dialects.postgresql import psycopg2
from werkzeug.exceptions import BadRequest

from .models import Notes, Norms, Material
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/newproject')
def new_project():
    if request.method == 'GET':
        norms = Norms.query.all()
        materials_ceiling = Material.query.filter_by(type='Sufit').all()
        material_walls = Material.query.filter_by(type='Ściany').all()
        material_floor = Material.query.filter_by(type='Podłogi').all()
        material_other = Material.query.filter_by(type='Inne').all()

    return render_template("newproject.html", user=current_user, norms=norms, materials_ceiling=materials_ceiling,
                           materials_walls=material_walls, material_floor=material_floor, material_other=material_other)


@views.route('/myProjects', methods=['GET', 'POST'])
def my_Projects():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("myProjects.html", user=current_user)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Notes.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/materialy/<string:typ>', methods=['GET'])
def zwroc_liste_materialow(typ):
    if typ == "sciana":
        cur = db.cursor()
        cur.execute('SELECT DISTINCT on (name) name, pkey FROM materials WHERE type=\'Ściany\'')
        dane = cur.fetchall()
        cur.close()
        return dane
    elif typ == "sufit":
        cur = db.cursor()
        cur.execute('SELECT DISTINCT on (name) name, pkey FROM materials WHERE type=\'Sufit\'')
        dane = cur.fetchall()
        cur.close()
        return dane
    elif typ == "podloga":
        cur = db.cursor()
        cur.execute('SELECT DISTINCT on (name) name, pkey FROM materials WHERE type=\'Podłogi\'')
        dane = cur.fetchall()
        cur.close()
        return dane
    elif typ == "inne":
        cur = db.cursor()
        cur.execute('SELECT DISTINCT on (name) name, pkey FROM materials WHERE type=\'Inne\'')
        dane = cur.fetchall()
        cur.close()
        return dane

    # za pomocą paraemtru GET pobierane są dostepne normy w bazie danych


@views.route('/normy', methods=['GET'])
def zwroc_liste_norm():
    cur = db.cursor()
    cur.execute('SELECT DISTINCT on (name) name, pkey FROM norms')
    dane = cur.fetchall()
    cur.close()
    return dane





# funkcja odpowiedzialna za zwrocenie czestotliwosci przypisanej do materialu
def zwroc_czestotliwosci_dla_materialu(id):
    cur = db.cursor()
    cur.execute(f'SELECT "120", "250", "500", "1000", "2000", "4000" from materials WHERE pkey={id};')
    czestotliwosci = cur.fetchall()
    cur.close()
    return czestotliwosci


# walidacja
def val(request):
    # sprawdzamy czy otrzymane dane sa poprawnie zapisane w formacie JSON
    try:
        dane = request.json
    except BadRequest as e:
        komunikat = "Dane nie sa poprawnie zapisane w formacie JSON"
        return jsonify({"error": komunikat}), 400

    # sprawdzamy czy JSON ma odpowiednia strukture
    # funkcja zwraca nazwe materialu dla podanego identyfikatora
    def zwroc_nazwe_materialu(id):
        cur = db.cursor()
        cur.execute(f'SELECT name from materials where pkey={id};')
        dane = cur.fetchall()
        cur.close()
        return dane

    # funkcja zwraca nazwe normy dla podanego indentyfikatora
    def zwroc_nazwe_normy(id):
        cur = db.cursor()
        cur.execute(f'SELECT name from norms where pkey={id};')
        dane = cur.fetchall()
        cur.close()
        return dane

    # zwracana jest wartosc minimalna przypisana dla danej normy ktora musi spelniac pomieszcze
    def zwroc_wartosc_dla_normy(id):
        cur = db.cursor()
        cur.execute(f'SELECT absorption_multiplayer from norms where pkey={id};')
        dane = cur.fetchall()
        cur.close()
        return dane

    def oblicz(request):
        dane = val(request)

        # ---- OBLICZENIA ----
        # pobieramy z danych wejsciowych wymiary pomieszczenia
        dlugosc = dane["wymiar_pomieszczenia"]["dlugosc"]
        wysokosc = dane["wymiar_pomieszczenia"]["wysokosc"]
        szerokosc = dane["wymiar_pomieszczenia"]["szerokosc"]
        objetosc_wnetrza = dlugosc * szerokosc * wysokosc

        # czestotliwosoci 125, 250, 500, 1000, 2000, 4000
        # dane dla czestotliwosci 125 sa zapisane w pierwszym indeksie tablicy,
        # dla 250 w drugim itd.
        czas_poglosu = [0, 0, 0, 0, 0, 0]
        chlonnosc_akustyczna = [0, 0, 0, 0, 0, 0]
        chlonnosc_akustyczna_na_1m2 = [0, 0, 0, 0, 0, 0]
        # dostepne nazwy elementow w JSONie otrzymanym w zapytaniu
        elementy = ["sufit", "podloga", "scianalewa", "scianaprawa", "scianafrontowa", "scianatylna"]

        # iterujemy po wszystkich elementach i obliczamy chlonnosc akustyczna dla podanych elementow w JSON
        for el in elementy:
            for dane_el in dane["elementy"][el]:
                powierzchnia_elementu = dane_el["powierzchnia"]
                indeks = 0
                # pobieramy czestotliwosc dla materialu, ktorego identyfikator podano w JSON
                for j in zwroc_czestotliwosci_dla_materialu(dane_el["id"])[0]:
                    chlonnosc_akustyczna[indeks] += float(j) * powierzchnia_elementu
                    indeks += 1

        for i in range(0, len(chlonnosc_akustyczna_na_1m2)):
            chlonnosc_akustyczna_na_1m2[i] = chlonnosc_akustyczna[i] / (dlugosc * szerokosc)

        # liczymy poglos dla podanych elementow w JSON
        for i in range(0, len(chlonnosc_akustyczna)):
            czas_poglosu[i] += 0.163 * objetosc_wnetrza / chlonnosc_akustyczna[i] if chlonnosc_akustyczna[i] != 0 else 0

        # pobieramy identyfikator wymagania jakie musi spelnic pomeiszczenie
        wymagania = dane["norma_id"]
        # jesli jest rozne od -1 to zwracamy wartosc dla normy
        if wymagania != -1:
            wymagania = zwroc_wartosc_dla_normy(wymagania)[0][0]

        komunikat_1 = ''
        if (chlonnosc_akustyczna_na_1m2[2] >= wymagania and chlonnosc_akustyczna_na_1m2[3] >= wymagania and
                chlonnosc_akustyczna_na_1m2[4] >= wymagania):
            komunikat_1 = 'Pomieszczenie spełnia wymagania normy PN-B-02151-4'
        else:
            komunikat_1 = 'Pomieszczenie nie spełnia wymagań normy PN-B-02151-4'
        # przygotowujemy JSON do wyslania na frontend
        dane_do_wyslania = {
            "error": False,
            "sredni_czas_poglosu": mean(czas_poglosu),
            "min": wymagania,
            "wyniki": {
                "4000": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[5],
                    "czas_poglosu": czas_poglosu[5],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[5]
                },
                "2000": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[4],
                    "czas_poglosu": czas_poglosu[4],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[4]
                },
                "1000": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[3],
                    "czas_poglosu": czas_poglosu[3],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[3]
                },
                "500": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[2],
                    "czas_poglosu": czas_poglosu[2],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[2]
                },
                "250": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[1],

                    "czas_poglosu": czas_poglosu[1],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[1]
                },
                "125": {
                    "chlonnosc_akustyczna": chlonnosc_akustyczna[0],
                    "czas_poglosu": czas_poglosu[0],
                    "chlonnosc_akustyczna_na_1m2": chlonnosc_akustyczna_na_1m2[0]
                },
                "Komunikat": komunikat_1
            }
        }
        return (dane_do_wyslania)


@views.route('/oblicz', methods=['POST'])
def oblicz_parametry():
    return jsonify(oblicz(request))


# zwraca plik pdf na frontend
@views.route("/pobierz-raport", methods=['POST'])
def raport(name=None):
    dane = val(request)

    norma = dane["norma_id"]
    dlugosc = dane["wymiar_pomieszczenia"]["dlugosc"]
    wysokosc = dane["wymiar_pomieszczenia"]["wysokosc"]
    szerokosc = dane["wymiar_pomieszczenia"]["szerokosc"]
    objetosc_wnetrza = dlugosc * szerokosc * wysokosc
    sufit_powierzchnia = podloga_powierzchnia = dlugosc * szerokosc
    scianalewa_powierzchnia = scianaprawa_powierzchnia = dlugosc * wysokosc
    scianafrontowa_powierzchnia = scianatylna_powierzchnia = szerokosc * wysokosc

    if norma != -1:
        norma = zwroc_nazwe_normy(norma)[0][0]

    html = ["<td>", "<td>", "<td>", "<td>", "<td>", "<td>"]
    elementy = ["sufit", "podloga", "scianalewa", "scianaprawa", "scianafrontowa", "scianatylna"]

    for z in range(0, len(elementy)):
        el = elementy[z]

        for dane_el in dane["elementy"][el]:
            powierzchnia_elementu = dane_el["powierzchnia"]
            tekst = zwroc_nazwe_materialu(dane_el["id"])[0][0] + ": " + str(
                powierzchnia_elementu) + " m2" + "<hr width=\"100%\" />"
            html[z] += tekst

        html[z] = html[z][:-19]
        html[z] += "</td>"
        html[z] = Markup(html[z])

    wynik_obliczen = oblicz(request)
    # do zmiennej sufit_powierzchnia przypisywana jest wartosc stąd
    out = render_template("export.html", data=date.today(), sufit_powierzchnia=sufit_powierzchnia,
                          podloga_powierzchnia=podloga_powierzchnia, scianalewa_powierzchnia=scianalewa_powierzchnia,
                          scianaprawa_powierzchnia=scianalewa_powierzchnia,
                          scianafrontowa_powierzchnia=scianafrontowa_powierzchnia,
                          scianatylna_powierzchnia=scianatylna_powierzchnia, wymagania=norma, dlugosc=dlugosc,
                          wysokosc=wysokosc, szerokosc=szerokosc, objetosc=objetosc_wnetrza,
                          wynik_obliczen=wynik_obliczen, budowa_pomieszczenia=html)

    config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

    # PDF options
    options = {
        "orientation": "landscape",
        "page-size": "A4",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

    # budujemy plik pdf z html
    pdf = pdfkit.from_string(out, options=options, configuration=config)

    # wysylamy na frontend plik pdf
    return Response(pdf, mimetype="application/pdf")
