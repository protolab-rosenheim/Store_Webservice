import csv
import requests

from Webservice.DbModels import Board

with open('Demodata.csv') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        if reader.line_num == 1:
            continue  # This row contains field names -> do nothing
        else:
            board = Board(Identnummer=row[0], Material=row[1], Dekor=row[2], Laenge=row[3], Breite=row[4], Dicke=row[5],
                          Maserung=row[6], OptiMatParam=row[7], OptiBoardParam=row[8], OptiFunctionCode=row[9],
                          Kosten=row[10], BestandPhys=row[11], Geplant=row[12], Barcode=row[13], MaxPaketHoehe=row[14],
                          MinBestand=row[15])
            requests.post(url='http://127.0.0.1:5000/api/board', json=board.to_dict(),
                          headers={'Content-Type': 'application/json'})
