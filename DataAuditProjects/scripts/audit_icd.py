import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# ==================================================
# STEP 1: READ THE DIAGNOSES_ICD FILE
# ==================================================
diagnoses = pd.read_csv("DIAGNOSES_ICD.csv")  # This must match your filename

# ==================================================
# STEP 2: DEFINE VALID ICD-9 CODES
# ==================================================
valid_codes = ["99591", "99662", "5672", "40391", "42731"]

# ==================================================
# STEP 3: FLAG ERRORS
# ==================================================
diagnoses["audit_error"] = diagnoses["icd9_code"].apply(lambda x: 0 if str(x) in valid_codes else 1)

# ==================================================
# STEP 4: CALCULATE STATS
# ==================================================
error_count = diagnoses["audit_error"].sum()
error_rate = error_count / len(diagnoses) * 100
total_records = len(diagnoses)

# ==================================================
# STEP 5: EXPORT RESULTS TO .csv
# ==================================================
results_file = "icd9_audit_results.csv"
diagnoses.to_csv(results_file, index=False)

# ==================================================
# STEP 6: PLOT RESULTS
# ==================================================
count_values = diagnoses["audit_error"].value_counts()
count_values.plot(kind='bar', color=['green','red'])
plt.xticks([0,1], ["Valid", "Error"])
plt.ylabel('Number of Records')
plt.title(f'ICD-9 Audit Results\nError Rate: {error_rate:.2f}%')
plot_file = 'icd9_audit.png'
plt.savefig(plot_file)

# ==================================================
# STEP 7: GENERATE PDF REPORT
# ==================================================
pdf_file = "icd9_audit_report.pdf"

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(0, 10, "ICD-9 Audit Report", ln=True, align='C')
pdf.cell(0, 10, f"Total Records: {total_records}", ln=True)
pdf.cell(0, 10, f"Error Count: {error_count}", ln=True)
pdf.cell(0, 10, f"Error Rate: {error_rate:.2f}%", ln=True)

pdf.image(plot_file, w=180)

pdf.output(pdf_file)

# ==================================================
# STEP 8: PRINT RESULTS TO TERMINAL
# ==================================================
print(f"✅ Exported results to: {results_file}")
print(f"✅ Created chart: {plot_file}")
print(f"✅ Created PDF report: {pdf_file}")

from fpdf import FPDF
import os

# Demo statistics (you'd use your actual data here!)
total_records = 1000
error_count = 45
error_rate = (error_count / total_records) * 100
plot_file = "icd9_audit.png"  # Replace with actual chart image path

class PDFWithHeaderFooter(FPDF):
    def header(self):
        # Logo / Branding area
        self.set_font("Arial", style='B', size=16)
        self.set_text_color(40, 40, 150)  # Dark Blue color
        self.cell(0, 10, "Sandra Owens Acheoja Ayame", align='C', ln=True)

        # Sub-title
        self.set_font("Arial", style='I', size=12)
        self.set_text_color(100, 100, 100)  # Grey
        self.cell(0, 10, "ICD-9 Audit Report", align='C', ln=True)

        # Space after the title
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("Arial", style='I', size=8)
        self.set_text_color(100, 100, 100)
        page_num = f"Page {self.page_no()}"
        self.cell(0, 10, page_num, align='C')


# Create the PDF
pdf = PDFWithHeaderFooter()
pdf.add_page()

# Main statistics
pdf.set_font("Arial", size=12)
pdf.set_text_color(0, 0, 0)  # Black text
pdf.cell(0, 10, f"Total Records: {total_records}", ln=True)
pdf.cell(0, 10, f"Error Count: {error_count}", ln=True)
pdf.cell(0, 10, f"Error Rate: {error_rate:.2f}%", ln=True)

# Adding the chart
if os.path.exists(plot_file):
    pdf.ln(5)
    pdf.image(plot_file, w=180)

# Export the final PDF
pdf.output("icd9_audit_report.pdf")

print("✅ Created professional PDF with title, page numbers, and chart.")
