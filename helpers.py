import os
import shutil
import stat

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(
                os.path.join(root, file), 
                os.path.relpath(
                    os.path.join(root, file), 
                    os.path.join(path, '..')
                )
            )

# TODO Remove read-only files for Windows
def rmdir(path):
    for root, dirs, files in os.walk(path):  
        for name in dirs:
            os.chmod(os.path.join(root, name), stat.S_IWRITE)
        for name in files:
            os.chmod(os.path.join(root, name), stat.S_IWRITE)
    shutil.rmtree(path)