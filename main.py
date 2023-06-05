import re
import csv

def csv_read():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def fix_name(row):
    full_name = ' '.join([row[0], row[1], row[2]]).strip()
    correct_name_list = re.sub(r'[ ,]|$', ',', full_name, count=2).split(',')
    row[0], row[1], row[2] = correct_name_list[0], correct_name_list[1], correct_name_list[2]

def fix_tp(row):
    row[5] = re.sub(r'(\+7|8) ?\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{2})[- ]?(\d{2})', r'+7(\g<2>)\g<3>-\g<4>-\g<5>)',
                    row[5])
    row[5] = re.sub(r'\(?доб. ?(\d{4})\)?', r'доб.\g<1>', row[5])

def union_rows(row, old_row):
    ROW_LENGHT = 7
    result_row = []
    for i in range(ROW_LENGHT):
        if row[i] != old_row[i]:
            result_row.append(row[i] + old_row[i])
        else:
            result_row.append(row[i])
    return result_row

def fix_contacts(contact_list):
    existing_contacts = {}
    result_list = []
    for id,row in enumerate(contact_list):
        fix_name(row)
        fix_tp(row)
        if row[0] in existing_contacts:
            result_list[existing_contacts[row[0]]] = union_rows(row, result_list[existing_contacts[row[0]]])
        else:
            existing_contacts.update({row[0]: len(result_list)})
            result_list.append(row)
    return result_list

def csv_write(list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list)

if __name__ == '__main__':
    contacts = csv_read()
    fixed_contacts = fix_contacts(contacts)
    csv_write(fixed_contacts)