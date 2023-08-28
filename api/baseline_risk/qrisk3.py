from api.baseline_risk.riskmodel import RiskModel
from api.baseline_risk.clinrisk import qrisk3

class QriskModel(RiskModel):
    
    def __init__(self, data: dict):
        self.data = data
        
    def create_args(self):
        args = (
            int(self.data["age"]),
            int(self.data.get("af", False)),
            int(self.data.get("antipsy", "none") == "atyp"),
            int(self.data.get("steroids", False)),
            int(self.data.get("migraine", False)),
            int(self.data.get("ra", False)),
            int(self.data.get("kidney", "none") != "none"),
            int(self.data.get("semi", False)),
            int(self.data.get("sle", False)),
            int(self.data.get("hypert_treat", False)),
            int(self.data.get("diabetes", "none") == "1"),
            int(self.data.get("diabetes", "none") == "2"),
            float(self.data["weight"])/((float(self.data["height"]) / 100) ** 2),
            int(self.data["ethnicity"]) + 1,
            int(self.data.get("fh_cvd", False)),
            int(self.data.get("ratio", 4)),
            int(self.data.get("sbp", 125)),
            0,
            int(self.data["smoking"]),
            0,
        )
        return args
        
    def predict(self):
        
        args = self.create_args()
        
        return qrisk3(*args)