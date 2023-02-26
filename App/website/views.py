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
import tempfile

import os
from .models import  Norms, Material, Projects
from . import db
import json
from .norm_requirements import norm_requirements


views = Blueprint('views', __name__)
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


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
            if x.find('<button') > 0:
                continue
            else:
                temp.append(x)


        # version for linux
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdf = pdfkit.from_string(''.join(temp), options=pdfkit_options, configuration=config)
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f"inline; filename={project_name}.pdf"
        return response

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
    _120_absorption = project._120
    _250_absorption = project._250
    _500_absorption = project._500
    _1000_absorption = project._1000
    _2000_absorption = project._2000
    _4000_absorption = project._4000
    _120_reverb_time = project.reverb_time_120
    _250_reverb_time = project.reverb_time_250
    _500_reverb_time = project.reverb_time_500
    _1000_reverb_time = project.reverb_time_1000
    _2000_reverb_time = project.reverb_time_2000
    _4000_reverb_time = project.reverb_time_4000
    requirements = project.requirements

    # Render the template with the stored data
    template_name = "display_newproject.html"
    rendered_template = render_template(template_name,user=current_user, project_name=project_name, norm_id=norm,
                                        up_to_norm=project.up_to_norm,
                                        new_project=project, norm=norm, sufit=sufit, wall1_material=wall1_material,
                                        wall2_material=wall2_material,
                                        front_wall_material=front_wall_material, height=project.height,
                                        length=project.length, width=project.width, back_wall_material=wall4_material,
                                        floor_material=floor_material, furniture=project.furniture, _120_absorption=_120_absorption,_250_absorption=_250_absorption,
                                        _500_absorption=_500_absorption,_1000_absorption=_1000_absorption,_2000_absorption=_2000_absorption,_4000_absorption=_4000_absorption,
                                        _120_reverb_time=_120_reverb_time, _250_reverb_time= _250_reverb_time,_500_reverb_time=_500_reverb_time,_1000_reverb_time=_1000_reverb_time,
                                        _2000_reverb_time=_2000_reverb_time,_4000_reverb_time=_4000_reverb_time, requirements =requirements)

    # Return the rendered template as a response
    return rendered_template


@views.route('/edit/<project_name>', methods=['GET', 'POST'])
@login_required
def edit_project(project_name=''):
    if request.method == 'POST':

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


        plain_list = [(int(item['quantity']), item['material'].pkey) for item in material_json]
        if float(length) <= 0.0 or float(width) <= 0.0 or float(height) <= 0.0:
            flash('Wymiary pomieszczenia musza byc wieksze od zera!', category='error')
        else:
            # Calculate room volume
            volume = float(length) * float(width) * float(height)
            surface_area = float(length) * float(width)

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

            for i in range(len(reverb_time)):
                reverb_time[i] += (0.161 * volume) / final_absorption_list[i] if final_absorption_list[i] != 0 else 0
            # Calculate absorption coefficient per square meter for the room
            for i in range(len(final_absorption_list)):
                final_absorption_list[i] /= volume
            list_of_furniture_json = json.dumps(list_of_furniture, ensure_ascii=False)
            # if (final_absorption_list[2] >= norm[0] and final_absorption_list[3] >= norm[0] and
            #         final_absorption_list[4] >= norm[0]):
            #     up_to_norm = 'Tak'
            # else:
            #     up_to_norm = 'Nie'
            requirements, up_to_norm = norm_requirements(volume, surface_area, norm_id, height, final_absorption_list,
                                                         reverb_time)

            existing_project = Projects.query.filter_by(name=project_name, user_id=current_user.id).first()

            if existing_project:
                # If the project already exists, update its attributes
                existing_project.norm_id = norm_id
                existing_project.up_to_norm = up_to_norm
                existing_project.length = length
                existing_project.width = width
                existing_project.height = height
                existing_project.floor = floor
                existing_project.sufit_id = sufit_id
                existing_project.wall1_id = wall1_id
                existing_project.wall2_id = wall2_id
                existing_project.wall3_id = wall3_id
                existing_project.wall4_id = wall4_id
                existing_project.furniture = list_of_furniture_json
                existing_project._120 = final_absorption_list[0]
                existing_project._250 = final_absorption_list[1]
                existing_project._500 = final_absorption_list[2]
                existing_project._1000 = final_absorption_list[3]
                existing_project._2000 = final_absorption_list[4]
                existing_project._4000 = final_absorption_list[5]
                existing_project.reverb_time_120 = reverb_time[0]
                existing_project.reverb_time_250 = reverb_time[1]
                existing_project.reverb_time_500 = reverb_time[2]
                existing_project.reverb_time_1000 = reverb_time[3]
                existing_project.reverb_time_2000 = reverb_time[4]
                existing_project.reverb_time_4000 = reverb_time[5]
                existing_project.requirements = requirements
                db.session.commit()
                flash('Projekt został zaktualizowany!')
            else:
                # If the project does not exist, create a new one
                new_projekt = Projects(user_id=current_user.id, name=project_name, norm_id=norm_id, up_to_norm=up_to_norm,
                                       length=length, width=width, height=height, floor=floor, sufit_id=sufit_id, wall1_id=wall1_id,
                                       wall2_id=wall2_id, wall3_id=wall3_id, wall4_id=wall4_id, furniture=list_of_furniture_json,
                                       _120=final_absorption_list[0], _250=final_absorption_list[1], _500=final_absorption_list[2],
                                       _1000=final_absorption_list[3], _2000=final_absorption_list[4], _4000=final_absorption_list[5],
                                       reverb_time_120=reverb_time[0],reverb_time_250=reverb_time[1],reverb_time_500=reverb_time[2],
                                       reverb_time_1000=reverb_time[3],reverb_time_2000=reverb_time[4],reverb_time_4000=reverb_time[5],requirements=requirements)
                db.session.add(new_projekt)
                db.session.commit()
                flash('Projekt został dodany!')


            flash('Podany projekt spelnia normy!', category='success')


            return redirect(url_for('views.display_new_project', project_name=project_name))

    # Get the project from the database based on the project_name parameter
    project = Projects.query.filter_by(name=project_name).first()

    # Render the editproject.html page with the collected data
    norms = Norms.query.all()
    materials_ceiling = Material.query.filter_by(type='Sufit').all()
    material_walls = Material.query.filter_by(type='Ściany').all()
    material_floor = Material.query.filter_by(type='Podłogi').all()
    material_other = Material.query.filter_by(type='Inne').all()

    # Get the related objects from the database based on the stored IDs in the project
    norm = Norms.query.get(project.norm_id).name
    norm_id = Norms.query.get(project.norm_id)

    sufit = Material.query.get(project.sufit_id).name
    sufit_id = Material.query.get(project.sufit_id).pkey
  
    wall1_material = Material.query.get(project.wall1_id).name
    wall1_material_id = Material.query.get(project.wall1_id).pkey

    wall2_material = Material.query.get(project.wall2_id).name
    wall2_material_id = Material.query.get(project.wall2_id).pkey

    front_wall_material = Material.query.get(project.wall3_id).name
    front_wall_material_id = Material.query.get(project.wall3_id).pkey

    back_wall_material = Material.query.get(project.wall4_id).name
    back_wall_material_id = Material.query.get(project.wall4_id).pkey

    floor_material = Material.query.get(project.floor).name
    floor_material_id = Material.query.get(project.floor).pkey

    data = json.loads(project.furniture)

    # Convert list of tuples to dictionary
    furniture_dict = {name: quantity for name, quantity in data}
    print('furniture_dict: ', furniture_dict)    

    project = Projects.query.filter_by(name=project_name).first()

    template_name = "editproject.html"
    rendered_template = render_template(template_name,user=current_user, project_name=project_name, norm_id=norm, up_to_norm=project.up_to_norm,
            new_project=project, norm=norm, sufit=sufit, wall1_material=wall1_material, wall2_material=wall2_material,
            front_wall_material=front_wall_material, height=project.height, length=project.length, width=project.width, floor_material = floor_material, furniture=project.furniture, norms=norms, materials_ceiling=materials_ceiling,
                           materials_walls=material_walls, material_floor=material_floor, material_other=material_other,
                           wall1_material_id = wall1_material_id, wall2_material_id = wall2_material_id, back_wall_material = back_wall_material, floor_material_id = floor_material_id, front_wall_material_id = front_wall_material_id, sufit_id = sufit_id, back_wall_material_id = back_wall_material_id, furniture_dict=furniture_dict)
    
    return rendered_template


@views.route('/newproject', methods=['GET', 'POST'])
@login_required
def new_project(project_name=''):
    if request.method == 'POST':
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
            surface_area = float(length) * float(width)

            # Define frequency list and reverb time list
            frequency_list = ['_120', '_250', '_500', '_1000', '_2000', '_4000']
            reverb_time = [0] * len(frequency_list)
            list_of_furniture = []
            # norm = Norms.query.filter_by(pkey=norm_id)
            # norm = Norms.query.filter_by(pkey=norm_id).with_entities(Norms.absorption_multiplayer).first()

            #Obsluga bledow
            if float(length) <= 0.0 or float(width) <= 0.0 or float(height) <= 0.0:
                flash('Wymiary pomieszczenia musza byc wieksze od zera!', category='error')

            # Initialize final absorption list
            final_absorption_list = [0] * len(frequency_list)

            # Loop through surfaces and floor materials, calculate absorption values and add to final absorption list
            surfaces = [sufit_id, wall1_id, wall2_id, wall3_id, wall4_id]
            areas = [surface_area, float(length)*float(height), float(length)*float(height), float(width)*float(height), float(width)*float(height)]

            for surface_id, area in zip(surfaces, areas):
                surface_absorption_list = Material.query.filter_by(pkey=surface_id).first()
                surface_absorption_values = [float(getattr(surface_absorption_list, f)) for f in frequency_list]
                for i in range(len(surface_absorption_values)):
                    surface_absorption_values[i] *= area
                    final_absorption_list[i] += surface_absorption_values[i]

            floor_material_list = Material.query.filter_by(pkey=floor).first()
            floor_material_values = [float(getattr(floor_material_list, f)) for f in frequency_list]
            for i in range(len(floor_material_values)):
                floor_material_values[i] *= surface_area
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

            for i in range(len(reverb_time)):
                reverb_time[i] += (0.161 * volume) / final_absorption_list[i]
                print(reverb_time[i])
            # Calculate absorption coefficient per square meter for the room
            # for i in range(len(final_absorption_list)):
            #     final_absorption_list[i] /= volume
            list_of_furniture_json = json.dumps(list_of_furniture, ensure_ascii=False)
            # if (final_absorption_list[2] >= norm[0] and final_absorption_list[3] >= norm[0] and
            #         final_absorption_list[4] >= norm[0]):
            #     up_to_norm = 'Tak'
            # else:
            #     up_to_norm = 'Nie'
            requirements, up_to_norm = norm_requirements(volume, surface_area, int(norm_id), float(height), final_absorption_list, reverb_time)
            print(requirements)
            print(up_to_norm)


            existing_project = Projects.query.filter_by(name=project_name, user_id=current_user.id).first()

            if existing_project:
                # If the project already exists, update its attributes
                existing_project.norm_id = norm_id
                existing_project.up_to_norm = up_to_norm
                existing_project.length = length
                existing_project.width = width
                existing_project.height = height
                existing_project.floor = floor
                existing_project.sufit_id = sufit_id
                existing_project.wall1_id = wall1_id
                existing_project.wall2_id = wall2_id
                existing_project.wall3_id = wall3_id
                existing_project.wall4_id = wall4_id
                existing_project.furniture = list_of_furniture_json
                existing_project._120 = final_absorption_list[0]
                existing_project._250 = final_absorption_list[1]
                existing_project._500 = final_absorption_list[2]
                existing_project._1000 = final_absorption_list[3]
                existing_project._2000 = final_absorption_list[4]
                existing_project._4000 = final_absorption_list[5]
                existing_project.reverb_time_120 = reverb_time[0]
                existing_project.reverb_time_250 = reverb_time[1]
                existing_project.reverb_time_500 = reverb_time[2]
                existing_project.reverb_time_1000 = reverb_time[3]
                existing_project.reverb_time_2000 = reverb_time[4]
                existing_project.reverb_time_4000 = reverb_time[5]
                existing_project.requirements = requirements
                db.session.commit()
                flash('Projekt został zaktualizowany!')
            else:
                # If the project does not exist, create a new one
                new_projekt = Projects(user_id=current_user.id, name=project_name, norm_id=norm_id, up_to_norm=up_to_norm,
                                       length=length, width=width, height=height, floor=floor, sufit_id=sufit_id, wall1_id=wall1_id,
                                       wall2_id=wall2_id, wall3_id=wall3_id, wall4_id=wall4_id, furniture=list_of_furniture_json,
                                       _120=final_absorption_list[0], _250=final_absorption_list[1], _500=final_absorption_list[2],
                                       _1000=final_absorption_list[3], _2000=final_absorption_list[4], _4000=final_absorption_list[5],
                                       reverb_time_120=reverb_time[0],reverb_time_250=reverb_time[1],reverb_time_500=reverb_time[2],
                                       reverb_time_1000=reverb_time[3],reverb_time_2000=reverb_time[4],reverb_time_4000=reverb_time[5], requirements = requirements)
                db.session.add(new_projekt)
                db.session.commit()
                flash('Projekt został dodany!')

            # flash('Podany projekt spelnia normy!', category='success')


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
        selected_project = request.form.get('selected_project')
        project = Projects.query.get(selected_project).name
        return redirect(url_for('views.display_new_project', project_name=project))
    return render_template("myProjects.html", user=current_user, projects=projects)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    return render_template("home.html", user=current_user)



@views.route('/delete/<project_name>', methods=['POST', 'GET'])
@login_required
def delete_project(project_name):
    if project_name:
        selected_project = request.form.get('project_name')
        project = Projects.query.filter_by(name=project_name).first()
        db.session.delete(project)
        db.session.commit()
    else:
        flash("Wybrano nieprawidłową opcję",category="error")
    return redirect(url_for('views.my_Projects'))

