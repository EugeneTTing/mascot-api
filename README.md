Run `flask --app api run --debug`  in the terminal to start developmental server.

## Endpoints

`/risk`

Calculate health risks. Questionnaire answers sent in JSON as POST request payload.

## Risk Factors Used

### Coronary Heart Disease and Stroke

Source: https://qrisk.org/index.php

- Age
- Atrial fibrilation
- Atypical antipsychotics
- Corticosteroids
- Migraines
- Rheumatoid Arthritis
- Kidney disease
- Severe mental illness
- Lupus
- Blood pressure treatment
- Diabetes
- BMI
- Ethnicity
- Family history of cardiovascular disease
- Cholesterol / HDL ratio
- Systolic bloop pressure
- Standard deviation of systolic blood pressure
- Smoking status
- Townsend deprivation score

### Vernous Thromboembolism

Source: https://qthrombosis.org/index.php

- Age
- Heart failure
- Admitted to hospital
- Antipsychotics
- Any cancer
- Oral contraceptive
- Chronic obstructibe airway disease
- Crohn's
- Chronic kidney disease
- Tamoxifen
- Varicose vein surgery
- BMI
- Smoking
- Townsend deprivation score

### Fracture

Source: https://qfracture.org/index.php

- Age
- Alcohol
- Antidepressant
- Any cancer
- Asthma or chronic obstructive airway disease
- Steroids
- Cardiovascular disease
- Dementia
- Endocrine problems
- Epilepsy or anticonvulsants
- History of falls
- Liver disease
- Malabsorption
- Parkinson's
- Rheumatoid arthritis or SLE
- Chronic kidney disease
- Diabetes
- BMI
- Ethnicity
- Familiy history of osteoposrosis
- Smoking

### Breast Cancer

Source: https://www.canrisk.org/

- Pedigree data: Age, year of birth, age at disagnosis of several kinds of cancer (breast cancer, contralateral BC, ovarian cancer, prostate cancer, pancreatic cancer), genetic test results. Pedigree data needed for the target and their parents.
- Menarche
- Number of children
- Age at first child
- Menopause age
- Height
- Oral contraceptive use
- Height
- Weight
- BMI
- Alcohol consumption




