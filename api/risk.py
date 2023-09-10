from flask import (
    Blueprint, request
)

import json

bp = Blueprint('risk', __name__, url_prefix='/risk')

@bp.route('', methods=['GET', 'POST'])
def risk():
    
    # valid request must use POST
    
    if request.method == 'GET':
        
        return "Please use a POST method."
    
    data = request.get_json()
        
    res = get_all_risks(data)
    
    return res

from api.baseline_risk.qrisk3 import QriskModel
from api.baseline_risk.qthrombosis import QthrombosisModel
from api.baseline_risk.qfracture import QfractureModel
from api.baseline_risk.canrisk import CanRisk
import api.hrtrisk as hrt
def get_all_risks(data):
    
    canrisk = CanRisk(data)
    qrisk = QriskModel(data)
    qthrombosis = QthrombosisModel(data)
    qfracture = QfractureModel(data)
    cvd_baseline = qrisk.predict()
    
    
    hazard = hrt.hrt_hazards(
        int(data["age"]),
        int(data.get("menopause_age", "-1")),
        int(data.get("hysterectomy", False))
    )
    
    dict = {
        "breast cancer": 
            {
                "baseline": canrisk.predict(),
                "hazard": hazard["cancer"]
            },
        "chd": 
            {
                "baseline": cvd_baseline,
                "hazard": hazard["chd"]
            },
        "stroke":
            {
                "baseline": cvd_baseline,
                "hazard": hazard["stroke"]
            },
        "vte":
            {
                "baseline": qthrombosis.predict(),
                "hazard": hazard["vte"]
            },
        "fracture":
            {
                "baseline": qfracture.predict(),
                "hazard": hazard["fracture"]
            }
    }
    
    return dict
