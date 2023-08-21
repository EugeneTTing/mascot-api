from math import log, exp

def cvd_baseline(data):
    args = (
        int(data["age"]),
        int(data["af"]),
        int(data["antipsy"] == "atyp"),
        int(data["steroids"]),
        int(data["migraine"]),
        int(data["ra"]),
        int(data["kidney"] != "none"),
        int(data["semi"]),
        int(data["sle"]),
        int(data["hypert_treat"]),
        int(data["diabetes"] == "1"),
        int(data["diabetes"] == "2"),
        float(data["weight"])/((float(data["height"]) / 100) ** 2),
        int(data["ethnicity"]) + 1,
        int(data["fh_cvd"]),
        125,
        4,
        0,
        int(data["smoking"]),
        0,
    )
    return qrisk3(*args)

# Still broken???
def qrisk3(
    age: int, # age
    b_af: int, # atrial fibrilation
    b_atypicalantipsy: int, # atypical antipsychotics
    b_corticosteroids: int, # steroids
    b_migraine: int, # migraines
    b_ra: int, # rheumatoid athritis
    b_renal: int, # kidney
    b_semi: int, # severe mental illness
    b_sle: int, # lupus
    b_treatedhyp: int, # blood pressure treatment
    b_type1: int, # type 1 diabetes
    b_type2: int, # type 2 diabetes
    bmi: float, # bmi
    ethrisk: int, # ethnicity
    fh_cvd: int, # family history cvd
    rati: float, # cholesterol HDL ratip 
    sbp: float, # systolic bp 
    sbps5: float, # systolic bp std 
    smoke_cat: int, # smoking status
    town: float # Townsend deprivation score
) -> float:
    
    survivor = 0.988876402378082 # 10 year risk
    
    # conditional arrays
    
    ethrisk_arr = [
        0,
		0, # White or not stated
		0.2804031433299542500000000, # Indian
		0.5629899414207539800000000,
		0.2959000085111651600000000,
		0.0727853798779825450000000,
		-0.1707213550885731700000000,
		-0.3937104331487497100000000,
		-0.3263249528353027200000000,
		-0.1712705688324178400000000
    ]
    
    smoke_arr = [
        0,
		0.1338683378654626200000000,
		0.5620085801243853700000000,
		0.6674959337750254700000000,
		0.8494817764483084700000000
    ]
    
    # apply fractional polynomial transforms
    
    d_age = age / 10.0
    age_1 = pow(d_age, -2)
    age_2 = d_age
    d_bmi = bmi / 10.0
    bmi_1 = pow(d_bmi, -2)
    bmi_2 = pow(d_bmi, -2) * log(d_bmi)
        
    # centring contrinuous variables
    
    age_1 -= 0.053274843841791
    age_2 -= 4.332503318786621
    bmi_1 -= 0.154946178197861
    bmi_2 -= 0.144462317228317
    rati -= 3.476326465606690
    sbp -= 123.130012512207030
    sbps5 -= 9.002537727355957
    town -= 0.392308831214905
    
    # start of sum
    
    a = 0.0
    
    # conditional sum
    
    a += ethrisk_arr[ethrisk]
    a += smoke_arr[smoke_cat]   
    
    # sum from continuous values
    
    a += age_1 * -8.1388109247726188000000000
    a += age_2 * 0.7973337668969909800000000
    a += bmi_1 * 0.2923609227546005200000000
    a += bmi_2 * -4.1513300213837665000000000
    a += rati * 0.1533803582080255400000000
    a += sbp * 0.0131314884071034240000000
    a += sbps5 * 0.0078894541014586095000000
    a += town * 0.0772237905885901080000000
    
    # sum from boolean values

    a += b_af * 1.5923354969269663000000000
    a += b_atypicalantipsy * 0.2523764207011555700000000
    a += b_corticosteroids * 0.5952072530460185100000000
    a += b_migraine * 0.3012672608703450000000000
    a += b_ra * 0.2136480343518194200000000
    a += b_renal * 0.6519456949384583300000000
    a += b_semi * 0.1255530805882017800000000
    a += b_sle * 0.7588093865426769300000000
    a += b_treatedhyp * 0.5093159368342300400000000
    a += b_type1 * 1.7267977510537347000000000
    a += b_type2 * 1.0688773244615468000000000
    a += fh_cvd * 0.4544531902089621300000000
    
    
    # sum from interaction terms

    a += age_1 * (smoke_cat==1) * -4.7057161785851891000000000
    a += age_1 * (smoke_cat==2) * -2.7430383403573337000000000
    a += age_1 * (smoke_cat==3) * -0.8660808882939218200000000
    a += age_1 * (smoke_cat==4) * 0.9024156236971064800000000
    a += age_1 * b_af * 19.9380348895465610000000000
    a += age_1 * b_corticosteroids * -0.9840804523593628100000000
    a += age_1 * b_migraine * 1.7634979587872999000000000
    a += age_1 * b_renal * -3.5874047731694114000000000
    a += age_1 * b_sle * 19.6903037386382920000000000
    a += age_1 * b_treatedhyp * 11.8728097339218120000000000
    a += age_1 * b_type1 * -1.2444332714320747000000000
    a += age_1 * b_type2 * 6.8652342000009599000000000
    a += age_1 * bmi_1 * 23.8026234121417420000000000
    a += age_1 * bmi_2 * -71.1849476920870070000000000
    a += age_1 * fh_cvd * 0.9946780794043512700000000
    a += age_1 * sbp * 0.0341318423386154850000000
    a += age_1 * town * -1.0301180802035639000000000
    a += age_2 * (smoke_cat==1) * -0.0755892446431930260000000
    a += age_2 * (smoke_cat==2) * -0.1195119287486707400000000
    a += age_2 * (smoke_cat==3) * -0.1036630639757192300000000
    a += age_2 * (smoke_cat==4) * -0.1399185359171838900000000
    a += age_2 * b_af * -0.0761826510111625050000000
    a += age_2 * b_corticosteroids * -0.1200536494674247200000000
    a += age_2 * b_migraine * -0.0655869178986998590000000
    a += age_2 * b_renal * -0.2268887308644250700000000
    a += age_2 * b_sle * 0.0773479496790162730000000
    a += age_2 * b_treatedhyp * 0.0009685782358817443600000
    a += age_2 * b_type1 * -0.2872406462448894900000000
    a += age_2 * b_type2 * -0.0971122525906954890000000
    a += age_2 * bmi_1 * 0.5236995893366442900000000
    a += age_2 * bmi_2 * 0.0457441901223237590000000
    a += age_2 * fh_cvd * -0.0768850516984230380000000
    a += age_2 * sbp * -0.0015082501423272358000000
    a += age_2 * town * -0.0315934146749623290000000
    
    # caluclate and return score
    return 100.0 * (1 - pow(survivor, exp(a)))

def vte_baseline(data):
    args = (
        int(data["age"]),
        int(data["heart_failure"]),
        int(data["hospital"]),
        int(data["antipsy"] != "none"),
        int(data["cancer"]),
        int(data["oral_c"] == "current"),
        int(data["copd"]),
        int(data["malabsorption"]),
        int(data["kidney"] != "none"),
        int(data["tamoxifen"]),
        int(data["varicose_vein"]),
        float(data["weight"])/((float(data["height"]) / 100) ** 2),
        int(data["smoking"]),
        0
    )
    return qthrombosis(*args)
    
def qthrombosis(
    age, # age
    b_CCF, # heart failure
    b_admit, # admitted to hospital
    b_antipsychotic, # antipsychotics
    b_anycancer, # any cancer
    b_cop, # oral cotraceptive
    b_copd, # chronic obsturctive airway
    b_ibd, # crohns
    b_renal, # kidney
    b_tamoxifen, # tamoxifen
    b_varicosevein, # varicose vein surgery
    bmi, # bmi
    smoke_cat, # smoking
    town # Townsend
):
    
    survivor = 0.996479928493500 # 5 year risk
    
    # conditional arrays
    
    smoke_arr = [
        0,
		0.0899056072614921040000000,
		0.2096026499560841000000000,
		0.2698567860827917900000000,
		0.3777926716180949300000000
    ]
    
    # apply fractional polynomial transforms
    
    d_age = age / 10.0
    age_1 = pow(d_age, -0.5)
    age_2 = log(d_age)
    d_bmi = bmi / 10.0
    bmi_1 = pow(d_bmi, -2)
    bmi_2 = bmi_1 * log(d_bmi)
    
    # centring the continuous variables
    
    age_1 -= 0.461668938398361
    age_2 -= 1.545814394950867
    bmi_1 -= 0.146233677864075
    bmi_2 -= 0.140570744872093
    town -= 0.081886291503906
    
    # start of sum
    
    a = 0.0
    
    # conditional sum
    
    a += smoke_arr[smoke_cat]
    
    # sum from continuous values
    
    a += age_1 * 44.3830463834610500000000000
    a += age_2 * 12.4309633619714290000000000
    a += bmi_1 * 4.2938468556841043000000000
    a += bmi_2 * -22.6864658094973740000000000
    a += town * 0.0243256958103135540000000
    
    # sum from boolean values
    
    a += b_CCF * 0.3203585274547171600000000
    a += b_admit * 0.3648270417062697800000000
    a += b_antipsychotic * 0.5419744307906361200000000
    a += b_anycancer * 0.5073551208032194300000000
    a += b_cop * 0.2651727310274107400000000
    a += b_copd * 0.3973172060275547700000000
    a += b_ibd * 0.4023036851423945100000000
    a += b_renal * 0.4367724008370839100000000
    a += b_tamoxifen * 0.3673289784136273300000000
    a += b_varicosevein * 0.3907194593022829700000000
    
    # calculate and return score
    
    return 100.0 * (1 - pow(survivor, exp(a)))

def fracture_baseline(data):
    args = (
        int(data["age"]),
        int(data["alcohol"]),
        int(data["antidepressants"]),
        int(data["cancer"]),
        int(data["copd"]),
        int(data["steroids"]),
        int(data["cvd"]),
        int(data["dementia"]),
        int(data["endocrine"]),
        int(data["anticonvulsants"]),
        int(data["falls"]),
        int(data["liver"]),
        int(data["malabsorption"]),
        int(data["parkin"]),
        int(data["ra"] or data["sle"]),
        int(data["kidney"] == "4"),
        int(data["diabetes"] == "1"),
        int(data["diabetes"] == "2"),
        float(data["weight"])/((float(data["height"]) / 100) ** 2),
        int(data["ethnicity"]) + 1,
        int(data["fh_osteo"]),
        int(data["smoking"])
    )
    
    return qfracture(*args)

def qfracture(
    age, # age
    alcohol_cat, # alcohol category
    b_antidepressant, # antidepressants
    b_anycancer, # cancer
    b_asthmacopd, # asthma or copd
    b_corticosteroids, # steroids
    b_cvd, # cardiovascular disease
    b_dementia, # dementia
    b_endocrine, # endocrine problems
    b_epilepsy2, # epilepsy or anticonvulsants
    b_falls, # history of falls
    b_liver, # liver disease
    b_malabsorption, # malabsorption
    b_parkinsons, # parkinsons
    b_ra_sle, # ra or sle
    b_renal, # kidney
    b_type1, # type 1 diabetes
    b_type2, # type 2 diabetes
    bmi, # bmi
    ethrisk, # ethnicity
    fh_osteoporosis, # family history osteoporosis
    smoke_cat # smoking
):
    
    survivor = 0.991504669189453 # 5 year risk
    
    # conditional arrays
    
    alcohol_arr = [
        0,
		-0.0161196598427115580000000,
		0.0181421919546882990000000,
		0.0870398130913111050000000,
		0.4850876681648371200000000,
		0.4521470045723863200000000
    ]
    
    ethrisk_arr = [
        0,
		0,
		-0.4256606921636625400000000,
		-0.5543209119502141600000000,
		-0.9182601097806930600000000,
		-0.6819360653148304200000000,
		-1.4668483404988077000000000,
		-0.9101238114228446000000000,
		-0.6421783317544739200000000,
		-0.5036829432634510900000000
    ]
    
    smoke_arr = [
        0,
		0.0557356934305611660000000,
		0.1633895661701352800000000,
		0.1540488338696587000000000,
		0.2329771591757904500000000
    ]
    
    # apply fractional polynomial transforms
    
    d_age = age / 10.0
    age_1 = pow(d_age, 2)
    age_2 = pow(d_age, 3)
    d_bmi = bmi / 10.0
    bmi_1 = pow(d_bmi, -1)
    
    # centring continuous variable
    
    age_1 -= 25.463895797729492
    age_2 -= 128.495315551757810
    bmi_1 -= 0.382189363241196
    
    # start of sum
    
    a = 0.0
    
    # conditional sum
    
    a += alcohol_arr[alcohol_cat]
    a += ethrisk_arr[ethrisk]
    a += smoke_arr[smoke_cat]
    
    # sum continuous values
    
    a += age_1 * 0.1488230617216508300000000
    a += age_2 * -0.0095516624764288762000000
    a += bmi_1 * 2.8180291389827810000000000
    
    # sum boolean values
    
    a += b_antidepressant * 0.2935891578881283900000000
    a += b_anycancer * 0.1175522733147793100000000
    a += b_asthmacopd * 0.1997193753352899900000000
    a += b_corticosteroids * 0.2187020094246774900000000
    a += b_cvd * 0.1419643725503051700000000
    a += b_dementia * 0.4697387263085152100000000
    a += b_endocrine * 0.1105394028217592300000000
    a += b_epilepsy2 * 0.4024460098604033000000000
    a += b_falls * 0.3322321626303583700000000
    a += b_liver * 0.4831161576961586200000000
    a += b_malabsorption * 0.1687477801835574600000000
    a += b_parkinsons * 0.4742239358039181400000000
    a += b_ra_sle * 0.2267059327471904200000000
    a += b_renal * 0.2508648723794006400000000
    a += b_type1 * 0.7832887160932293600000000
    a += b_type2 * 0.2363869657814060800000000
    a += fh_osteoporosis * 0.3837949755860494700000000
    
    # calculate and return score
    
    return 100.0 * (1 - pow(survivor, exp(a)))

# qrisk test
# Baseline test: 55 yo, all ethnicities, mean UK Townsend score -0.35
# https://s3-eu-west-1.amazonaws.com/statistics.digitalresources.jisc.ac.uk/dkan/files/Townsend_Deprivation_Scores/UK%20Townsend%20Deprivation%20Scores%20from%202011%20census%20data.pdf
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 1, 0, 4, 125, 0, 0, 0))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 2, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 3, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 4, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 5, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 6, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 7, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 8, 0, 4, 125, 0, 0, -0.35))
# print(qrisk3(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 9, 0, 4, 125, 0, 0, -0.35))

# qthrombosis test
# print(qthrombosis(60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25.39, 0, 0)) # 0.7
# print(qthrombosis(65, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31.11, 4, 0)) # 1.9
# print(qthrombosis(40, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 20.81, 2, 0)) # 0.9
# print(qthrombosis(50, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 21.6, 1, 0)) # 3.7
# print(qthrombosis(55, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 20.76, 0, 0)) # 2

# qfracture tests
# for i in range(1, 10):
#     print(i)
#     print(qfracture(55, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25.39, i, 0, 0))

# print(qfracture(65, 2, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 25.39, 1, 0, 2)) # 9.5
# print(qfracture(70, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 38.05, 6, 1, 3)) # 3.7
# print(qfracture(50, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 26.16, 8, 0, 0)) # 4.8
# print(qfracture(80, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 18.52, 4, 0, 4)) # 10.4