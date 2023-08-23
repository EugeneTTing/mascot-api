vte_arr = [1.73, 1.4]

cancer_arr =[[1.08, 1.42], [1.12, 1.34], [1.13, 1.49], [1.26, 1.62]]

cvd_arr = [(0.52, 1.37), (1.07, 1.21)]

def hrt_vte(hysterectomy: int) -> float:
    return vte_arr[hysterectomy]

def hrt_cancer(age: int, hysterectomy: int) -> float:
    if age < 50:
        return cancer_arr[0][hysterectomy]
    elif age < 60:
        return cancer_arr[1][hysterectomy]
    elif age < 70:
        return cancer_arr[2][hysterectomy]
    else:
        return cancer_arr[3][hysterectomy]
        
def hrt_cvd(age: int, age_at_menopause: int) -> tuple[float, float]:
    if age_at_menopause == -1 and age < 60:
        return cvd_arr[0]
    if age < 60 or age - age_at_menopause < 10:
        return cvd_arr[0]
    return cvd_arr[1]

def hrt_hazards(age: int, age_at_menopause: int, hysterectomy: int) -> dict[str, float]:
    dict = {}
    dict["cancer"] = hrt_cancer(age, hysterectomy)
    dict["vte"] = hrt_vte(hysterectomy)
    cvd = hrt_cvd(age, age_at_menopause)
    dict["chd"] = cvd[0]
    dict["stroke"] = cvd[1]
    dict["fracture"] = 0.74
    return dict
