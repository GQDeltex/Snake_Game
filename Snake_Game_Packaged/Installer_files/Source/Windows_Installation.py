from win32com.client import Dispatch
import shutil
import zipfile
import os
import time

install_location_ = 'C:\\Program Files (x86)\\PeteStudioGames\\Snake_Game\\'
install_location = 'C:\\PeteStudioGames\\Snake_Game\\'
dir_location_ = 'C:\\Program Files (x86)\\PeteStudioGames'
dir_location = 'C:\\PeteStudioGames'
error = False
 
def createShortcut(path, target='', wDir='', icon=''):    
    ext = path[-3:]
    if ext == 'url':
        shortcut = file(path, 'w')
        shortcut.write('[InternetShortcut]\n')
        shortcut.write('URL=%s' % target)
        shortcut.close()
    else:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        if icon == '':
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()

def unzip(target_file, output_file):
    fh = open(target_file, 'rb')
    z = zipfile.ZipFile(fh)
    for name in z.namelist():
        z.extract(name, output_file)
    fh.close()

def copy(src, dst):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    shutil.copytree(src, dst)

print "Install [Y] or uninstall [n] the 'snake game'?"
answer = raw_input("")
if answer == 'y' or answer == 'Y':
    try:
        print "Unzipping"
        unzip('Snake_Game_Windows_v0.3.zip', 'Snake_Game_v0.3\\')
    except:
        print "ERROR!!  Unzipping Failed"
        error = True
    time.sleep(1)
    try:
        print "Copying"
        copy('Snake_Game_v0.3', install_location)
    except:
        print "ERROR!! Copying Failed"
        error = True
    time.sleep(1)
    try:
        print "Deleting unused Files"
        shutil.rmtree('Snake_Game_v0.3')
    except:
        print "ERROR!!  Deleting Files Failed"
        error = True
    time.sleep(1)
    try:
        print "Creating Shortcut"
        createShortcut(path = os.path.join(os.path.expanduser('~'), 'Desktop\\Snake_game.lnk'), target = os.path.join(install_location, 'game.exe'), wDir = install_location)
    except:
        print "ERROR!!  Creating Shortcut Failed"
        error = True
    if error == True:
        print "Finished, but Errors occured, try again later."
    else:
        print "Finished!"
    time.sleep(1)
    raw_input("Press any key to continute...")
elif answer == 'n' or answer == 'N':
    print "Removing Files"
    try:    
        shutil.rmtree(install_location)
        os.rmdir(dir_location)
    except:
        print "ERROR!!  Failed to delete the Snake Game at: ", install_location
        error = True
    try:
        os.remove(os.path.join(os.path.expanduser('~'), 'Desktop\\Snake_game.lnk'))
    except:
        print "ERROR!!  Failed to delete shortcut!"
        error = True
    if error == True:
        print "Finished, but Errors occured, try again later."
    else:
        print "Finished"
    raw_input("Press any key to continute...")
else:
    print "No option!"
    raw_input("Press any key to continute...")
    
