import os
import sys
import re



def find_emails(input_file, output_file):

    pattern = re.compile(r'([\w\.%+-]+)\s*[\[\(/]*\s*(?:@+|at)\s*[\]\)/]*\s*'
                          '([\w\.-]+)\s*[\[\(/]*\s*(?:\.+|dot)\s*[\]\)/]*\s*([\w]{2,6})')

    emails_list = []
    with open(input_file) as file:
        for page in file.readlines():
            print("Line : {}".format(page))
            email = pattern.search(page)
            if email is None:
                result = "None"
            else:
                result = email.group()
                result = pattern.sub(r'\1@\2.\3', result)

            print(result)
            emails_list.append(result)

    with open(output_file, 'w') as file:
        file.write('\n'.join(emails_list))


if __name__ == '__main__':
    path = "webpages.txt"
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    find_emails(input_file, output_file)
