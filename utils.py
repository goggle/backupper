import config
import logging

#
#
# fullBackupFilenameExtension = 'full'
# incrementalBackupFilenameExtension = 'incremental'
# dateTimeRegexString = '\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d'
#
#
# def datetimeToString(time):
#     return time.strftime("%Y-%m-%d-%H-%M-%S")

class Organizer:

    def __init__(self):
        self.fullBackupFilenameExtension = 'full'
        self.incrementalBackupFilenameExtension = 'incremental'
        self.dateTimeRegexString = '\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d'

        self.configurations = config.Config()
        self.logFile = self.configurations.getLogFile()

        # Initialize the logger:
        logging.basicConfig(filename=self.logFile, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

    def getFullBackupFilenameExtension(self):
        return self.fullBackupFilenameExtension

    def getIncrementalBackupFilenameExtension(self):
        return self.incrementalBackupFilenameExtension

    def getDateTimeRegexString(self):
        return self.dateTimeRegexString

    def getLogFile(self):
        return self.logFile



    def datetimeToString(self, time):
        return time.strftime("%Y-%m-%d-%H-%M-%S")
