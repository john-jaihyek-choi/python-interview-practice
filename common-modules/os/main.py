import os


# File and Directory Operations
# List Directory
def list_folder_contents(path) -> None:
    output = os.listdir(path)

    print(output)


list_folder_contents("./")


# Check if path exists
def check_if_path_exists(path: str) -> None:
    if os.path.exists(path):
        print(f"path {path} exists")
    else:
        print("path not found")


check_if_path_exists("new_directory")
check_if_path_exists("something-unique")


# Make New Directory
def make_new_directory(path: str) -> None:
    try:
        os.makedirs(path, exist_ok=True)
        print(f"new directory created: {path}")
    except Exception:
        print("unexpected error")


make_new_directory("new_directory")
make_new_directory("new_directory/new_sub_directory")
make_new_directory("new_directory/to_be_deleted")


# Remove directory
def delete_directory(path) -> None:
    try:
        os.rmdir(path)
        print(f"deleted directory - {path}")
    except Exception as e:
        print("unexpected error")


delete_directory("new_directory/to_be_deleted")


# Rename file
def rename_file_or_dir(src: str, dst: str) -> None:
    try:
        # os.rename(src, dst)
        os.replace(src, dst)
        print("rename successul!")
    except Exception as e:
        print(f"unexpected error - {e}")


rename_file_or_dir(
    "new_directory/new_sub_directory", "new_directory/sub_directory_new_name/new_sub"
)


# Make new file
def make_new_file(path: str) -> None:
    try:
        dir = os.path.dirname(path)
        make_new_directory(dir)
        with open(path, "w") as file:
            file.write("uploading content")
        print(f"successfully written a file to: {path}")
    except Exception as e:
        print(e)
        print("unexpected error")


make_new_file("new/new.txt")


# Path Handling
# os.path.join(a, b, ...)
def join_paths(*args) -> str:
    path = os.path.join(*args)

    print(f"joined path - {path}")
    return path


join_paths("new_directory", "sub_directory_new_name", "new_sub")


# Get base name (right most) of the path
def get_basename(path: str) -> None:
    base = os.path.basename(path)
    print(f"base name for the path '{base}'")


get_basename(join_paths("new_directory", "sub_directory_new_name", "new_sub"))


# Get directory name (everything to the left of basename)
def dirname(path: str) -> None:
    file_path = "new_directory/sub_directory_new_name/new_sub/test.json"

    dir = os.path.dirname(file_path)
    print(dir)


dirname("main.py")


# Get root and ext of the filename
def splittext(path: str) -> None:
    root, ext = os.path.splitext(path)
    print(f"splitted path - root: {root} / ext: {ext}")


splittext("new_directory/sub_directory_new_name/new_sub/test.json")


# Get Current Working Directory Path
def get_cwd() -> None:
    print(os.getcwd())


get_cwd()


# Environment Variables
# Get Enviroment Variable
def list_env_vars() -> None:
    os.environ["ENV_VAR"] = "SOME VALUE"
    env_var = os.getenv("ENV_VAR", None)
    print(env_var)


list_env_vars()


# Process control
# Get Process ID
def get_process_id() -> None:
    print(os.getpid())


get_process_id()
