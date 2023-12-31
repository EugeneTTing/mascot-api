from api.baseline_risk.riskmodel import RiskModel
from api.baseline_risk.clinrisk import qfracture

class QfractureModel(RiskModel):
    
    def __init__(self, data: dict):
        self.data = data
        
        height = float(data["height"])/100.0
        weight = int(data["weight"])
        bmi = weight / (height * height)
        
        if bmi > 40:
            self.bmi = 40.0
        elif bmi < 20:
            self.bmi = 20.0
        else:
            self.bmi = bmi
        
    def create_args(self):
        
        args = (
            int(self.data["age"]),
            int(self.data["alcohol"]),
            int(self.data.get("antidepressants", False)),
            int(self.data.get("cancer", False)),
            int(self.data.get("copd", False)),
            int(self.data.get("steroids", False)),
            int(self.data.get("cvd", False)),
            int(self.data.get("dementia", False)),
            int(self.data.get("endocrine", False)),
            int(self.data.get("anticonvulsants", False)),
            int(self.data.get("falls", False)),
            int(self.data.get("liver", False)),
            int(self.data.get("malabsorption", False)),
            int(self.data.get("parkin", False)),
            int(self.data.get("ra", False) or self.data.get("sle", False)),
            int(self.data.get("kidney", "none") == "4"),
            int(self.data.get("diabetes", "none") == "1"),
            int(self.data.get("diabetes", "none") == "2"),
            self.bmi,
            int(self.data["ethnicity"]) + 1,
            int(self.data.get("fh_osteo", False)),
            int(self.data["smoking"])
        )
        
        return args
    
    def predict(self):
        
        args = self.create_args()
        
        return qfracture(*args)