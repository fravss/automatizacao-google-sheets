import gspread
from google.oauth2.service_account import Credentials

# Defina o escopo e as credenciais
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('software-414219-b50eeaecc512.json', scopes=scope)

# Autentique o cliente
client = gspread.authorize(creds)

# Abra a planilha (substitua 'Nome da Planilha' pelo nome da sua planilha)
sheet = client.open('Engenharia de Software - Desafio Ana Flávia').sheet1

# Leia os dados
# Ler todos os valores da planilha
values = sheet.cell(3, 2).value
print(values)




