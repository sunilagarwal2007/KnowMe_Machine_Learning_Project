import os
import itertools
from sklearn.svm import SVC
from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ExtractFeatures as extract
import categorize
from flask import Flask, jsonify, render_template
from PIL import Image
def crop(image_path):
    outPath = "images"
    path = "images"
    # iterate through the names of contents of the folder
    # for image_path in os.listdir(path): 
     
    if image_path.endswith('.png') or image_path.endswith('.jpg'):
        # establish input path
        input_path = os.path.join(path, image_path)
        # open & read each image in loop
        image = Image.open(input_path)
        # crop each image in dir
        x = 350
        y = 350
        cropped_image = image.crop( ( x, y, x + 2200 , y + 2200 ) )
        # create full path process for forloop and deposit into new directory
        image_path = image_path[:-3] + 'png'
        fullpath = os.path.join(outPath, 'crop_'+image_path)
        # print(fullpath)
        cropped_image.save(fullpath)
        new_file_name = 'crop_'+image_path
    return new_file_name

def resize(filename):
    image_path = crop(filename)

    outPath = "images"
    path = "images"
    # iterate through the names of contents of the folder
    # for image_path in os.listdir(path):  
    if image_path.endswith('.png') or image_path.endswith('.jpg'):
        # establish input path
        input_path = os.path.join(path, image_path)
        # open & read each image in loop
        image = Image.open(input_path)
        # transform the image into the necessary 850x850 pixel requirements
        image = image.resize((850,850), Image.ANTIALIAS)
        # create full path process for forloop and deposit into new directory
        image_path = image_path[:-3] + 'png'
        fullpath = os.path.join(outPath, 'resize_'+image_path)
        image.save(fullpath)

        new_file_name = 'resize_'+image_path
    return new_file_name

def identifyPersonalityTraits(file_name_orig):

    clf_emotional_stability = load('knowme_EmotionalSt.joblib')
    clf_knowme_MentalE_WlPower = load('knowme_MentalE_WlPower.joblib')
    clf_knowme_Modesty = load('knowme_Modesty.joblib')
    clf_lackOfDiscipline = load('lackOfDiscipline.joblib')
    clf_PoorConcentration = load('PoorConcentration.joblib')
    clf_SocialIsolation = load('SocialIsolation.joblib')

    # file_name_orig ="Michael_HW.png"  
    # crop(file_name_orig)
    file_name = resize(file_name_orig)

    raw_features = extract.start(file_name)        
    raw_baseline_angle = raw_features[0]
    baseline_angle, comment = categorize.determine_baseline_angle(raw_baseline_angle)
    print ("Baseline Angle: "+comment)
    
    raw_top_margin = raw_features[1]
    top_margin, comment = categorize.determine_top_margin(raw_top_margin)
    print("Top Margin: "+comment)
        
    raw_letter_size = raw_features[2]
    letter_size, comment = categorize.determine_letter_size(raw_letter_size)
    print ("Letter Size: "+comment)
    
    raw_line_spacing = raw_features[3]
    line_spacing, comment = categorize.determine_line_spacing(raw_line_spacing)
    print ("Line Spacing: "+comment)
    
    raw_word_spacing = raw_features[4]
    word_spacing, comment = categorize.determine_word_spacing(raw_word_spacing)
    print ("Word Spacing: "+comment)
    
    raw_pen_pressure = raw_features[5]
    pen_pressure, comment = categorize.determine_pen_pressure(raw_pen_pressure)
    print ("Pen Pressure: "+comment)
    
    raw_slant_angle = raw_features[6]
    slant_angle, comment = categorize.determine_slant_angle(raw_slant_angle)
    print ("Slant: "+comment)

    emotional_stability= clf_emotional_stability.predict([[baseline_angle, slant_angle]])
    MentalE_WlPower = clf_knowme_MentalE_WlPower.predict([[letter_size, pen_pressure]])
    Modesty = clf_knowme_Modesty.predict([[letter_size, top_margin]])
    Discipline= clf_lackOfDiscipline.predict([[slant_angle, top_margin]])
    Concentration= clf_PoorConcentration.predict([[letter_size, line_spacing]])
    SocialIsolation= clf_SocialIsolation.predict([[line_spacing, word_spacing]])

    if(emotional_stability[0]==1):
        emotional_stability = "Stable"
    else:
        emotional_stability = "Not Stable"
    if(MentalE_WlPower[0]==1):
        MentalE_WlPower = "High or Average"
    else:
        MentalE_WlPower = "Low"
    if(Modesty[0]==1):
        modesty= "Observed"
    else:
        modesty= "Not Observed"
    if(Concentration[0]==1):
        concentration= "Observed"
    else:
        concentration= "Not Observed"
    if(Discipline[0]==1):
        discipline= "Observed"
    else:
        discipline= "Not Observed"
    if(SocialIsolation[0]==1):
        SocialIsolation= "Observed"
    else:
        SocialIsolation= "Not Observed"
    
    personality_Trait_dict = {
    "Emotional_Stability": emotional_stability ,
    "Mental_Power": MentalE_WlPower,
    "Modesty": modesty,
    "Discipline": discipline,
    "Concentration": concentration,
    "Social_Isolation": SocialIsolation
    }

    print(personality_Trait_dict)
    return personality_Trait_dict



input_file_name ="Michael_HW.png" 

personality_Trait_dict = identifyPersonalityTraits(input_file_name)
print("Printin g value of personality_Trait_dict:")
print(personality_Trait_dict)