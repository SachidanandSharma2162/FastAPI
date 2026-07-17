from fastapi.responses import JSONResponse
import pandas as pd
import pickle

MODEL_VERSION="1.0.0"
with open("model/model.pkl","rb") as f:
    model=pickle.load(f)

class_labels = model.classes_.tolist()

def predict_output(user_input:dict):
    input_df=pd.DataFrame([user_input])
    try:
        predicted_class = model.predict(input_df)[0]

        # Get probabilities for all classes
        probabilities = model.predict_proba(input_df)[0]
        confidence = max(probabilities)
        
        # Create mapping: {class_name: probability}
        class_probs = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
    
        return {
            "predicted_category": predicted_class,
            "confidence": round(confidence, 4),
            "class_probabilities": class_probs
        }
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))