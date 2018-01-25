import getopt
import os
import re
import sys


def get_student_and_date(logs):
    data = []
    for log in logs:
        temp = (log[0][0][:-11].replace(" ", ""), log[0][2])
        data.append(temp)
    return list(set(data))


def get_students_with_id(students):
    id = 1
    students_with_id = []
    sorted_students = sorted(students)
    for s in sorted_students:
        temp = (id, s)
        students_with_id.append(temp)
        id += 1
    return students_with_id


def write_sql_scripts_for_inserting_files_and_ftplog(logs, students):
    print("Generating SQL script for inserting files and ftpLog data...")
    file_id = 1
    ftp_log_id = 1
    file_table_data = []
    ftp_log_table_data = []
    local_students = get_students_with_id(students)
    tempdata = get_student_and_date(logs)
    for td in tempdata:
        for log in logs:
            if(td[0] == log[0][0][:-11].replace(" ", "") and td[1] == log[0][2]):
                for ls in local_students:
                    if(ls[1] == log[0][2]):
                        tmp_file_data = (file_id, log[0][3], td[0], log[0][1])
                        tmp_ftp_log_data = (ftp_log_id, ls[0], file_id)
                        ftp_log_id += 1
                        file_id += 1
                        file_table_data.append(tmp_file_data)
                        ftp_log_table_data.append(tmp_ftp_log_data)
                break
    file = open('filesInsertScript.sql', 'w')
    file.write('INSERT INTO file(ID, FileName, Date, IP) VALUES\n')
    for index in range(0, len(file_table_data) - 1):
        file.write('(' + str(file_table_data[index][0]) + ", '" + file_table_data[index][1] + "', '" + file_table_data[index][2]  + "', '" + file_table_data[index][3] + "'),\n")
    file.write('(' + str(file_table_data[len(file_table_data) - 1][0]) + ", '" + file_table_data[len(file_table_data) - 1][1] + "', '" + file_table_data[len(file_table_data) - 1][2]  + "', '" + file_table_data[len(file_table_data) - 1][3] + "');")
    file.close()
    file = open('ftpLogInsertScript.sql', 'w')
    file.write('INSERT INTO ftplog(ID, StudentID, FileID) VALUES\n')
    for index in range(0, len(ftp_log_table_data) - 1):
        file.write('(' + str(ftp_log_table_data[index][0]) + ", " + str(ftp_log_table_data[index][1]) + ", " + str(ftp_log_table_data[index][2]) + "),\n")
    file.write('(' + str(ftp_log_table_data[len(ftp_log_table_data) - 1][0]) + ", " + str(ftp_log_table_data[len(ftp_log_table_data) - 1][1]) + ", " + str(ftp_log_table_data[len(ftp_log_table_data) - 1][2]) + ");")
    file.close()
    print("SQL script for inserting files and ftpLog data has been generated!\n")


def write_sql_script_for_inserting_students(students):
    print("\nGenerating SQL script for inserting students data...")
    sorted_students = get_students_with_id(students)
    file = open('studentsInsertScript.sql', 'w')
    file.write('INSERT INTO student(ID, Name) VALUES\n')
    for index in range(0, len(sorted_students) - 1):
        file.write('(' + str(sorted_students[index][0]) + ", '" + sorted_students[index][1] + "'),\n")
    file.write('(' + str(sorted_students[len(sorted_students) - 1][0]) + ", '" + sorted_students[len(sorted_students) - 1][1] + "');\n")
    file.close()
    print("SQL script for inserting students data has been generated!\n")


def get_students(logs):
    students = []
    print("Getting students list from logs")
    for log in logs:
        if not(log[0][2] in students):
            students.append(log[0][2])
    return students


def parse_logs(argv):
    data = []
    print("Started parsing logs...")
    for filename in os.listdir(argv):
        with open(argv + filename) as f:
            for line in f:
                found = re.findall('.+\)\s(.+)\s-.+\(([0-9\.]+).+150.+upload.+\/Pbd\/Stud\/[^\/.]+\/([^\/.]+)\/(.+)\"', line)
                if (found):
                    data.append(found)
    return data


def write_sql_create_tables_script():
    file = open('createTables.sql', 'w')
    file.write('create table student')
    file.write('(ID INTEGER NOT NULL,\n    Name VARCHAR(50) NOT NULL,\n    PRIMARY KEY(ID));\n\n')
    file.write('create table file (ID INTEGER NOT NULL,\n    FileName VARCHAR(255) NOT NULL,\n')
    file.write('    Date VARCHAR(25) NOT NULL,\n    IP VARCHAR(20) NOT NULL,\n    PRIMARY KEY(ID));\n\n')
    file.write('create table ftplog (ID INTEGER NOT NULL,\n')
    file.write('    StudentID INTEGER NOT NULL,\n    FileID INTEGER NOT NULL,\n    PRIMARY KEY(ID),\n')
    file.write('    FOREIGN KEY (StudentID) REFERENCES student(ID),\n    FOREIGN KEY (FileID) REFERENCES file(ID));')
    file.close()


def main(argv):
    data = []
    students = []
    inputfolder = ''
    if len(sys.argv) < 2:
        print('USAGE: pytest.py -i <inputFolder>')
    try:
        opts, args = getopt.getopt(argv, "hi:", ["iFolder="])
    except getopt.GetoptError:
        print('USAGE: pytest.py -i <inputFolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('pytest.py -i <inputFolder>')
            sys.exit()
        elif opt in ("-i", "--iFolder"):
            inputfolder = arg
            print('Input folder is: ' + inputfolder)
            data = parse_logs(inputfolder)
            if(len(data) == 0):
                print('WARNING: No data found! Provide folder with corresponding logs!')
                sys.exit()
            else:
                print("Logs parsed! Data Found!")
                students = get_students(data)
                write_sql_script_for_inserting_students(students)
                write_sql_scripts_for_inserting_files_and_ftplog(data, students)
                write_sql_create_tables_script()
                print('Program terminated successfully!')
        else:
            print('USAGE: pytest.py -i <inputFolder>')
if __name__ == '__main__':
    main(sys.argv[1:])
