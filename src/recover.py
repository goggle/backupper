import utils
import logging
import datetime
import os
import subprocess
import shlex

class Recover:
    def __init__(self, organizer):
        self.organizer = organizer

        self.backupDirectory = organizer.configurations.getBackupDirectory()
        self.recoveryDirectory = organizer.configurations.getRecoveryDirectory()
        self.backupEntries = organizer.configurations.getBackupEntries()

        self.fullBackupFilenameExtension = organizer.getFullBackupFilenameExtension()
        self.incrementalBackupFilenameExtension = organizer.getIncrementalBackupFilenameExtension()
        self.dateTimeRegexString = organizer.getDateTimeRegexString()


    def recoverBackupUpToDate(self, date=datetime.datetime.now()):
        for entry in self.backupEntries:
            self.recoverBackupEntryUpToDate(entry, date)

    def recoverBackupEntryUpToDate(self, backupEntry, date=datetime.datetime.now()):
        name = backupEntry.getName()
        compression = backupEntry.getCompressionType()
        fileExtension = backupEntry.getFilenameExtension()
        directory = backupEntry.getDirectory()
        tarDict = {
            'tar': '',
            'gz': 'z',
            'bz2': 'j',
            'xz': 'J'
        }

        logging.info('Beginning recovery of ' + name + '.')

        # Check, if the recovery already exists:
        directoryName = directory.strip('/')
        if directoryName.find('/') == -1:
            directoryName = '/'
        else:
            while True:
                ind = directoryName.find('/')
                if ind == -1:
                    break
                directoryName = directoryName[ind + 1 :]
        checkDir = os.path.join(self.recoveryDirectory, directoryName)
        if os.path.exists(checkDir):
            logging.warning('The directory ' + checkDir + ' already exists. You should move it first. Aborted recovery of ' + name + '.')
            return


        try:
            fullBackupDate = self.organizer.getTimeOfLastFullBackupBeforeDate(backupEntry, date)
            fullBackupDateString = self.organizer.datetimeToString(fullBackupDate)
        except utils.NoBackupException:
            logging.error('No full backup before the specified date could be found.')
            return

        fullBackupFilename = name + '_' + fullBackupDateString + '_' + self.fullBackupFilenameExtension + fileExtension
        fullBackupFullFilename = os.path.join(self.backupDirectory, fullBackupFilename)

        incrementalBackupDates = self.organizer.getIncrementalTimesBetweenDates(backupEntry, fullBackupDate, date)
        incrementalBackupFilenames = []
        for elem in incrementalBackupDates:
            datestring = self.organizer.datetimeToString(elem)
            filename = name + '_' + datestring + '_' + self.incrementalBackupFilenameExtension + fileExtension
            incrementalBackupFilenames.append(filename)

        command = 'tar'
        commandOptionsFullBackup = '-x' + tarDict[compression] + 'pf ' + fullBackupFullFilename + ' -C ' + self.recoveryDirectory

        try:
            commandString = command + ' ' + commandOptionsFullBackup
            process = subprocess.Popen(shlex.split(commandString), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logging.error('Executing tar resulted in an error.')
                logging.error(stderr)
            logging.info('Successfully recovered full backup ' + fullBackupFullFilename + ' into ' + self.recoveryDirectory + '.')

        except OSError as exception:
            logging.error('Exception occured: ' + str(exception))
            os.chdir(currentDir)
        except Exception as exception:
            logging.error('An unknown exception occured: ' + str(exception))
            os.chdir(currentDir)

        try:
            for filename in incrementalBackupFilenames:
                fullFilename = os.path.join(self.backupDirectory, filename)
                commandOptionsIncrementalBackup = '--incremental -x' + tarDict[compression] + 'pf ' + fullFilename + ' -C ' + self.recoveryDirectory
                commandString = command + ' ' + commandOptionsIncrementalBackup
                process = subprocess.Popen(shlex.split(commandString), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                if stderr:
                    logging.error('Executing tar resulted in an error.')
                    logging.error(stderr)
                logging.info('Successfully recovered incremental backup ' + fullFilename + ' into ' + self.recoveryDirectory + '.')
        except OSError as exception:
            logging.error('Exception occured: ' + str(exception))
            os.chdir(currentDir)
        except Exception as exception:
            logging.error('An unknown exception occured: ' + str(exception))
            os.chdir(currentDir)

        logging.info('Successfully recovered ' + name + ' up to ' + str(date) + '.')

class RecoveryExists(Exception):
    pass
