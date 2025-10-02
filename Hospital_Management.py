import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#TO LOAD A CSV FILE
df = pd.read_csv(r"C:\Users\harsh\Desktop\Hospital_management\hospital_data.csv")

#FOR OVERVIEW
print(df.head(11)) #TO DISPLAY FIRST 10 RECORDS
print(df.tail(11)) #TO DISPLAY LAST 10 RECORDS

print(df.info())  #TO DISPLAY THE NAMES, DATATYPES, NULL VALUES OF THE COLUMNS

print("Missing Values:\n",df.isnull().sum()) #TO DISPLAY THE TOTAL OF NULL VALUES IN EACH COLUMN


#TO CONVERT THE DATATYPE ACCORDING TO THE DATA
df["Admission_Date"] = pd.to_datetime(df["Admission_Date"],errors = "coerce")
df["Discharge_Date"] = pd.to_datetime(df["Discharge_Date"],errors= "coerce")
print(df.info())


#DIFFERENT WAYS TO FILL THE NULL VALUES
df["Doctor_Name"] = df["Doctor_Name"].fillna(method = "ffill")
df["Payment_Method"] = df["Payment_Method"].fillna(method="ffill")
df["Bill_Amount"] = df["Bill_Amount"].fillna(df["Bill_Amount"].median())
df["City"] = df["City"].fillna("Unknown")
df["Admission_Date"] = df["Admission_Date"].fillna(method = "ffill")
print(df.head(20))

#TO REMOVE THE ROW WHERE THE VALUE IN NAN
# df = df.dropna(subset=['City'])
print(df.head(21))
print(df.isnull().sum())


#TO DROP DUPLICATES ENTRIES

df = df.drop_duplicates(subset =['Patient_ID'])
print(print(df[['Patient_ID','Patient_Name', 'Admission_Date', 'Discharge_Date']].head(21)))

print(df.isnull().sum())

#TO CREATE NEW USEFUL CLOLUMNS
df["Length_Of_Stay"] = (df["Admission_Date"] - df["Discharge_Date"]).dt.days

#TO EXTRACT YEAR AND MONTH
df["Year"] = df["Admission_Date"].dt.year
df["Month"] = df["Discharge_Date"].dt.month
print(df[["Patient_ID","Department", "Patient_Name","Admission_Date","Discharge_Date","Length_Of_Stay"]].head(21))

#TO KNOW THE PERFORMANCE OF THE DEPARTMENT LIKE REVENUE AND PATIENT
Dept_Perfm = df.groupby("Department").agg(
    Total_Revenue = ("Bill_Amount","sum"),
    Total_Patients = ("Patient_ID","nunique")
).reset_index()

#TO DISPLAY THE DEPARTMENTS ACCORDING TO THEIR TOTAL REVENUE
Dept_Perfm = Dept_Perfm.sort_values("Total_Revenue",ascending=False)
print("\n",Dept_Perfm)

#TO DISPLAY TOP 10 DOCTORS

Top_Doctors = (df.groupby(["Doctor_Name"])["Bill_Amount"]
               .sum()
               .reset_index()
               .sort_values("Bill_Amount",ascending=False)
               .head(11))
print("\n",Top_Doctors)

#TO KNOW THE TOTAL OF MONTHLY ADMISSIONS

Monthly_Admission = (df.set_index("Admission_Date")
                     .resample('M')["Patient_ID"]
                     .nunique()
                     .reset_index(name="Total_Patients")
                     )
print("\n",Monthly_Admission)

#AVERAGE LENGTH OF STAY
Avg_Stay = df.groupby("Department")["Length_Of_Stay"].agg(
             Avg_stay = 'mean',
             Total_stay = 'sum'
            )
print("\n",Avg_Stay)

#TO ANALYZE PAYMENT METHOD
Pay_Perfm = (df.groupby("Payment_Method")["Bill_Amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index(name="Collection")
)
print("\n",Pay_Perfm)

#TO ANALYZE WHICH PATIENT PAID THE MOST
Most_Paid_Patient = (df.groupby("Patient_Name")["Bill_Amount"]
                     .sum()
                     .sort_values(ascending=False)
                     .head(10)
                     .reset_index(name="Total Paid")
)
print("\n",Most_Paid_Patient)

Dept_Perfm.to_csv('Department_Performance.csv', index=False)
Top_Doctors.to_csv('Top_Doctors.csv', index=False)
Monthly_Admission.to_csv('Monthly_Admission.csv')
Avg_Stay.to_csv('Average_Stay.csv', index=False)
Pay_Perfm.to_csv('Payment_Performance.csv', index=False)
Most_Paid_Patient.to_csv('High_Revenue_Patients.csv', index=False)