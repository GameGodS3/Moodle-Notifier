usr = input("Enter Moodle Username: ")
pwd = input("Enter Moodle Password: ")
with open(".env", "w") as f:
    f.write(f'MOODLEUSERNAME="{usr}"\nMOODLEPASSWD="{pwd}"')
print("Credentials stored in .env file!")
