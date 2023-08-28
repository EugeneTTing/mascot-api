from api.baseline_risk.riskmodel import RiskModel
from api.baseline_risk.clinrisk import qthrombosis

class QthrombosisModel(RiskModel):
    
    def __init__(self, data: dict):
        self.data = data
    
    def create_args(self):
        
        args = (
            int(self.data["age"]),
            int(self.data.get("heart_failure", False)),
            int(self.data.get("hospital", False)),
            int(self.data.get("antipsy", "none") != "none"),
            int(self.data.get("cancer", False)),
            int(self.data.get("oral_c", "never") == "current"),
            int(self.data.get("copd", False)),
            int(self.data.get("malabsorption", False)),
            int(self.data.get("kidney", "none") != "none"),
            int(self.data.get("tamoxifen", False)),
            int(self.data.get("varicose_vein", False)),
            float(self.data["weight"])/((float(self.data["height"]) / 100) ** 2),
            int(self.data["smoking"]),
            0
        )
        
        return args
    
    def predict(self):
        
        args = self.create_args()
        
        return qthrombosis(*args)