# import utils
import logging
import os

class Remove:
    def __init__(self, organizer):
        self.organizer = organizer
        self.backupDirectory = organizer.configurations.getBackupDirectory()
        self.backupEntries = organizer.configurations.getBackupEntries()

        self.fullBackupFilenameExtension = organizer.getFullBackupFilenameExtension()
        self.incrementalBackupFilenameExtension = organizer.getIncrementalBackupFilenameExtension()
        self.dateTimeRegexString = organizer.getDateTimeRegexString()


    def removePreviousBackupEntryCycles(self, backupEntry):
        name = backupEntry.getName()
        fileExtension = backupEntry.getFilenameExtension()
        logging.info('Beginning to remove previous backup cycles of ' + name + '.')
        if not self.organizer.moreThanOneFullBackupAvailable(backupEntry):
            logging.info('No previous backup cycle of ' + name + ' available. Nothing to remove.')
            return

        fullBackupDates = self.organizer.getDatesOfPreviousFullBackups(backupEntry)
        incrementalBackupDates = self.organizer.getDatesOfPreviousIncrementalBackups(backupEntry)

        for date in fullBackupDates:
            filenameFullBackup = name + '_' + self.organizer.datetimeToString(date) + '_' + self.fullBackupFilenameExtension + fileExtension
            filenameSnar = name + '_' + self.organizer.datetimeToString(date) + '.snar'

            fullFilenameFullBackup = os.path.join(self.backupDirectory, filenameFullBackup)
            os.remove(fullFilenameFullBackup)
            logging.info('File ' + fullFilenameFullBackup + ' removed.')

            fullFilenameSnar = os.path.join(self.backupDirectory, filenameSnar)
            os.remove(fullFilenameSnar)
            logging.info('File ' + fullFilenameSnar + ' removed.')


        for date in incrementalBackupDates:
            filenameIncrementalBackup = name + '_' + self.organizer.datetimeToString(date) + '_' + self.incrementalBackupFilenameExtension + fileExtension
            fullFilenameIncrementalBackup = os.path.join(self.backupDirectory, filenameIncrementalBackup)
            os.remove(fullFilenameIncrementalBackup)
            logging.info('File ' + fullFilenameIncrementalBackup + ' removed.')


    def removePreviousBackupCycles(self):
        for entry in self.backupEntries:
            self.removePreviousBackupEntryCycles(entry)
