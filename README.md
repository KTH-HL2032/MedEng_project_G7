# MedEng_project_G7
This project is a result of the project course in medical engineering at KTH

You need to install all the packages from the requirements.txt as well as the ones in the dependencies folder. This can be done manually or with the bash or batch skrips install_packages_... A venv is recommended. If this is a new concept to you watch the video by corey shaefer for [unix][1] or [windows][2] respectively.

Installation process for unix:
1) clone repository to a local path
2) create a venv if desired (recommended)
3) make the install_packages_unix.sh executable: `chmod +x install_packages.sh`
4) run the bash skript with: `sh install_packages_unix.sh`

Installation process for windows:
1) clone repository to a local path
2) create a venv if desired (recommended)
3) install all the packages from the requirements.txt `pip install -r requirements.txt`
4) install the niryo one package as follows `pip install -e ./dependencies/niryo_one_tcp_client_package`

## Niryo One
The Niryo One Robot can be operated via different communication channels.
The easiest way to get stared is to [download][3] the desktop application.
Here you can connect to the robot and get a qucik overview of the features.

To communicate with the robot a more sophisticated method is needed. The 

[1]:	https://youtu.be/Kg1Yvry_Ydk
[2]:	https://youtu.be/APOPm01BVrk
[3]:	https://niryo.com/download/
