from mainapp.models import Victim
import csv

with open("victims.csv") as f:
    reader = csv.reader(f)
    row_num = 1
    for row in reader:
        if row_num == 1:
            row_num += 1
            continue

        ob, created = Victim.objects.get_or_create(
                row = row_num,
                timestamp = str(row[0]),
                name = str(row[1]),
                contact = str(row[2]),
                coordinates = str(row[3]),
                status = str(row[4]),
                location = str(row[5]),
                no_of_people = str(row[6]),
                degree_of_emergency = str(row[7]),
                district = str(row[8]),
                help_required_immediatly = str(row[9]),
                done = str(row[11]))
        row_num += 1

