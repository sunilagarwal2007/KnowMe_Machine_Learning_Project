# import necessary libraries
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template,  jsonify, request
import numpy as np
import pandas as pd
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image


# import sys
# sys.path.append("knowme")
import Execute_Model as execute_model

# Create an instance of our Flask app.
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Flask Routes
#List all routes that are available
@app.route("/")
def welcome():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/api/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

        filepath = destination
        model = load_model("mnist_trained.h5")
        image_size = (28, 28)
       
        # from tensorflow.keras.preprocessing import image
        # from tensorflow.keras.preprocessing.image import img_to_array
        im = image.load_img(filepath, target_size=image_size, color_mode="grayscale")
        image = img_to_array(im)
        image /= 255
        img = image.flatten().reshape(-1, 28*28)
        img = 1 - img
        model.predict_classes(img)

        print(model.predict_classes(img))

        pred = model.predict_classes(img)
        

    return str(pred[0])
    # return render_template("index.html")

# /api/getCountryNames?indicator_code=<indicator_code>
@app.route('/api/getPersonalityTraits', methods=['POST'])
def getPersonalityTraits():
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)
        file = filename

    print("FileName is : "+filename)

    # image_filename = "".join(["knowme/images/",file])
    image_filename = "".join(["knowme/images/",file])
    print("image filename to process: " +image_filename)

    # file = "Michael_HW.png"
    personality_Trait_dict = execute_model.identifyPersonalityTraits(image_filename)

    print("Printin g value of personality_Trait_dict:")
    print(personality_Trait_dict)

    # personality_Trait_dict = {
    #     "Emotional_Stability": "Not Stable",
    #     "Mental_Power": "Low",
    #     "Modesty": "Not Observed",
    #     "Discipline": "Not Observed",
    #     "Concentration": "Observed",
    #     "Social_Isolation": "Observed"
    #     }

    return jsonify(personality_Trait_dict)



# /api/getCountryNames?indicator_code=<indicator_code>
@app.route('/api/getPersonalityTraits_Test', methods=['GET'])
def getPersonalityTraits_Test():
    # link = request.form.get('Link')

    personality_Trait_dict = {
        "Emotional_Stability": "Not Stable",
        "Mental_Power": "Low",
        "Modesty": "Not Observed",
        "Discipline": "Not Observed",
        "Concentration": "Observed",
        "Social_Isolation": "Observed"
        }

    return jsonify(personality_Trait_dict)


    
if __name__ == "__main__":
    app.run(debug=True)
