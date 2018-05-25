import os
import sys
import platform
import subprocess

# returns the current user (just a reminder :p)
def get_user():
    return os.getlogin()

# returns the running OS to decide where to search the installation scripts
def get_os():
    if platform.system() == "Windows":
        return "Windows"

    elif platform.system() == "Linux":
        distro = subprocess.check_output(['lsb_release', '-is']).decode('utf-8')[:-1]

        if distro == "ManjaroLinux":
            return "Manjaro"
        
        elif distro == "Debian":
            return "Debian"

        else:
            return "Other"
    else:
        return "Other"

# append some text to a file, useful to set config strings to system files.
def append_text_to_file(path, content):
    try:
        file = open(path, "a")
        file.write(content)
        file.close()

    except IOError:
        print("Could not create file", path)

# returns the current linux kernel formatted like 414, 415, 49... used only to install virtualbox modules
def get_linux_kernel():
    return subprocess.check_output(["uname", "-r"]).decode("utf-8").replace(".", "")[:3]

# run the correct scripts to install program to the specified system
def install(program, system):
    try:
        # install:program
        # script:action
        command = program.split(":")

        with open("Sources/" + command[0] + "/" + system + "/" + command[1], "r") as script:
            for line in script:
                if (not line == "\n") and (not line.startswith("#")):
                    if line.startswith("!"):
                        exec(line[1:].replace('\n', ''))
                    else:
                        os.system(line.replace('\n', ''))
                else:
                    pass
    except IOError:
        print(program + ": is not supported on this platform")

    except IndexError:
        print(program + ": line not recognized")

# starts the program
if __name__ == "__main__":
    # check if the system is supported
    if not get_os() == "Other":
        for param in sys.argv[1:]:
            # tries to run the installation scripts
            try:
                # if a file was received
                if os.path.isfile(param):
                    # tries to install every parameter received
                    with open(param, "r") as programs_to_install:
                        for line in programs_to_install:
                            # ignores commented and empty lines
                            if (not line.startswith("#")) and (not line == "\n"):
                                # runs the adequate script
                                install(line.replace('\n', ''), get_os())

                # installs a received argument
                else:
                    install(param, get_os())

            except KeyboardInterrupt:
                print("Stopped by user")
                os._exit(0)

            except IOError:
                print("Could not read the specified file")


    else:
        print("Unsupported OS :(")
