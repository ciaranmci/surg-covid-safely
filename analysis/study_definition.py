#########################
## Imports.
#########################
# Obligatory OpenSAFELY import.
from cohortextractor import (
	StudyDefinition,
)
# Import codelists.py script.
from codelists import *
# Import study_parameters.
import study_parameters
# # Define variables explicitly from study_parameters
start_date = study_parameters["start_date"]
end_date = study_parameters["end_date"]


#########################
## Study definition.
#########################
study = StudyDefinition(
	default_expectations = {
		"date": {"earliest": start_date, "latest": end_date},
		"rate": "uniform",
		"incidence": 0.5,
	},

	population = patients.with_these_clinical_events(
		codelist_cancer_surgery,
		on_or_after = start_date
	),

	#############################################
	## Variables for calculating exposure.
	#############################################
	
	## Date of testing.
	# ...

	## Date of surgery.
	date_surgery = patients.admitted_to_hospital(
		with_these_procedures = codelist_cancer_surgery,
		returning = 'date',
		return_number_of_matches_in_period = True,
		include_date_of_match = True,
		date_format = "YYYY-MM-DD",
		return_expectations={
			"date": {"earliest"; start_date, "latest": "today"},
			"rate": "uniform",
			"incidence": 0.5}
	),


	#############################################
	## Variables for calculating outcomes.
	#############################################
	
	## Date of death.
	# Date of death from GP data.
	date_death_gp = patients.with_death_recorded_in_primary_care(
		on_or_after = start_date,
		returning = "date_of_death",
		return_expectations = {
			"date": {"earliest" : start_date},
			"rate": "exponential_increase"
		},
	),
	# Date of death from ONS data.
	date_death_ons = patients.died_from_any_cause(
		on_or_after = start_date,
		returning = "date_of_death",
		date_format = "YYYY-MM-DD",
		return_expectations = {
			"date": {"earliest" : start_date},
			"rate": "exponential_increase"
		},
	),
	# Date of death from CPNS data.
	date_death_cpns = patients.with_death_recorded_in_cpns(
		on_or_after = start_date,
		returning = "date_of_death",
		date_format = "YYYY-MM-DD",
		return_expectations = {
			"date": {"earliest" : start_date},
			"rate": "exponential_increase"
		},
	),

	## Date of post-operative pulmonary complications.
	date_postOp_pulmonary_complications = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_pulmonary_complications,
		on_or_after = date_surgery,
		returning = 'date',
		return_number_of_matches_in_period = True,
		include_date_of_match = True,
		date_format = ""YYYY-MM-DD"",
		return_expectations={
			""date"": {""earliest"": date_surgery, ""latest"": ""today""},
			""rate"": ""uniform"",
			""incidence"": 0.3}
	),

	## Date of post-operative cardiac complications.
	date_postOp_cardiac_complications = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_cardiac_complications,
		on_or_after = date_surgery,
		returning = 'date',
		return_number_of_matches_in_period = True,
		include_date_of_match = True,
		date_format = ""YYYY-MM-DD"",
		return_expectations={
			""date"": {""earliest"": date_surgery, ""latest"": ""today""},
			""rate"": ""uniform"",
			""incidence"": 0.3}
	),

	## Date of post-operative cerebrovascular complications.
	date_postOp_cerebrovascular_complications = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_cerebrovascular_complications,
		on_or_after = date_surgery,
		returning = 'date',
		return_number_of_matches_in_period = True,
		include_date_of_match = True,
		date_format = ""YYYY-MM-DD"",
		return_expectations={
			""date"": {""earliest"": date_surgery, ""latest"": ""today""},
			""rate"": ""uniform"",
			""incidence"": 0.3}
	),

	## Variables to calculate 'lenth of stay'.
	# Date of admission.
	date_hospital_admission = patients.admitted_to_hospital(
		returning = ""date_admitted"",
		on_or_before = date_surgery,
		find_first_match_in_period = True,
		with_these_procedures = codelist_cancer_surgery,
		date_format = ""YYYY-MM-DD"",
		return_expectations = {
			""date"": {""earliest"": <study_start_date>, ""latest"": ""today""}
		}
	),
	# Date of post-operative discharge.
	date_postOp_discharge = patients.admitted_to_hospital(
		returning = ""date_discharged"",
		on_or_after = date_surgery,
		find_first_match_in_period = True,
		with_these_procedures = codelist_cancer_surgery,
 		date_format = ""YYYY-MM-DD"",
		return_expectations = {
			""date"": {""earliest"": date_surgery, ""latest"": ""today""}
		}
	),

	## Variables to calculate 'discharge to a destination difference
	## from the pre-operative residence'.
	# Source of admission.
	source_of_admission = patients.admitted_to_hospital(
		returning = ""source_of_admission"",
		on_or_after = <study_start_date>,
		find_first_match_in_period = True,
		with_these_procedures = codelist_cancer_surgery,
		return_expectations = {
			# I don't know what the permitted values are, so 
			# I can't suggest proportions of categories.
			}
		}
	),
	# Discharge destination.
	discharge_destination = patients.admitted_to_hospital(
		returning = ""discharge_destination"",
		on_or_after = date_surgery,
		find_first_match_in_period = True,
		with_these_procedures = codelist_cancer_surgery,|
		return_expectations = {
			# I don't know what the permitted values are, so 
			# I can't suggest proportions of categories.
			}
		}
	),

	## Post-operative emergency attendance.
	date_postOp_emergency_dept_attendance = patients.attended_emergency_care(
		on_or_after = date_surgery,
		returning = ""date_arrived"",
		date_format = ""YYYY-MM-DD"",
		return_expectations = {
			""date"": {""earliest"": date_surgery, ""latest"": ""today""},
			""rate"": ""uniform""
		}
	),

	#############################################
	## Variables for calculating confounders
	#############################################
	## Age
	# Age, in years.
	age_at_surgery = patients.age_as_of(
		date_surgery,
	        return_expectations = {
        	        "rate": "universal",
                	"int": {"distribution": "population_ages"}
		        }
	),
	# Age group, in accordance with the original COVIDSurg study.
	age_group_surgery = patients.categorised_as(
        	{
		"0-29": "age_at_surgery <= 29",
	        "30-49": "age_at_surgery > 29 AND age <= 49",
	        "50-69": "age_at_surgery > 49 AND age <= 69",
	        "70-79": "age_at_surgery > 69 AND age <= 79",
	        "80+": "age_at_surgery >= 80",
	        "Missing": "isintance(age_at_surgery, int)",
	        },
		return_expectations={
			"rate": "universal",
			"category": {
			"ratios": {
				"0-29": 0.229,
				"30-49": 0.275,
				"50-69": 0.304,
				"70-79": 0.128,
				"80+": 0.064 ,
				}
			},
		},
	),

	## Sex
	sex = sex(
		return_expectations = {
			"rate": "universal",
			"category": {"ratios": {"Female": 0.5, "Male": 0.50}}
			}
	),

	## Variables needed for Revised Cardiac Risk Index.
	# Intraperitoneal or intrathroacic surgery.
	intraperitoneal_or_intrathroacic_surgery_gpData = patients.with_these_clinical_events(
		codelist_intraperitoneal_or_intrathroacic_surgery,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	intraperitoneal_or_intrathroacic_surgery_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_intraperitoneal_or_intrathroacic_surgery,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	# History of ischemic heart disease.
	history_of_ischemic_heart_disease_gpData = patients.with_these_clinical_events(
		codelist_ischemic_heart_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
	 	}
	), 
	history_of_ischemic_heart_disease_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_ischemic_heart_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	# History of congestive heart failure.
	history_of_congestive_heart_failure_gpData = patients.with_these_clinical_events(
		codelist_congestive_heart_failure,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	history_of_congestive_heart_failure_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_congestive_heart_failure,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	# History of cerebrovascular disease.
	history_of_cerebrovascular_disease_hgpData = patients.with_these_clinical_events(
		codelist_cerebrovascular_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	history_of_cerebrovascular_disease_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_cerebrovascular_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
 			"incidence": 0.3
		}
	), 
	# History of diabetes mellitus treated with insulin.
	history_of_diabetes_mellitus_treated_with_insulin_gpData = patients.with_these_clinical_events(
		codelist_diabetes_mellitus_treated_with_insulin,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	history_of_diabetes_treated_with_insulin_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_diabetes_treated_with_insulin,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	# History of chronic kidney disease.
	history_of_chronic_kidney_disease_gpData = patients.with_these_clinical_events(
		codelist_chronic_kidney_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	history_of_chronic_kidney_disease_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_chronic_kidney_disease,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	# Calculate the Revised Cardiac Risk Index.
	revised_cardiac_risk_index = (intraperitoneal_or_intrathroacic_surgery_gpData or
					intraperitoneal_or_intrathroacic_surgery_hospitalData) +
					(history_of_ischemic_heart_disease_gpData or
					history_of_ischemic_heart_disease_hospitalData) +
					(history_of_congestive_heart_failure_gpData or
					history_of_congestive_heart_failure_hospitalData) +
					(history_of_cerebrovascular_disease_gpData or
					history_of_cerebrovascular_disease_hospitalData) +
					(history_of_diabetes_treated_with_insulin_gpData or
					history_of_diabetes_treated_with_insulin_hospitalData) +
					(history_of_chronic_kidney_disease_gpData or
					history_of_chronic_kidney_disease_hospitalData),
	# Calculate the categories for the Revised Cardiac Risk Index.
	category_revised_cardiac_risk_index = patients.categorised_as(
		{
		"0": "revised_cardiac_risk_index == 0"
		"1": "revised_cardiac_risk_index == 1"
		"2": "revised_cardiac_risk_index == 2"
		">=3": "revised_cardiac_risk_index > 2"
		},
		return_expectations = {
			"rate": "universal",
			"category": {
				"ratios": {
					"0": 0.25,
					"1": 0.25,
					"2": 0.25,
					">=3": 0.25
				}
			}
		}
	),

	## Presence of pre-operative respiratory comorbidities.
	# Asthma.
	diagnosis_of_asthma_gpData = patients.with_these_clinical_events(
		codelist_asthma,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations = {
			"incidence": 0.3
		}
	),
	diagnosis_of_asthma_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_asthma,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	), 
	# COPD.
	diagnosis_of_COPD_gpData = patients.with_these_clinical_events(
		codelist_COPD,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	diagnosis_of_COPD_hospitalData = patients.admitted_to_hospital(
		with_these_diagnoses = codelist_COPD,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"incidence": 0.3
		}
	),
	# Compute the indicator for the presence of pre-operative
	# respiratory comorbidities.
	category_presence_of_respiratory_comorbidities = patients.categorised_as(
		{
		"Yes": "diagnosis_of_asthma_gpData == 1 or diagnosis_of_asthma_hospitalData == 1 or
			diagnosis_of_COPD_gpData == 1 or diagnosis_of_COPD_hospitalData == 1"
		"No": "diagnosis_of_asthma_gpData == 1 and diagnosis_of_asthma_hospitalData == 1 and
			diagnosis_of_COPD_gpData == 1 and diagnosis_of_COPD_hospitalData == 1"
		},
		return_expectations = {
			"rate": "universal",
			"category": {
				"ratios": {
					"Yes": 0.5,
					"No": 0.5
					}
				}
			}
	),

	## Grade of surgery.
	# Grade of surgery, minor.
	BUPA_grade_of_surgery_minor = patients.with_these_clinical_events(
		codelist_BUPA_grade_of_surgery_minor,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"rate": "universal"
			}
	),
	# Grade of surgery, major.
	BUPA_grade_of_surgery_major = patients.with_these_clinical_events(
		codelist_BUPA_grade_of_surgery_major,
		on_or_before = date_surgery,
		returning = "binary_flag",
		return_expectations={
			"rate": "universal"
			}
	),

	## 'Urgency of surgery'.
	admission_urgency = patients.admitted_to_hospital(
		with_these_procedures = codelist_cancer_surgery,
		returning = ""admission_method"",
		on_or_after = start_date,
		find_first_match_in_period = True,
		return_expectations = {
 			# I don't know the admission codes so I've said 11, 12, 13.
			""category"": {""ratios"": {""11"": 0.3, ""12"": 0.3, ""13"": 0.4}}, 
			""incidence"": 1
		}
	),

	## Local COVID-specific index of multiple deprivation.
	address_deprivation_index = patients.address_as_of(
		date = date_surgery,
		returning = "index_of_multiple_deprivation",
		round_to_nearest = 100,
		return_expectations = {
			“rate”: “universal”,
			“category”: {“ratios”: {“100”: 0.1, “200”: 0.2, “300”: 0.7}}
			}
	),

	## Perioperative practices.
	# ...
	
	## Cancer type.
	# ...

	## Cancer stage.
	# ...

	## Surgical Approach.
	# Open surgery.
	# ...
	# Laproscopic surgery.
	# ...
	# Conversion surgery.
	# ...

	## Regional SARS-CoV-2 prevalence.
	# ...
	
	## Local perioperative resource.
	# ...

	## Local COVID-non-specific perioperative practices.
	# ...

	## Local practices for scheduling surgeries.
	# ...

	## Regional testing practices.
	# ...

	## Month of patients' surgery.
	# ...

	## Year of patients' surgery.
	# ...




) # End of StudyDefinition().
