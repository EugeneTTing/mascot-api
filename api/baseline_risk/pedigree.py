import datetime


""" 
    Class to format pedigree data of a single family member. Prefix determine which
    family memeber the object is for:
        't_' -- target
        'f_' -- father
        'm_' -- mother
"""
class Pedigree():
    
    def __init__(self, prefix, data):
        self.prefix = prefix
        self.data = data
        
    def createPedigree(self):
        
        # Create array of parameters
        
        params = [
            "01", # FamID
            self.prefix, # Name
            "1" if self.prefix == "t_" else "0", # Target
            self.prefix, # IndivID
            "f_" if self.prefix == "t_" else "0", # FathID
            "m_" if self.prefix == "t_" else "0", # MothID
            "M" if self.prefix == "f_" else "F", # Sex
            "0", # MZtwin
            "0" if self.prefix == "t_" else ("1" if self.data[f"{self.prefix}dead"] else "0"), # Dead
            self.data["age"] if self.prefix == "t_" else self.data[f"{self.prefix}age"], # Age
            str(datetime.date.today().year - int(self.data["age"])) if self.prefix == "t_" else self.data[f"{self.prefix}yob"], # YOB
            self.data.get(f"{self.prefix}br_cancer_age", "0"), # BC1
            self.data.get(f"{self.prefix}br_cancer_2_age", "0"), # BC2
            self.data.get(f"{self.prefix}ov_cancer_age", "0"), # OC
            self.data.get(f"{self.prefix}pr_cancer_age", "0"), # PRO
            self.data.get(f"{self.prefix}pa_cancer_age", "0"), # PAN
            "1" if self.data.get("ash", False) else "0", # Ashkn
            "0:0", # BRCA1
            "0:0", # BRCA2
            "0:0", # PALB2
            "0:0", # ATM
            "0:0", # CHEK2
            "0:0", # BARD1
            "0:0", # RAD51D
            "0:0", # RAD51C
            "0:0", # BRIP1
            "0:0:0:0:0" # ER:PR:HER2:CK14:CK56
        ]
        
        return '\t'.join(params)