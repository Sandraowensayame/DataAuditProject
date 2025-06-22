import pandas as pd

# ==================================================
# STEP 1: READ ALL THREE FILES
# ==================================================
patients = pd.read_csv("PATIENTS.csv")
admissions = pd.read_csv("ADMISSIONS.csv")
diagnoses = pd.read_csv("DIAGNOSES_ICD.csv")

# ==================================================
# STEP 2: LINK DIAGNOSES WITH ADMISSIONS
# ==================================================
diag_adm = diagnoses.merge(admissions, on=["hadm_id", "subject_id"], how="left")

# ==================================================
# STEP 3: LINK WITH PATIENTS
# ==================================================
full_data = diag_adm.merge(patients, on="subject_id", how="left")

# ==================================================
# STEP 4: FLAG ERRORS
# ==================================================
valid_codes = ["99591", "99662", "5672", "40391", "42731"]
full_data["audit_error"] = full_data["icd9_code"].apply(lambda x: 0 if str(x) in valid_codes else 1)

# ==================================================
# STEP 5: EXPORT RESULT
# ==================================================
results_file = "linked_results.csv"
full_data.to_csv(results_file, index=False)

# ==================================================
# STEP 6: PRINT SUMMARY
# ==================================================
error_count = full_data["audit_error"].sum()
error_rate = error_count / len(full_data) * 100
print(f"✅ Exported results to {results_file}")
print(f"✅ TOTAL Records: {len(full_data)} | Errors: {error_count} | Error Rate: {error_rate:.2f}%")
