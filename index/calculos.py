import math
import gspread
from google.oauth2.service_account import Credentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('software-414219-b50eeaecc512.json', scopes=scope)


client = gspread.authorize(creds)

sheet = client.open('Notas finais').sheet1

def absenceFailure(absence, totalClasses):
    if absence > 0.25 * totalClasses:
        return True
    else:
        return False

def calculateAverage(grade1, grade2, grade3): 
    average = (grade1 + grade2 + grade3) / 3
    return average

def calculateNAF(average):
    return math.ceil(2 * 50 - average)

values = sheet.get_all_values()


for i, student in enumerate(values[3:], start=4):
    student_name = student[1]
    absence = int(student[2])
    total_classes = 60
    grade1 = float(student[3])
    grade2 = float(student[4])
    grade3 = float(student[5])

    print(f"Processing student: {student_name}")

    if absenceFailure(absence, total_classes):
        print(f"Student {student_name} failed due to absence")
        sheet.update_cell(i, 7, "Reprovado por Falta")
        sheet.update_cell(i, 8, "0")
    else:
        average = calculateAverage(grade1, grade2, grade3)
        print(f"Average for student {student_name}: {average}")

        if average < 50:
            print(f"Student {student_name} failed due to low grades")
            sheet.update_cell(i, 7, "Reprovado por Nota")
            sheet.update_cell(i, 8, "0")

        elif 50 <= average < 70:
            print(f"Student {student_name} needs final exam")
            sheet.update_cell(i, 7, "Exame Final")
            naf = calculateNAF(average)
            print(f"Required score for passing final exam: {naf}")
            sheet.update_cell(i, 8, str(naf))
        else:
            print(f"Student {student_name} passed")
            sheet.update_cell(i, 7, "Aprovado")
            sheet.update_cell(i, 8, "0")

    print("\n")

print("Process completed.")

