#!/usr/bin/env python
import sys
import os
import datetime
import re
import shutil
# import configparser
# import config
import logging
import shlex
import subprocess
import utils

# The directories we want to backup:
# DIRECTORIES = ['/home/alex/Documents', '/home/alex/Pictures', '/home/alex/Music', '/home/alex/Calibre']

# The directory, where we want to store the backups:
# BACKUP_DIRECTORY = '/mnt/harddrive/backup'


class Backup:
    # def __init__(self, backupType):
    def __init__(self, organizer):
        # configurations = config.Config()
        # self.backupDirectory = configurations.getBackupDirectory()
        # self.backupEntries = configurations.getBackupEntries()
        # self.logFile = configurations.getLogFile()

        self.organizer = organizer
        self.backupDirectory = organizer.configurations.getBackupDirectory()
        self.backupEntries = organizer.configurations.getBackupEntries()

        # self.backupType = backupType
        # self.time = datetime.datetime.now()
        # self.names = []
        # for directory in DIRECTORIES:
        #     self.names.append(os.path.split(directory)[-1])
        self.fullBackupFilenameExtension = organizer.getFullBackupFilenameExtension()
        self.incrementalBackupFilenameExtension = organizer.getIncrementalBackupFilenameExtension()
        self.dateTimeRegexString = organizer.getDateTimeRegexString()

        # Initialize the logger:
        # logging.basicConfig(filename=self.logFile, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')


    # def fullBackupAvailable(self):
    #     """
    #     This method checks, if there is a full backup of all the specified
    #     backup entries available. It returns 'True', if there is a full backup
    #     available, and 'False' otherwise.
    #     """
    #     files = os.listdir(self.backupDirectory)
    #     for entry in self.backupEntries:
    #         found = False
    #         name = entry.getName()
    #         fileExtension = entry.getFilenameExtension()
    #         regexString = name + '_\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d_' + self.fullBackupFilenameExtension + fileExtension
    #         for f in files:
    #             if re.match(regexString, f):
    #                 found = True
    #                 break
    #         if not found:
    #             return False
    #     return True


    def performFullBackupOfEntry(self, backupEntry):
        """
        Performs a full backup of a given backup entry.
        """
        time = datetime.datetime.now()
        # timeString = self.datetimeToString(time)
        timeString = self.organizer.datetimeToString(time)

        name = backupEntry.getName()
        compression = backupEntry.getCompressionType()
        fileExtension = backupEntry.getFilenameExtension()
        directory = backupEntry.getDirectory()
        directoryName = directory.strip('/')
        if directoryName.find('/') == -1:
            directoryName = '/'
        else:
            while True:
                ind = directoryName.find('/')
                if ind == -1:
                    break
                directoryName = directoryName[ind + 1 :]

        snarFilename = name + '_' + timeString + '.snar'
        tarFilename = name + '_' + timeString + '_' + self.fullBackupFilenameExtension + fileExtension

        snarFullFilename = os.path.join(self.backupDirectory, snarFilename)
        tarFullFilename = os.path.join(self.backupDirectory, tarFilename)

        tarDict = {
            'tar': '',
            'gz': 'z',
            'bz2': 'j',
            'xz': 'J'
        }

        command = 'tar'
        commandOptions = ' --listed-increment ' + snarFullFilename + ' -c' + tarDict[compression] + 'pf ' + tarFullFilename + ' ' + directoryName
        commandString = command + commandOptions

        logging.info('Starting full backup of ' + directory + '.')

        try:
            currentDir = os.getcwd()
            os.chdir(directory)
            os.chdir('..')
            process = subprocess.Popen(shlex.split(commandString), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logging.error('Executing tar resulted in an error.')
                logging.error(stderr)
            os.chdir(currentDir)
            logging.info('Successfully created full backup of ' + directory + ' and stored in ' + tarFullFilename + \
                '. The corresponding snapshot was stored in ' + snarFullFilename + '.')

        except OSError as exception:
            logging.error('Exception occured: ' + str(exception))
            os.chdir(currentDir)
        except Exception as exception:
            logging.error('An unknown exception occured: ' + str(exception))
            os.chdir(currentDir)


    def performFullBackup(self):
        for entry in self.backupEntries:
            self.performFullBackupOfEntry(entry)


    def performIncrementalBackupOfEntry(self, backupEntry):
        """
        Performs an incremental backup of a given backup entry.
        """
        time = datetime.datetime.now()
        # timeString = self.datetimeToString(time)
        timeString = self.organizer.datetimeToString(time)

        name = backupEntry.getName()
        compression = backupEntry.getCompressionType()
        fileExtension = backupEntry.getFilenameExtension()
        directory = backupEntry.getDirectory()
        directoryName = directory.strip('/')
        if directoryName.find('/') == -1:
            directoryName = '/'
        else:
            while True:
                ind = directoryName.find('/')
                if ind == -1:
                    break
                directoryName = directoryName[ind + 1 :]

        # snarFilename = name + '_' + timeString + '.snar'
        tarFilename = name + '_' + timeString + '_' + self.incrementalBackupFilenameExtension + fileExtension
        # snarFullFilename = os.path.join(self.backupDirectory, snarFilename)
        tarFullFilename = os.path.join(self.backupDirectory, tarFilename)

        tarDict = {
            'tar': '',
            'gz': 'z',
            'bz2': 'j',
            'xz': 'J'
        }


        logging.info('Starting incremental backup of ' + directory + '.')
        try:
            lastFullBackupTime = self.getTimeOfLastFullBackup(backupEntry)
        except NoBackupException:
            logging.error('Could not find a previous full backup of ' + directory + '. Aborting!')
            return
        # lastFullBackupTimeString = self.datetimeToString(lastFullBackupTime)
        lastFullBackupTimeString = self.organizer.datetimeToString(lastFullBackupTime)

        # lastSnarFilename = name + '_' + lastTimeString + '.snar'
        # lastSnarFullFilename = os.path.join(self.backupDirectory, lastSnarFilename)
        snarFilename = name + '_' + lastFullBackupTimeString + '.snar'
        snarFullFilename = os.path.join(self.backupDirectory, snarFilename)

        command = 'tar'
        commandOptions = ' --listed-increment ' + snarFullFilename + ' -c' + tarDict[compression] + 'pf ' + tarFullFilename + ' ' + directoryName
        commandString = command + commandOptions

        try:
            currentDir = os.getcwd()
            os.chdir(directory)
            os.chdir('..')
            process = subprocess.Popen(shlex.split(commandString), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logging.error('Executing tar resulted in an error.')
                logging.error(stderr)
            os.chdir(currentDir)
            logging.info('Successfully created incremental backup of ' + directory + ' and stored in ' + tarFullFilename + \
                '. The corresponding snapshot was stored in ' + snarFullFilename + '.')

        except OSError as exception:
            logging.error('Exception occured: ' + str(exception))
            os.chdir(currentDir)
        except Exception as exception:
            logging.error('An unknown exception occured: ' + str(exception))
            os.chdir(currentDir)


    def performIncrementalBackup(self):
        for entry in self.backupEntries:
            self.performIncrementalBackupOfEntry(entry)



    def getTimeOfLastBackup(self, backupEntry):
        """
        Returns the time of the last performed backup (full or incremental)
        of a given backup entry.
        It raises a NoBackupException, if no backup could be found.
        """
        fileExtension = backupEntry.getFilenameExtension()
        name = backupEntry.getName()
        regexFullString = name + '_' + self.dateTimeRegexString + '_'+ self.fullBackupFilenameExtension + fileExtension
        regexIncrementalString = name + '_' + self.dateTimeRegexString + '_' + self.incrementalBackupFilenameExtension + fileExtension
        files = os.listdir(self.backupDirectory)
        dateTimes = []
        for f in files:
            if re.match(regexFullString, f) or re.match(regexIncrementalString, f):
                match = re.search(self.dateTimeRegexString, f)
                b = match.span()[0]
                e = match.span()[1]
                datetimeString = f[b:e]
                year = int(datetimeString[0:4])
                month = int(datetimeString[5:7])
                day = int(datetimeString[8:10])
                hour = int(datetimeString[11:13])
                minute = int(datetimeString[14:16])
                second = int(datetimeString[17:19])
                dt = datetime.datetime(year, month, day, hour=hour, minute=minute, second=second)
                dateTimes.append(dt)

        if not dateTimes:
            raise NoBackupException
        return max(dateTimes)


    def getTimeOfLastFullBackup(self, backupEntry):
        fileExtension = backupEntry.getFilenameExtension()
        name = backupEntry.getName()
        regexFullString = name + '_' + self.dateTimeRegexString + '_' + self.fullBackupFilenameExtension + fileExtension
        files = os.listdir(self.backupDirectory)
        dateTimes = []
        for f in files:
            if re.match(regexFullString, f):
                match = re.search(self.dateTimeRegexString, f)
                b = match.span()[0]
                e = match.span()[1]
                datetimeString = f[b:e]
                year = int(datetimeString[0:4])
                month = int(datetimeString[5:7])
                day = int(datetimeString[8:10])
                hour = int(datetimeString[11:13])
                minute = int(datetimeString[14:16])
                second = int(datetimeString[17:19])
                dt = datetime.datetime(year, month, day, hour=hour, minute=minute, second=second)
                dateTimes.append(dt)

        if not dateTimes:
            raise NoBackupException
        return max(dateTimes)



    # def performBackup(self):
    #     if self.backupType == 'full':
    #         print('Performing full backup...')
    #         # timeString = self.datetimeToString(self.time)
    #         timeString = self.organizer.datetimeToString(self.time)
    #
    #         for directory, name in zip(DIRECTORIES, self.names):
    #             print('Backup ' + directory + ' ...')
    #             snarName = name + '_' + timeString + '_full.snar'
    #             snarDirectory = os.path.join(BACKUP_DIRECTORY, snarName)
    #             tarName = name + '_' + timeString + '_full.tar.gz'
    #             tarDirectory = os.path.join(BACKUP_DIRECTORY, tarName)
    #             commandString = 'cd ' + directory + ' && cd .. && tar --listed-increment ' + snarDirectory + ' -czpf ' + tarDirectory + ' ' + name
    #             os.system(commandString)
    #
    #     elif self.backupType == 'incremental':
    #         print('Performing incremental backup...')
    #         # timeString = self.datetimeToString(self.time)
    #         timeString = self.organizer.datetimeToString(self.time)
    #
    #         for directory, name in zip(DIRECTORIES, self.names):
    #             print('Backup (incrmental) ' + directory + ' ...')
    #             lastTime = self.getTimeOfLastFullUpdate(name)
    #             if not lastTime:
    #                 print('Could not perform incremental backup of ' + directory + '. There was no full backup found!')
    #                 continue
    #             # lastTimeString = self.datetimeToString(lastTime)
    #             lastTimeString = self.organizer.datetimeToString(lastTime)
    #
    #             # Copy the snar file of the last full update, so that it does not get overwritten:
    #             lastSnarName = name + '_' + lastTimeString + '_full.snar'
    #             shutil.copy(os.path.join(BACKUP_DIRECTORY, lastSnarName), os.path.join(BACKUP_DIRECTORY, 'tmp.snar'))
    #
    #             tarName = name + '_' + timeString + '_incremental.tar.gz'
    #             tarDirectory = os.path.join(BACKUP_DIRECTORY, tarName)
    #             snarDirectory = os.path.join(BACKUP_DIRECTORY, 'tmp.snar')
    #             commandString = 'cd ' + directory + ' && cd .. && tar --listed-increment ' + snarDirectory + ' -czpf ' + tarDirectory + ' ' + name
    #
    #             os.system(commandString)
    #             os.remove(snarDirectory)
    #     else:
    #         print('No backup performed!')


    def getTimeOfLastFullUpdate(self, name):
        regex = name + '_\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d_full.tar.gz'
        # regex = name + '_' + self.dateTimeRegexString + '_' + self.fullBackupFilenameExtension
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


    # def datetimeToString(self, time):
    #     return time.strftime("%Y-%m-%d-%H-%M-%S")


# class NoFullBackupException(Exception):
#     pass

class NoBackupException(Exception):
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
