import os
from os.path import join, dirname
from dotenv import load_dotenv
import requests
import datetime

### Create CanRisk pedigree file from data passed in

def pedigree_file(data: dict) -> str:
    
    file = "##CanRisk 2.0\n"
    
    # Optional target headers
    headers = {
        "menarche": "##Menarhche=",
        "num_children": "##Parity=",
        "age_at_first_child": "##First_live_birth=",
        "menopause_age": "##Menopause=",
        "height": "##Height=",
    }
    for key, value in headers.items():
        file += value + data.get(key, "NA") + '\n'
        
    oc_use = data["oral_c"]
    if oc_use != "never":
        file += "##OC_use="
        if oc_use == "former":
            file += "F:"
        else:
            file += "C:"
        file += data["oral_c_years"] + '\n'
        
    height = float(data["height"])/100.0
    weight = int(data["weight"])
    file += "##BMI=" + str(weight / (height * height)) + '\n'
    
    alcohol = [
        0,
        0.5,
        1.5,
        4.5,
        8,
        12
    ] # mean units of range from form
    file += "##Alcohol=" + str(alcohol[int(data["alcohol"])] * 8) + '\n'
    
    file += "##FamID Name Target IndivID FathID MothID Sex MZtwin Dead Age Yob BC1 BC2 OC PRO PAN Ashkn BRCA1 BRCA2 PALB2 ATM CHEK2 BARD1 RAD51D RAD51C BRIP1 ER:PR:HER2:CK14:CK56\n"

    # Target pedigree data
    file += "01\ttarget\t1\tta\tfa\tmo\tF\t0\t0\t"
    file += data["age"] + '\t'
    file += str(datetime.date.today().year - int(data["age"])) + '\t'
    file += "0\t0\t0\t0\t0\t"
    if data["ash"]:
        file += "1\t"
    else:
        file += "0\t"
    file += "0:0\t" * 9 + "0:0:0:0:0\n"
    
    # Mother pedigree data
    file += "01\tmother\t0\tmo\t0\t0\tF\t0\t"
    if data["m_dead"]:
        file += "1\t"
    else:
        file += "0\t"
    file += data["m_age"] + '\t'
    file += data["m_yob"] + '\t'
    file += data.get("m_br_cancer_age", "0") + '\t'
    file += data.get("m_br_cancer_2_age", "0") + '\t'
    file += data.get("m_ov_cancer_age", "0") + '\t'
    file += "0\t"
    file += data.get("m_pa_cancer_age", "0") + '\t'
    if data["ash"]:
        file += "1\t"
    else:
        file += "0\t"
    file += "0:0\t" * 9 + "0:0:0:0:0\n"
    
    # Father pedigree data
    file += "01\tfather\t0\tfa\t0\t0\tM\t0\t"
    if data["f_dead"]:
        file += "1\t"
    else:
        file += "0\t"
    file += data["f_age"] + '\t'
    file += data["f_yob"] + '\t'
    file += "0\t0\t0\t"
    file += data.get("f_pr_cancer_age", "0") + '\t'
    file += data.get("f_pa_cancer_age", "0") + '\t'
    if data["ash"]:
        file += "1\t"
    else:
        file += "0\t"
    file += "0:0\t" * 9 + "0:0:0:0:0\n"
    
    # print(file)
    
    return file

def auth_token() -> str:
    
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    url = os.environ.get("CANRISK_URL")
    uname = os.environ.get("CANRISK_USERNAME")
    pword = os.environ.get("CANRISK_PASSWORD")
    
    payload = {
        "username": uname,
        "password": pword
    }
    
    r = requests.post(f"{url}/auth-token/", json=payload)
    return r.json()["token"]

def breast_cancer_baseline(data: dict):

    ped = pedigree_file(data)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    url = os.environ.get("CANRISK_URL")
    token = auth_token()
    
    payload = {
        "pedigree_data": ped,
        "user_id": "mascot",
        "cancer_rates": "UK",
        "mut_freq": "UK",
    }
    
    r = requests.post(
        f"{url}/boadicea/",
        headers= {"Authorization": f"Token {token}"},
        json=payload 
    )
    
        
    return (r.json()["pedigree_result"][0]["cancer_risks"][4]["breast cancer risk"]["percent"])

# def create_pedigree_file(target_risk_factors: dict[str, str], pedigree_data: list[dict[str, str]]) -> str:
    
#     file = "##CanRisk 2.0\n"
    
#     for key, value in headers.items():
#         file += value + target_risk_factors[key] + '\n'

#     file += "##FamID Name Target IndivID FathID MothID Sex MZtwin Dead Age Yob BC1 BC2 OC PRO PAN Ashkn BRCA1 BRCA2 PALB2 ATM CHEK2 BARD1 RAD51D RAD51C BRIP1 ER:PR:HER2:CK14:CK56\n"
    
#     for ped in pedigree_data:
        
#         role = ped["role"]
        
#         file += "0001\t" + role + '\t'
        
#         if role == "target":
#             file = file + "1\tT\tF\tM\tF\t0\t"
#         elif role == "mother":
#             file = file + "0\tM\t0\t0\tF\t0\t"
#         elif role == "father":
#             file = file + "0\tF\t0\t0\tM\t0\t"
            
#         file += ped["dead"] + '\t' + ped["age"] + '\t'
        
#         try:
#             file += ped["yob"] + '\t'
#         except:
#             file += str(datetime.date.today().year - int(ped["age"])) + '\t'
            
#         file += ped["bc1"] + '\t' + ped["bc2"] + '\t' + ped["oc"] + '\t' + ped["pro"] + '\t' + ped["pan"] + '\t' + ped["ashkn"] + '\t'
        
#         file += "0:0\t" * 9 + "0:0:0:0:0\n" 
    
#     return file

# def target_dict(data):
    
#     dict = {}
#     dict["menarche"] = data["menopause_age"]
    
#     if not data["has_children"]:
#         dict["parity"] = "0"
#         dict["age_first_birth"] = "0"
#     else:
#         dict["parity"] = data["num_children"]
#         dict["age_first_birth"] = data["age_at_first_child"]
        
#     oc_use = data["oral_c"]
#     if oc_use == "never":
#         dict["oc"] = "N"
#     elif oc_use == "former":
#         dict["oc"] = "F:" + data["oral_c_years"]
#     else:
#         dict["oc"] = "C:" + data["oral_c_years"]
    
#     height = float(data["height"])/100.0
#     weight = int(data["weight"])
    
#     dict["bmi"] = str(weight / (height * height))
    
#     alcohol = [
#         0,
#         0.5,
#         1.5,
#         4.5,
#         8,
#         12
#     ] # average units
    
#     dict["alcohol"] = str(alcohol[int(data["alcohol"])] * 8)
#     # 1 unit is 8 grams of alcohol
    
#     if data["menopause"]:
#         dict["menopause"] = data["menopause_age"]
#     else:
#         dict["menopause"] = "NA"
        
#     dict["height"] = data["height"]
    
#     return dict
    
# def pedigree_dict(data):
    
#     dict = [
#         {
#             "role": "mother",
#             "dead": "0",
#             "age": data["m_age"],
#             "yob": data["m_yob"],
#             "bc1": "0",
#             "bc2": "0",
#             "oc": "0",
#             "pro": "0",
#             "pan": "0",
#             "ashkn": "0"
#         },
#         {
#             "role": "father",
#             "dead": "0",
#             "age": data["f_age"],
#             "yob": data["f_yob"],
#             "bc1": "0",
#             "bc2": "0",
#             "oc": "0",
#             "pro": "0",
#             "pan": "0",
#             "ashkn": "0"    
#         },
#         {
#             "role": "target",
#             "dead": "0",
#             "age": data["age"],
#             "yob": str(datetime.date.today().year - int(data["age"])),
#             "bc1": "0",
#             "bc2": "0",
#             "oc": "0",
#             "pro": "0",
#             "pan": "0",
#             "ashkn": "0"
#         }
#     ]
    
#     if data["m_br_cancer"]:
#         dict[0]["bc1"] = data["m_br_cancer_age"]
        
#     if data["m_br_cancer_2"]:
#         dict[0]["bc2"] = data["m_br_cancer_2_age"]
        
#     if data["m_ov_cancer"]:
#         dict[0]["oc"] = data["m_ov_cancer_age"]
        
#     if data["m_pa_cancer"]:
#         dict[0]["pan"] = data["m_pa_cancer_age"]
        
#     if data["f_pr_cancer"]:
#         dict[1]["pro"] = data["f_pr_cancer_age"]
        
#     if data["f_pa_cancer"]:
#         dict[1]["pan"] = data["f_pa_cancer_age"]
        
#     if data["m_dead"]:
#         dict[0]["dead"] = "1"
        
#     if data["f_dead"]:
#         dict[1]["dead"] = "1"
        
#     if data["ash"]:
#         for d in dict:
#             d["ashkn"] = "1"
        
#     return dict
    
# example_target_risk_factors = {
#     "menarche": "12",
#     "parity": "2",
#     "age_first_birth": "35",
#     "oc": "F:5",
#     "mht": "E",
#     "bmi": "20",
#     "alcohol": "32",
#     "menopause": "56",
#     "height": "160",
# }

# example_pedigree_data = [
#     {
#         "role": "mother",
#         "dead": "1",
#         "age": "67",
#         "yob": "1951",
#         "bc1": "0",
#         "bc2": "0",
#         "oc": "63",
#         "pro": "0",
#         "pan": "0",
#         "ashkn": "0"
#     },
#     {
#         "role": "father",
#         "dead": "0",
#         "age": "86",
#         "bc1": "0",
#         "bc2": "0",
#         "oc": "0",
#         "pro": "84",
#         "pan": "0",
#         "ashkn": "0"
#     },
#     {
#         "role": "target",
#         "dead": "0",
#         "age": "55",
#         "bc1": "51",
#         "bc2": "0",
#         "oc": "0",
#         "pro": "0",
#         "pan": "0",
#         "ashkn": "0"
#     }
# ]

# print(breast_cancer_risk(example_target_risk_factors, example_pedigree_data))