# from pprint import pprint
import csv
import re
from copy import deepcopy


class Contact:
    def __init__(self, lastname, firstname, surname, organization, position, phone, email):
        self.lastname = lastname
        self.firstname = firstname
        self.surname = surname
        self.organization = organization
        self.position = position
        self.phone = phone
        self.email = email

    def __eq__(self, other):
        if self.lastname == other.lastname and self.firstname == other.firstname:
            for atr in self.__dict__:
                # print(atr)
                self.__dict__[atr] = self.__dict__[atr] if self.__dict__[atr] != '' else other.__dict__[atr]
                other.__dict__[atr] = self.__dict__[atr]
            del other
            return True
        else:
            return False

    def __str__(self):
        return str(list(self.__dict__.values()))

    def __repr__(self):
        return f'{self.lastname} {self.firstname} {self.surname}'
        # return [self.lastname, self.firstname, self.surname, self.organization, self.position, self.phone, self.email]


def get_contacts(file, key_open, encoding, delimiter):
    with open(file, key_open, encoding=encoding) as f:
        rows = csv.reader(f, delimiter=delimiter)
        contacts_list = list(rows)
        # pprint(contacts_list)
        return contacts_list


def moving_LFS(contacts_list):
    lfs_contacts = contacts_list[::]
    for index, contact in enumerate(lfs_contacts[1:]):
        last = contact[0].split(' ')
        first = contact[1].split(' ')
        sur = contact[2].split(' ')
        lfs = []
        [lfs.extend(x) for x in [last, first, sur]]
        for i in range(3):
            lfs_contacts[1 + index][i] = lfs[:3][i]
        # print(lfs_contacts[1 + index])
    return lfs_contacts[1:]


def create_table(contacts_list, class_name):
    contacts = []
    for user in contacts_list:
        atr = user[:7]
        contacts.append(class_name(*atr))
    return contacts


def format_phone_number(lst, index=5):
    lst_formatted = deepcopy(lst)
    pattern = r'(8|\+7)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*)(\(?(доб.)?\s*(\d*)\)?)?'
    repl = r'+7(\2)\3-\4-\5\6\8\9'
    for contact in lst_formatted:
        contact[index] = re.sub(pattern=pattern, repl=repl, string=contact[index])
    return lst_formatted


def unite_duplicate(contacts):
    index = 0
    while index < len(contacts):
        if contacts[index] in contacts[index + 1:]:
            del contacts[index]
        else:
            index += 1
    return contacts


def convert_to_table(list_instances):
    table = []
    for instance in list_instances:
        record = [atr for atr in instance.__dict__.values()]
        table.append(record)
    return table


if __name__ == '__main__':
    contacts_list = get_contacts(file="phonebook_raw.csv", key_open='rt', encoding='utf-8', delimiter=",")
    headers = contacts_list[0]
    lfs_contacts = moving_LFS(contacts_list=contacts_list)
    contacts_formatted = format_phone_number(lfs_contacts)
    contacts = create_table(contacts_list=contacts_formatted, class_name=Contact)
    united_contacts = unite_duplicate(contacts=contacts)
    table = convert_to_table(list_instances=united_contacts)
    table.insert(0, headers)
    # print(table)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(table)
