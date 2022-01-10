from cohortextractor import (codelist_from_csv, combine_codelists)

## #####################
## Cohort definition
## #####################

# Patients undergoing cancer-related surgery.
codelist_cancer_surgery = codelist_from_csv(
    "codelists/codelist-cancer-surgery.csv",
    system="snomed",
    column="code",
)

## #####################
## Exposure
## #####################
# No codelits needed.


## #####################
## Outcomes
## #####################
## ## Outcomes used in the original COVIDSurg study.

## Post-operative mortality.
# No codelists needed.

## 30-day post-operative pulmonary complications.
# Defined by the presence of any codes for pneumonia,
# acute respiratory distress syndrome, or unexpected
# post-operative ventilation.

# Pneumonia.
codelist_pneumonia = codelist_from_csv(
    "codelists/codelist-pneumonia.csv",
    system="snomed",
    column="code",
)
# Acute respiratory distress syndrome, ARDS.
codelist_ARDS = codelist_from_csv(
    "codelists/codelist-ARDS.csv",
    system="snomed",
    column="code",
)
# Unexpected post-operative ventilation.
codelist_unexpected_ventilation = codelist_from_csv(
    "codelists/codelist-unexpected-ventilation.csv",
    system="snomed",
    column="code",
)
# Post-operative pulmonary complications.
codelist_pulmonary_complications = combine_codelists(
    codelist_pneumonia,
    codelist_ARDS,
    codelist_unexpected_ventilation,
)

## ## Outcomes in addition to those used in the original
## ## COVIDSurg study.

## 30-day post-operative cardiac complications.
# Defined by...

# Post-operative *<indicator of post-operative cardiac complications>.
codelist_* = codelist_from_csv(
    "codelists/codelist-*.csv",
    system="snomed",
    column="code",
)
# Post-operative **<indicator of post-operative cardiac complications>.
codelist_** = codelist_from_csv(
    "codelists/codelist-**.csv",
    system="snomed",
    column="code",
)
# Post-operative cardiac complications.
codelist_cardiac_complications = combine_codelists(
    codelist_*,
    codelist_**,
)

## 30-day post-operative cerebrovascular complications.
# Defined by...

# Post-operative *<indicator of post-operative cerebrovascular complications>.
codelist_* = codelist_from_csv(
    "codelists/codelist-*.csv",
    system="snomed",
    column="code",
)
# Post-operative **<indicator of post-operative cardcerebrovascular iac complications>.
codelist_** = codelist_from_csv(
    "codelists/codelist-*.csv",
    system="snomed",
    column="code",
)
# Post-operative cerebrovascular complications.
codelist_cerebrovascular_complications = combine_codelists(
    codelist_*,
    codelist_**,
)


## #####################
## Covariates
## #####################
## ## Outcomes used in the original COVIDSurg study.
## Revised Cardiac Risk Index
# Defined by the sum of 1/0 indications of:
# - Current surgeryis intraperitoneal or intrathoracic;
# - History of ischemic heart disease;
# - History of congestive heart failure;
# - History of cerebrovascular disease;
# - History of diabetes mellitus treated with insulin;
# - History of chronic kidney disease (creatinine > 176 μmol.l-1).

# Intraperioneal surgery.
codelist_intraperioneal_surgery = codelist_from_csv(
    "codelists/codelist-intraperioneal-surgery.csv",
    system="snomed",
    column="code",
)
# Intrathoracic surgery.
codelist_intrathoracic_surgery = codelist_from_csv(
    "codelists/codelist-intrathoracic-surgery.csv",
    system="snomed",
    column="code",
)
# Intraperioneal or intrathoracic surgery.
codelist_intraperioneal_or_intrathoracic_surgery = codelist_combine(
    codelist_intraperioneal_surgery,
    codelist_intrathoracic_surgery,
)
# Ischedmic heart disease.
codelist_ischedmic_heart_disease = codelist_from_csv(
    "codelists/codelist-ischedmic-heart-disease.csv",
    system="snomed",
    column="code",
)
# Congestive heart failure.
codelist_congestive_heart_failure = codelist_from_csv(
    "codelists/codelist-congestive-heart-failure.csv",
    system="snomed",
    column="code",
)
# Cerebrovascular disease.
codelist_cerebrovascular_disease = codelist_from_csv(
    "codelists/codelist-cerebrovascular-disease.csv",
    system="snomed",
    column="code",
)
# Diabetes mellitus treated with insulin.
codelist_diabetes_mellitus_treated_with_insulin = codelist_from_csv(
    "codelists/codelist-diabetes-mellitus-treated-with-insulin.csv",
    system="snomed",
    column="code",
)
# Chronic kidney disease, CKD.
codelist_chronic_kidney_disease = codelist_from_csv(
    "codelists/codelist-chronic-kidney-disease.csv",
    system="snomed",
    column="code",
)

## Presence of respiratory comorbidities.
# Asthma.
codelist_asthma = codelist_from_csv(
  "codelists/opensafely-asthma-diagnosis-snomed.csv"
  system="snomed",
  colum="code",
)
# COPD.
codelist_COPD = codelist_from_csv(
  "codelists/opensafely-chronic-obstructive-pulmonary-disease-copd-review-qof.csv",
  system="snomed",
  colum="code",
)
# Presence of respiratory comorbidities.
codelist_respiratory_comorbidities = combine_codelists(
    codelist_asthma,
    codelist_COPD,
)

## BUPA grade of surgery.
# Minor codes.
codelist_BUPA_grade_of_surgery_minor = codelist_from_csv(
   "codelists/codelist-BUPA-grade-of-surgery-minor.csv",
    system = "snomed",
    column = "code",
)
# Major codes.
codelist_BUPA_grade_of_surgery_major = codelist_from_csv(
   "codelists/codelist-BUPA-grade-of-surgery-major.csv",
    system = "snomed",
    column = "code",
)
