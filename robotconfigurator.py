import os
import platform
import subprocess


def get_os():
    if platform.system() == "Windows":
        return "Windows"

    elif platform.system() == "Linux":
        distro = subprocess.check_output(['lsb_release', '-is']).decode('utf-8')[:-1]

        if distro == "ManjaroLinux":
            return "Manjaro"

        else:
            return "Other"

def append_text_to_file(path, content):
    try:
        file = open(path, "a")
        file.write(content)
        file.close()

    except IOError:
        print("Could not create file", path)

def get_linux_kernel():
    return subprocess.check_output(["uname", "-r"]).decode("utf-8").replace(".", "")[:3]

def install(program, system):
    try:
        with open("Scripts/" + system + "/" + program, "r") as script:
            for line in script:
                if not line == "\n":
                    if line.startswith("#"):
                        exec(line[1:].replace('\n', ''))
                    else:
                        os.system(line.replace('\n', ''))
                else:
                    pass
    except IOError:
        print("Not supported")


if __name__ == "__main__":
    if not get_os() == "other":
        try:
            with open("programs-to-install.txt", "r") as programs_to_install:
                for line in programs_to_install:
                    if (not line.startswith("#")) and (not line == "\n"):
                        install(line.replace('\n', ''), get_os())

        except KeyboardInterrupt:
            print("Stopped by user")

        except IOError:
            print("Could not read programs-to-install.txt")

    else:
        print("Unsupported OS :(")