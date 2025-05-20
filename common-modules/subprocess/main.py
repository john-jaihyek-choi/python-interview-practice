import subprocess

# .run() - run cli commands
subprocess.run(["ls"])


# streams to standard output
output = subprocess.run(["echo", "hello world!"])

# captures stdout rather than streaming it to standard output
output = subprocess.run(["echo", "hello world!"], capture_output=True, text=True)

# Run shell expressions
subprocess.run(
    "echo $HOME", shell=True
)  # shell to be used carefully for any injections


def list_directory() -> None:
    try:
        output = subprocess.run(["ls", "-l"], capture_output=True, text=True)
        print(output.stdout)
        return
    except Exception:
        print("Unknown error")


def get_uptime() -> None:
    try:
        output = subprocess.run(["uptime"], capture_output=True, text=True)
        print(output.stdout.strip())
        return
    except:
        print("exception error")


list_directory()
get_uptime()
