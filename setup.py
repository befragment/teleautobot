import configparser
from cprint import *
import os


try:
    change = int(input("// Do you want to change your setup? [0-no / 1-yes]: "))
except ValueError:
    cprint.err("// Type in a number!")
    sys.exit(1)

if change or os.path.getsize('config.ini') == 0:
    cparse = configparser.ConfigParser()
    cparse.add_section("UserInfo")

    api_id = input("Enter your api id: ")
    cparse.set("UserInfo", "id", api_id)
    api_hash = input("Enter your api hash: ")
    cparse.set("UserInfo", "hash", api_hash)
    phone_number = input("Enter your phone number: ")
    cparse.set("UserInfo", "phone", phone_number)

    setup = open('config.ini', 'w')
    cparse.write(setup)
    setup.close()

    cprint.info("Setup is completed")
else:
    cprint.info("OK")
