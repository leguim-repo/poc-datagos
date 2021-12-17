import os
from configparser import ConfigParser

if __name__ == '__main__':
    ENV = os.getenv("ENVIRONMENT", "dev")

    conf = ConfigParser()
    conf.read(["default.ini", f"{ENV}.ini"])
    host = conf.get("db", "host")
    print(f"{host}")

