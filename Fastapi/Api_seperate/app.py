from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput #importing pydantic model from schema folder
from model.predict import predict_op,MODEL_VERSION,model
from schema.op_model import PredictionResponse
app = FastAPI()

#human readable
@app.get("/")
def home():
    return {'message':"Insurance Premium Prediction API"}

#machine readable(services like aws,kubernetes)
@app.get('/health')
def health_check():
    return{
        'status':"OK",
        "Version":"1.0.0",
        'model_loaded':model is not None
    }

@app.post('/predict',response_model=PredictionResponse)
def predict_premium(data :UserInput):

    user_input = {
    'bmi': data.bmi,
    'age_group': data.age_group,
    'lifestyle_risk': data.lifestyle_risk,
    'city_tier': data.city_tier,
    'income_lpa': data.income_lpa,
    'occupation': data.occupation
    }

    try:
        prediction = predict_op(user_input)
        return JSONResponse(
                status_code=200, 
                content={"response": str(prediction)}
            )
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
    
