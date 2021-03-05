from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import re
import csv


def getProfiles(htmlContent):
    listOfProfiles = []
    soup = BeautifulSoup(htmlContent,"html.parser")
    for data in soup.find_all("div",attrs = {'class':"profilemain"}):
        listOfProfiles.append(data.get_text().strip())
    return listOfProfiles

def getProfilesByBranches(lpyistOfProfiles):
    branches = defaultdict(list)
    for profile in listOfProfiles:
        profile =  profile.split("\n")
        profile =  [i for i in profile if i.strip() != ""]
        name,position = profile[0],profile[1]
        department =  profile[2].rstrip()[:-1]
        email = re.findall('\S+@\S+',profile[3])[0] if(len(re.findall('\S+@\S+',profile[3])) != 0) else "Not Available"
        tmp1 = profile[-4:-2]
        qualification,research_area  = "",""
        if("Qualification" in tmp1[0] and "Reseach" not in tmp1[1]):
            qualification = "["+tmp1[1].lstrip()+"]"
        else:
            qualification = "Not Available"
        research_area = "Not Available" if profile[-1] == "Reseach Area :" else "["+profile[-1]+"]"
      
        d = {"Name" : name,
             "Position" : position,
             "Department" : department,
             "Email-ID" : email,
             "Qualification" : qualification,
             "Research Area": research_area
            }
        if(department == 'Information Technology'): branches['Information Technology'].append(d)
        elif(department == 'Computer Science & Engineering'): branches['Computer Science & Engineering'].append(d)
        elif(department == 'Electrical and Electronics Engineering' ): branches['Electrical and Electronics Engineering'].append(d)
        elif(department == 'Civil Engineering'): branches['Civil Engineering'].append(d)
        elif(department == 'Mechanical Engineering'): branches['Mechanical Engineering'].append(d)
        elif(department == 'Shri Vaishnav Institute of Textile Technology'): branches['Shri Vaishnav Institute of Textile Technology'].append(d)
        elif(department == 'Shri Vaishnav Institute of Agriculture'): branches['Shri Vaishnav Institute of Agriculture'].append(d)
        elif(department == 'Shri Vaishnav Institute of Architecture'): branches['Shri Vaishnav Institute of Architecture'].append(d)
        elif(department == 'Shri Vaishnav Institute of Commerce'): branches['Shri Vaishnav Institute of Commerce'].append(d)
        elif(department == 'Shri Vaishnav Institute of Computer Applications'): branches['Shri Vaishnav Institute of Computer Applications'].append(d)
        elif(department == 'Shri Vaishnav Institute of Fine Arts'): branches['Shri Vaishnav Institute of Fine Arts'].append(d)
        elif(department == 'Shri Vaishnav Institute of Forensic Science'): branches['Shri Vaishnav Institute of Forensic Science'].append(d)
        elif(department == 'Shri Vaishnav Institute of Journalism and Mass Communication'): branches['Shri Vaishnav Institute of Journalism and Mass Communication'].append(d)
        elif(department == 'Shri Vaishnav Institute of Science'): branches['Shri Vaishnav Institute of Science'].append(d)
        elif(department == 'Shri Vaishnav Institute of Social Science, Humanities and Arts'): branches['Shri Vaishnav Institute of Social Science, Humanities and Arts'].append(d)
        elif(department == 'Shri Vaishnav School of Law'): branches['Shri Vaishnav School of Law'].append(d)
        elif(department == 'Shri Vaishnav School of Management'): branches['Shri Vaishnav School of Management'].append(d)
    return branches


def branchesListToCsv(branches):
    fieldnames = ["Name","Position","Department","Email-ID","Qualification","Research Area"]
    for department,profiles in branches.items():
        with open("C:/Users/Ashish Rawat/Desktop/FacultyInfo/"+department+'_Faculties.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for profile in profiles:

                writer.writerow(profile)

        


url = "https://svvv.edu.in/UserPanel/EMPBiodata.aspx#collapse7"


print("Getting Data...")
r =  requests.get(url)
print("Data Recieved.\n")

htmlContent  = r.content

soup = BeautifulSoup(htmlContent,"html.parser")


print("Fetching Profiles From htmlContent...")
listOfProfiles = getProfiles(htmlContent)
print("Profiles Fetched From htmlContent.\n")

print("Sorting Profiles By Branches...")
profilesByBranches = getProfilesByBranches(listOfProfiles)
print("Profiles Sorted By Branches\n")


print([len(i) for  i in profilesByBranches.values()])



branchesListToCsv(profilesByBranches)
#profiles = profilesByBranches["Information Technology"]
#for i in profiles:
#print(i)


