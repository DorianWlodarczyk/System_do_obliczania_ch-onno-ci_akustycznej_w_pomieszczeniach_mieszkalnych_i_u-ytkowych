from datetime import date
from statistics import mean
from flask.json import JSONEncoder

from flask import Blueprint, render_template, request, flash, jsonify, Response, Flask, session, redirect, url_for, make_response
from flask_cors import CORS
from flask_login import login_required, current_user
from markupsafe import Markup
import pdfkit
from sqlalchemy.dialects.postgresql import psycopg2
from werkzeug.exceptions import BadRequest

from .models import Notes, Norms, Material, Projects
from . import db
import json
# from bs4 import BeautifulSoup

# class MaterialEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Material):
#             return {'pkey': obj.pkey, 'name': obj.name, 'type': obj.type, '_120': float(obj._120), '_250': float(obj._250), '_500': float(obj._500), '_1000': float(obj._1000), '_2000': float(obj._2000), '_4000': float(obj._4000)}
#         return super().default(obj)

views = Blueprint('views', __name__)
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# app.json_encoder = MaterialEncoder

@views.route('/download_pdf', methods=['POST'])
def download_pdf():
        project_name = request.form.get('project_name')
        html = display_new_project(project_name)
        print(html)
        pdfkit_options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
        }
        temp = []
        for x in html.splitlines(keepends=True):
            if x.find('<button type="submit">') > 0:
                continue
            else:
                temp.append(x)


        # version for linux
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdf = pdfkit.from_string(''.join(temp), options=pdfkit_options, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=output.pdf"
        return response

def prepare_html(html):


    return html




@views.route('/newproject/display/<project_name>')
@login_required
def display_new_project(project_name):
    # Get the project from the database based on the project_name parameter
    project = Projects.query.filter_by(name=project_name).first()

    # Get the related objects from the database based on the stored IDs in the project
    norm = Norms.query.get(project.norm_id).name
    sufit = Material.query.get(project.sufit_id).name
    wall1_material = Material.query.get(project.wall1_id).name
    wall2_material = Material.query.get(project.wall2_id).name
    wall4_material = Material.query.get(project.wall4_id).name
    floor_material = Material.query.get(project.floor).name
    front_wall_material = Material.query.get(project.wall3_id).name



    # Render the template with the stored data
    template_name = "display_newproject.html"
    rendered_template = render_template(template_name,user=current_user, project_name=project_name, norm_id=norm,
                                        up_to_norm=project.up_to_norm,
                                        new_project=project, norm=norm, sufit=sufit, wall1_material=wall1_material,
                                        wall2_material=wall2_material,
                                        front_wall_material=front_wall_material, height=project.height,
                                        length=project.length, width=project.width, back_wall_material=wall4_material,
                                        floor_material=floor_material, furniture=project.furniture)

    # Return the rendered template as a response
    return rendered_template


@views.route('/edit/<project_name>')
@login_required
def edit_project(project_name):
    # project = Projects.query.filter_by(name=project_name).first()
    return render_template('newproject.html', project_name=project_name)


@views.route('/newproject', methods=['GET', 'POST'])
@login_required
def new_project(project_name=''):
    if request.method == 'POST':
        # print(request.form)
        # Handle form submission
        project_name = request.form.get('projectName')
        norm_id = request.form.get('norms')
        length = request.form.get('length')
        width = request.form.get('width')
        height = request.form.get('height')
        sufit_id = request.form.get('sufit')
        wall1_id = request.form.get('wall1')
        wall2_id = request.form.get('wall2')
        wall3_id = request.form.get('wall3')
        wall4_id = request.form.get('wall4')
        floor = request.form.get('podloga')
        # for x in [project_name, norm_id, length, width, height, sufit_id, wall1_id, wall2_id, wall3_id, wall4_id, floor]:
        #     if x:
        #         pass
        #     else:
        #         flash(f'Nie wypelniono: {x}', category='error')
        # Extract the data-material-id attribute from all li elements inside the ul with id="material-other-list"
        # Print quantity and pkey for every member of the list with quantity > 0

        material_list_quantity = request.form.getlist('material-other-list')

        material_list = Material.query.filter_by(type='material_li').all()

        # Serialize the Material objects with custom JSON encoder
        material_list = Material.query.filter_by(type='Inne').all()
        material_json = []
        for material in material_list:
            quantity = request.form.get(f"material_{material.pkey}", 0)
            if int(quantity) > 0:
                material_json.append({'quantity': quantity, 'material': material})
        # json_materials = json.dumps(material_json, cls=MaterialEncoder)

        print("Full List: ", material_json)
        plain_list = [(int(item['quantity']), item['material'].pkey) for item in material_json]
        if float(length) <= 0.0 or float(width) <= 0.0 or float(height) <= 0.0:
            flash('Wymiary pomieszczenia musza byc wieksze od zera!', category='error')
        else:
            # Calculate room volume
            volume = float(length) * float(width) * float(height)

            # Define frequency list and reverb time list
            frequency_list = ['_120', '_250', '_500', '_1000', '_2000', '_4000']
            reverb_time = [0] * len(frequency_list)
            list_of_furniture = []
            # norm = Norms.query.filter_by(pkey=norm_id)
            norm = Norms.query.filter_by(pkey=norm_id).with_entities(Norms.absorption_multiplayer).first()
            print("norm:", norm[0])

            #Obsluga bledow
            if float(length) <= 0.0 or float(width) <= 0.0 or float(height) <= 0.0:
                flash('Wymiary pomieszczenia musza byc wieksze od zera!', category='error')

            # Initialize final absorption list
            final_absorption_list = [0] * len(frequency_list)

            # Loop through surfaces and floor materials, calculate absorption values and add to final absorption list
            for surface_id in [sufit_id, wall1_id, wall2_id, wall3_id, wall4_id]:
                surface_absorption_list = Material.query.filter_by(pkey=surface_id).first()
                surface_absorption_values = [float(getattr(surface_absorption_list, f)) for f in frequency_list]
                for i in range(len(surface_absorption_values)):
                    surface_absorption_values[i] *= volume
                    final_absorption_list[i] += surface_absorption_values[i]

            floor_material_list = Material.query.filter_by(pkey=floor).first()
            floor_material_values = [float(getattr(floor_material_list, f)) for f in frequency_list]
            for i in range(len(floor_material_values)):
                floor_material_values[i] *= volume
                final_absorption_list[i] += floor_material_values[i]

            #Obliczanie umeblowania
            for i in range(len(plain_list)):
                furniture_absorption_list = Material.query.filter_by(pkey=plain_list[i][1]).first()
                furniture_absorption_value = [float(getattr(furniture_absorption_list,f)) for f in frequency_list]
                furniture_name =getattr(furniture_absorption_list, 'name')
                list_of_furniture.append((furniture_name, plain_list[i][0]))
                for j in range(len(furniture_absorption_value)):
                    furniture_absorption_value[j] *= plain_list[i][0]
                    final_absorption_list[j] += furniture_absorption_value[j]

            print("Lista mebli: ", list_of_furniture)
            # Calculate absorption coefficient per square meter for the room
            for i in range(len(final_absorption_list)):
                final_absorption_list[i] /= volume
            list_of_furniture_json = json.dumps(list_of_furniture, ensure_ascii=False)
            if (final_absorption_list[2] >= norm[0] and final_absorption_list[3] >= norm[0] and
                    final_absorption_list[4] >= norm[0]):
                up_to_norm = 'Tak'
            else:
                up_to_norm = 'Nie'

            new_projekt = Projects(user_id=current_user.id,name=project_name,norm_id=norm_id, up_to_norm=up_to_norm,length=length, width=width,height=height,floor=floor,sufit_id=sufit_id,wall1_id=wall1_id,wall2_id=wall2_id,wall3_id=wall3_id,wall4_id=wall4_id,furniture=list_of_furniture_json,_120=final_absorption_list[0],_250=final_absorption_list[1],_500=final_absorption_list[2],_1000=final_absorption_list[3],_2000=final_absorption_list[4],_4000=final_absorption_list[5])
            db.session.add(new_projekt)
            db.session.commit()


            # flash('Podany projekt spelnia normy!', category='success')
            print("Final absorption list:", final_absorption_list)

            return redirect(url_for('views.display_new_project', project_name=project_name))



    # Render the newproject.html page with the collected data
    norms = Norms.query.all()
    materials_ceiling = Material.query.filter_by(type='Sufit').all()
    material_walls = Material.query.filter_by(type='Ściany').all()
    material_floor = Material.query.filter_by(type='Podłogi').all()
    material_other = Material.query.filter_by(type='Inne').all()
    
    return render_template("newproject.html", user=current_user, norms=norms, materials_ceiling=materials_ceiling,
                           materials_walls=material_walls, material_floor=material_floor, material_other=material_other)
                          

@views.route('/myProjects', methods=['GET', 'POST'])
@login_required
def my_Projects():
    projects = Projects.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':


        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Notes(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')


    return render_template("myProjects.html", user=current_user, projects=projects)


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

# To co poniżej przekopiowane ze starego projektu, trzeba zmodyfikować


#Zrobione wyżej, nie potrzebne
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

#Zrobione wyżej, nie potrzebne
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
