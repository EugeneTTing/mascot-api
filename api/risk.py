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

import api.baseline_risk.canrisk as cr
import api.baseline_risk.hrtrisk as hrt
import api.baseline_risk.clinrisk as clin
def get_all_risks(data):
    
    menopause_age = int(data.get("menopause_age", "-1"))
    
    hazard = hrt.hrt_hazards(
        int(data["age"]),
        menopause_age,
        int(data["hysterectomy"])
    )
    
    cvd_baseline = clin.cvd_baseline(data)
    
    dict = {
        "breast cancer": 
            {
                "baseline": cr.breast_cancer_baseline(data),
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
                "baseline": clin.vte_baseline(data),
                "hazard": hazard["vte"]
            },
        "fracture":
            {
                "baseline": clin.fracture_baseline(data),
                "hazard": hazard["fracture"]
            }
    }
    
    return dict
