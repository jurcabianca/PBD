*This is a school project*

Aproach:
	- I took from the logs messages like:
	>(000086) 1/9/2017 14:14:39 PM - student (192.168.113.65)> 150 Opening data channel for file upload to server of "/Pbd/Stud/Luni 08-10/Florea Caius/plSQL/Lab09/Lab09.sql"
	- The information my regular expression is using: 
		* Date: 1/9/2017 14:14:39 PM
		* IP: 192.168.113.65
		* FTP code: 150
		* FTP Message Info: upload
		* Path: Pbd
		* Path(student name): Florea Caius
		* File full path: /Pbd/Stud/Luni 08-10/Florea Caius/plSQL/Lab09/Lab09.sql
	- I considered the following aspects:
		* A student was attending the laboratory if in date XX/XX/XXXX he/she uploaded a file to Server location /Pbd/Stud/XXXX/Student Name/
		* Every student must have in path /Pbd/Stud/XXXXX/ a folder with his name. *ex: Pbd/Stud/XXXXX/JURCA BIANCA EVELINE/*
		* After each laboratory every student has to upload a file to location */Pbd/Stud/XXXXX/Student Name/*

To use this program you will need to install Python 2.7.xx.
**Usage:**
```
python sqlGenerator.py -i <inputFolder>
ex: python sqlGenerator.py -i /home/user/Documents/PBD/Project/Logs/
```
inputFolder - full path to folder where logs are located.

After executing the program, 4 .sql files are generated.
