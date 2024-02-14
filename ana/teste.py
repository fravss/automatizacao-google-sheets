import math
import gspread
from google.oauth2.service_account import Credentials

# Scope and credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('software-414219-b50eeaecc512.json', scopes=scope)

# Authenticate the client
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open('Engenharia de Software - Desafio Ana Flávia').sheet1

def absenceFailure(absence, totalClasses):
    # Function to check if student failed due to excessive absence
    if absence > 0.25 * totalClasses:
        return True
    else:
        return False

def calculateAverage(grade1, grade2, grade3): 
    # Function to calculate the average grade of a student
    average = (grade1 + grade2 + grade3) / 3
    return average

def calculateNAF(average):
    # Function to calculate the score needed for passing the final exam
    return math.ceil(2 * 50 - average) # rounding up to the nearest 

values = sheet.get_all_values()  # Get all values from the spreadsheet

# Loop through each student's data
for i, student in enumerate(values[3:], start=4):
    student_name = student[1]
    absence = int(student[2])
    total_classes = 60
    grade1 = float(student[3])
    grade2 = float(student[4])
    grade3 = float(student[5])

    print(f"Processing student: {student_name}")

    if absenceFailure(absence, total_classes):
        # If student failed due to absence, update the spreadsheet accordingly
        print(f"Student {student_name} failed due to absence")
        sheet.update_cell(i, 7, "Reprovado por Falta")
        sheet.update_cell(i, 8, "0")
    else:
        # Calculate the average grade for the student
        average = calculateAverage(grade1, grade2, grade3)
        print(f"Average for student {student_name}: {average}")

        if average < 50:
            # If student failed due to low grades, update the spreadsheet accordingly
            print(f"Student {student_name} failed due to low grades")
            sheet.update_cell(i, 7, "Reprovado por Nota")
            sheet.update_cell(i, 8, "0")
        elif 50 <= average < 70:
            # If student needs a final exam, calculate the required score and update the spreadsheet
            print(f"Student {student_name} needs final exam")
            sheet.update_cell(i, 7, "Exame Final")
            naf = calculateNAF(average)
            print(f"Required score for passing final exam: {naf}")
            sheet.update_cell(i, 8, str(naf))
        else:
            # If student passed, update the spreadsheet accordingly
            print(f"Student {student_name} passed")
            sheet.update_cell(i, 7, "Aprovado")
            sheet.update_cell(i, 8, "0")

    print("\n")

print("Process completed.")

