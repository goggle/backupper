#!/usr/bin/env python
import sys
import os
import datetime
import re
import shutil
# import configparser
import config

# The directories we want to backup:
DIRECTORIES = ['/home/alex/Documents', '/home/alex/Pictures', '/home/alex/Music', '/home/alex/Calibre']

# The directory, where we want to store the backups:
BACKUP_DIRECTORY = '/mnt/harddrive/backup'


class Backup:
    def __init__(self, backupType):
        configurations = config.Config()
        self.backupDirectory = configurations.getBackupDirectory()
        self.backupEntries = configurations.getBackupEntries()
        self.backupType = backupType
        # self.time = datetime.datetime.now()
        # self.names = []
        # for directory in DIRECTORIES:
        #     self.names.append(os.path.split(directory)[-1])
        self.fullBackupFilenameExtension = 'full'
        self.incrementalBackupFilenameExtension = 'incremental'

    def fullBackupAvailable(self):
        pass


    def performBackup(self):
        if self.backupType == 'full':
            print('Performing full backup...')
            timeString = self.datetimeToString(self.time)

            for directory, name in zip(DIRECTORIES, self.names):
                print('Backup ' + directory + ' ...')
                snarName = name + '_' + timeString + '_full.snar'
                snarDirectory = os.path.join(BACKUP_DIRECTORY, snarName)
                tarName = name + '_' + timeString + '_full.tar.gz'
                tarDirectory = os.path.join(BACKUP_DIRECTORY, tarName)
                commandString = 'cd ' + directory + ' && cd .. && tar --listed-increment ' + snarDirectory + ' -czpf ' + tarDirectory + ' ' + name
                os.system(commandString)

        elif self.backupType == 'incremental':
            print('Performing incremental backup...')
            timeString = self.datetimeToString(self.time)

            for directory, name in zip(DIRECTORIES, self.names):
                print('Backup (incrmental) ' + directory + ' ...')
                lastTime = self.getTimeOfLastFullUpdate(name)
                if not lastTime:
                    print('Could not perform incremental backup of ' + directory + '. There was no full backup found!')
                    continue
                lastTimeString = self.datetimeToString(lastTime)

                # Copy the snar file of the last full update, so that it does not get overwritten:
                lastSnarName = name + '_' + lastTimeString + '_full.snar'
                shutil.copy(os.path.join(BACKUP_DIRECTORY, lastSnarName), os.path.join(BACKUP_DIRECTORY, 'tmp.snar'))

                tarName = name + '_' + timeString + '_incremental.tar.gz'
                tarDirectory = os.path.join(BACKUP_DIRECTORY, tarName)
                snarDirectory = os.path.join(BACKUP_DIRECTORY, 'tmp.snar')
                commandString = 'cd ' + directory + ' && cd .. && tar --listed-increment ' + snarDirectory + ' -czpf ' + tarDirectory + ' ' + name

                os.system(commandString)
                os.remove(snarDirectory)
        else:
            print('No backup performed!')


    def getTimeOfLastFullUpdate(self, name):
        regex = name + '_\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d_full.tar.gz'
        files = os.listdir(BACKUP_DIRECTORY)
        fullBackups = []
        for f in files:
            if re.match(regex, f):
                # fullBackups.append(f)
                datetimeRegex = '\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d'
                match = re.search(datetimeRegex, f)
                b = match.span()[0]
                e = match.span()[1]
                datetimeString = f[b:e]
                # print(datetimeString)
                year = int(datetimeString[0:4])
                month = int(datetimeString[5:7])
                day = int(datetimeString[8:10])
                hour = int(datetimeString[11:13])
                minute = int(datetimeString[14:16])
                second = int(datetimeString[17:19])
                dt = datetime.datetime(year, month, day, hour=hour, minute=minute, second=second)
                fullBackups.append(dt)

        if not fullBackups:
            return None

        # Return the newest found datetime object:
        return max(fullBackups)


    def datetimeToString(self, time):
        return time.strftime("%Y-%m-%d-%H-%M-%S")


class NoFullBackupException(Exception):
    pass


# if __name__ == '__main__':
#     if len(sys.argv) <= 1:
#         print("Specify the type of the backup: Use either 'full' for a full backup or 'incremental' for a incremental backup.")
#         sys.exit(0)
#     backupType = ''
#     if sys.argv[1] == 'full':
#         backupType = 'full'
#     elif sys.argv[1] == 'incremental':
#         backupType = 'incremental'
#     else:
#         print("No valid backup type specified. Use either 'full' for a full backup or 'incremental' for a incremental backup.")
#         sys.exit(0)
#
#     backup = Backup(backupType)
#     backup.performBackup()
