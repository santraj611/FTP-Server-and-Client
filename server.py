from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read("server_config.conf")
folder = config["directory"]["folder"]
username = config["credentials"]["username"]
password = config["credentials"]["password"]
ip_address = config["network"]["ip_address"]
port = config["network"]["port"]

def main():
    # Instantiate a dummy authorizer
    authorizer = DummyAuthorizer()

    # Define a new user with full permissions
    authorizer.add_user(username, password, folder, perm="elradfmw")

    # Define an anonymous user with read-only permissions
    authorizer.add_anonymous(folder)

    # Instantiate an FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (optional)
    handler.banner = "Welcome to my FTP server."

    # Instantiate an FTP server
    address = (ip_address, int(port))
    server = FTPServer(address, handler)

    # Set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Start FTP server
    server.serve_forever()

if __name__ == "__main__":
    main()
