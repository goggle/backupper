import os
import datetime
import re
import shutil
import logging
import shlex
import subprocess
import utils


class Backup:
    def __init__(self, organizer):
        self.organizer = organizer
        self.backupDirectory = organizer.configurations.getBackupDirectory()
        self.backupEntries = organizer.configurations.getBackupEntries()

        self.fullBackupFilenameExtension = organizer.getFullBackupFilenameExtension()
        self.incrementalBackupFilenameExtension = organizer.getIncrementalBackupFilenameExtension()
        self.dateTimeRegexString = organizer.getDateTimeRegexString()



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

        tarFilename = name + '_' + timeString + '_' + self.incrementalBackupFilenameExtension + fileExtension
        tarFullFilename = os.path.join(self.backupDirectory, tarFilename)

        tarDict = {
            'tar': '',
            'gz': 'z',
            'bz2': 'j',
            'xz': 'J'
        }


        logging.info('Starting incremental backup of ' + directory + '.')
        try:
            lastFullBackupTime = self.organizer.getTimeOfLastFullBackup(backupEntry)
        except utils.NoBackupException:
            logging.error('Could not find a previous full backup of ' + directory + '. Aborting!')
            return
        lastFullBackupTimeString = self.organizer.datetimeToString(lastFullBackupTime)

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
