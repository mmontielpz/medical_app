from flask import Flask,jsonify,request
import json
import pickle

app = Flask(__name__)

@app.route('/heart_cancer_predict' , methods=['POST'])
def heart():
    request_data = request.get_json()
    
    heart_model = 'heart_model.pk'
    
    if not request_data['data']:
        print("Bad request")
        return jsonify({'message':'bad request not data'})
    else:
        #Load the saved model
        print("Loading the model...")
        
        loaded_model = None
        
        with open('./models/'+ heart_model,'rb') as f:
            loaded_model = pickle.load(f)

        print("The model has been loaded...doing predictions now...")

        # Convert json to array
        data  = request_data['data']
        print(data)

        prediction = loaded_model.predict(data)

        # Convert 2D array to 1D
        prediction = prediction.ravel()

        print("[INFO] prediction: " + str(prediction[0]))

        # Conver to bool
        prediction = bool(prediction[0])

        print("Good request")
        return jsonify({'data': prediction})
#   return jsonify(new_store)


if __name__ == '__main__':
    app.run(port=5000, debug=True)