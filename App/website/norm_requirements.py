from .models import NormsReverbTimeVolumeReq, NormsReverbTimeNoReq, NormsAbsorptionMultiplayer, NormsReverbTimeHeightReq
def norm_requirements(Volume,surface_area, project_id,height, absorption_list, reverb_time_list):
    if(project_id == 1):
        if(Volume <= 120):
            requirements = 'Dla V mniejszego od 120m3 , T musi być mniejsze badz rowne 0.6s'
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.less_120).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif(Volume > 120 and Volume < 250):
            requirements = 'Dla V z zakresu od 120m3 do 250m3 T musi byc mniejsze badz rowne 0.6s a STI większe bądź równe 0.6 '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.between_120_250).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif(Volume >= 250 and Volume < 500):
            requirements = 'Dla V z zakresu od 250m3 do 500m3 T musi byc mniejsze badz rowne 0.8s a STI większe bądź równe 0.6 '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.between_250_500).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (Volume >= 500 and Volume < 2000):
            requirements = 'Dla V z zakresu od 500m3 do 2000m3 T musi byc mniejsze badz rowne 1.0s a STI większe bądź równe 0.6 '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.between_500_2000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (Volume > 2000):
            requirements = 'Dla V większego od 2000m3 T oraz STI musi byc okreslone indywidualnie '
            up_to_norm = 'Dla tego typu pomieszczenia nie ma okreslonej normy, nalezy ja wyznaczyc dla tego pomieszczenia'
            return requirements,up_to_norm


    if(project_id == 2):
        requirements = 'Dla kazdego pomieszczenia T musi byc mniejsze badz rowne 0.4s '
        reverb_time_norm = NormsReverbTimeNoReq.query.with_entities(NormsReverbTimeNoReq.no_cubature_req).filter_by(norm_id=project_id).first()
        up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
        return requirements, up_to_norm

    if(project_id == 3 or project_id == 4 or project_id == 5 or project_id == 14):
        requirements = 'Dla kazdego pomieszczenia T musi byc mniejsze badz rowne 0.6s '
        reverb_time_norm = NormsReverbTimeNoReq.query.with_entities(NormsReverbTimeNoReq.no_cubature_req).filter_by(norm_id=project_id).first()
        up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
        return requirements, up_to_norm

    if(project_id == 6 or project_id == 19):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 0.6 * S'
        absorption_norm =NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 0.6)
        return requirements, up_to_norm


    if(project_id == 7):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 1.0 * S'
        absorption_norm = NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 1.0)
        return requirements, up_to_norm

    if (project_id == 20 or project_id == 21):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 0.4 * S'
        absorption_norm = NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 0.4)
        return requirements, up_to_norm

    if (project_id == 8):
        if(height <=4):
            requirements = 'Dla pomieszczenia o wysokosci mniejszej badz rownej 4, T musi byc mniejsze badz rowne 0.6s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_less_4).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (height > 4):
            requirements = 'Dla pomieszczenia o wysokosci wiekszej od 4, T musi byc mniejsze badz rowne 0.8s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_between_4_16).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm


    if(project_id == 9):
        if(Volume <= 5000):
            requirements = 'Dla V mniejszego badz rownego 5000m3, T musi byc mniejsze badz rowne 1.5s '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.less_5000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif(Volume > 5000):
            requirements = 'Dla V wiekszego od 5000m3, T musi byc mniejsze badz rowne 1.8s '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.more_5000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

    if(project_id == 10):
        if (Volume <= 5000):
            requirements = 'Dla V mniejszego badz rownego 5000m3, T musi byc mniejsze badz rowne 1.8s '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.less_5000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (Volume > 5000):
            requirements = 'Dla V wiekszego od 5000m3, T musi byc mniejsze badz rowne 2.2s '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.more_5000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

    if(project_id == 12):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 1.1 * S'
        absorption_norm = NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 1.1)
        return requirements, up_to_norm

    if (project_id == 13):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 1.3 * S'
        absorption_norm = NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 1.3)
        return requirements, up_to_norm

    if(project_id == 11):
        if (Volume <= 500):
            requirements = 'Dla V mniejszego badz rownego 500m3, T musi byc mniejsze badz rowne 0.8s a STI wieksze badz rowne 0.6 '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.less_120).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (Volume > 500 and Volume <= 2000):
            requirements = 'Dla V z zakresu od 500m3 do 2000m3, T musi byc mniejsze badz rowne 1.0s a STI wieksze badz rowne 0.6 '
            reverb_time_norm = NormsReverbTimeVolumeReq.query.with_entities(NormsReverbTimeVolumeReq.between_500_2000).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif(Volume > 2000):
            requirements = 'Dla V większego od 2000m3 T oraz STI musi byc okreslone indywidualnie '
            up_to_norm = 'Dla tego typu pomieszczenia nie ma okreslonej normy, nalezy ja wyznaczyc dla tego pomieszczenia'
            return requirements, up_to_norm

    if(project_id == 15):
        requirements = 'Dla kazdego pomieszczenia T musi byc mniejsze badz rowne 0.8s '
        reverb_time_norm = NormsReverbTimeNoReq.query.with_entities(NormsReverbTimeNoReq.no_cubature_req).filter_by(norm_id=project_id).first()
        up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
        return requirements, up_to_norm

    if(project_id == 16 or project_id == 19):
        requirements = 'Dla kazdego pomieszczenia A musi byc wieksze badz rowne 0.8 * S'
        absorption_norm = NormsAbsorptionMultiplayer.query.with_entities(NormsAbsorptionMultiplayer.absorption_multiplayer).filter_by(norm_id=project_id).first()
        up_to_norm = absorption_norm_checker(absorption_list, absorption_norm, surface_area, 0.8)
        return requirements, up_to_norm

    if(project_id == 22 or project_id == 23):
        if (height <= 4):
            requirements = 'Dla pomieszczenia o wysokosci mniejszej badz rownej 4, T musi byc mniejsze badz rowne 1.2s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_less_4).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (height > 4 and height <=16):
            requirements = 'Dla pomieszczenia o wysokosci z zakresu od ponad 4m do 16m , T musi byc mniejsze badz rowne 1.5s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_between_4_16).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (height >16):
            requirements = 'Dla pomieszczenia o wysokosci wiekszej od 16, T musi byc mniejsze badz rowne 1.8s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_more_16).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

    if(project_id == 24):
        if (height <= 4):
            requirements = 'Dla pomieszczenia o wysokosci mniejszej badz rownej 4, T musi byc mniejsze badz rowne 1.5s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_less_4).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (height > 4 and height <=16):
            requirements = 'Dla pomieszczenia o wysokosci z zakresu od ponad 4m do 16m , T musi byc mniejsze badz rowne 2.0s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_between_4_16).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm

        elif (height >16):
            requirements = 'Dla pomieszczenia o wysokosci wiekszej od 16, T musi byc mniejsze badz rowne 2.5s '
            reverb_time_norm = NormsReverbTimeHeightReq.query.with_entities(NormsReverbTimeHeightReq.h_more_16).filter_by(norm_id=project_id).first()
            up_to_norm = reverb_time_norm_checker(reverb_time_norm, reverb_time_list)
            return requirements, up_to_norm




def absorption_norm_checker(absorption_list, absorption_norm,surface_area , multiplayer):
    for i in range(len(absorption_list)):
        if(absorption_list[i] >= absorption_norm * multiplayer):
            up_to_norm = 'Pomieszczenie spelnia wymagana norme'
            return up_to_norm
        else:
            up_to_norm = 'Chlonnosc akustyczna jest niezgodna z norma'
            return up_to_norm

def reverb_time_norm_checker(reverb_time_norm, reverb_time_list):
    reverb_time = float(reverb_time_norm[0])
    for i in range(len(reverb_time_list)):
        if(reverb_time_list[i] <= reverb_time):
            up_to_norm = 'Pomieszczenie spelnia wymagana norme'
            return up_to_norm
        else:
            up_to_norm = 'Czas poglosu jest niezgodny z norma'
            return  up_to_norm
