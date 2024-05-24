from ftplib import FTP
import os

def connect_ftp(server: str, port: int, user: str, passwd: str) -> FTP:
    ftp = FTP()
    ftp.connect(server, port)
    ftp.login(user, passwd)
    print(f"Connected to FTP server at {server}:{port}")
    return ftp

def list_files(ftp: FTP):
    files = ftp.nlst()
    print("Files on the server:")
    for file in files:
        print(file)

def download_file(ftp: FTP, filename: str, local_path: str):
    with open(local_path, 'wb') as f:
        ftp.retrbinary(f"RETR {filename}", f.write)
    print(f"Downloaded {filename} to {local_path}")

def upload_file(ftp: FTP, local_path: str, server_path: str):
    with open(local_path, 'rb') as f:
        ftp.storbinary(f"STOR {server_path}", f)
    print(f"Uploaded {local_path} to {server_path}")

def change_dir(ftp: FTP, path: str):
    if path == "..":
        ftp.cwd("..")
    elif path in ftp.nlst():
        ftp.cwd(path)
    else:
        print("Path {path} does not exist")
    print(f"Changed directory to {path}")

def get_user_quary():
    print()
    print("1. list (list files on the server)")
    print("2. cd subfolder (change directory or server)")
    print("3. list current (list files on the current directory)")
    print("4. download (download a file from the server)")
    print("5. upload (upload a file to the server)")
    print("6. exit (quit the program)")
    user_quary = input("\nWhat do you want to do?\n")
    return user_quary.lower()

def main():
    server = "127.0.0.1"
    port = 2121
    user = "android_user"
    passwd = "your_android_password"

    run = True
    ftp = connect_ftp(server, port, user, passwd)
    try:
        while run:
            quary = get_user_quary()

            if quary == "list" or quary == "1":
                list_files(ftp)
            elif quary == "cd" or quary == "2":
                path = input("What subfolder do you want to change to? ")
                change_dir(ftp, path.strip())
            elif quary == "list current" or quary == "3":
                print("Files on this Direcotry")
                for file in os.listdir():
                    print(file)

            elif quary == "download" or quary == "4":
                file_name = input("What file you wolud like to download? ")
                list_files(ftp)
                if file_name in ftp.nlst():
                    download_file(ftp, file_name, file_name)
                else:
                    print(f"{file_name} not found on the server")
            elif quary == "upload" or quary == "5":
                file_name = input("What file you wolud like to upload? ")
                print("Files on this Direcotry")
                for file in os.listdir():
                    print(file)
                if file_name in os.listdir():
                    upload_file(ftp, file_name, file_name)
                else:
                    print(f"{file_name} not found in this directory")
                upload_file(ftp, "local_file.txt", "server_file.txt")

            elif quary == "exit" or quary == "quit" or quary == "6":
                run = False

    except Exception as e:
        print(e)

    # try:
    #     list_files(ftp)
    #     upload_file(ftp, "local_file.txt", "server_file.txt")
    #     download_file(ftp, "server_file.txt", "downloaded_file.txt")
    # finally:
    #     ftp.quit()
    #     print("Disconnected from the FTP server")

if __name__ == "__main__":
    main()

