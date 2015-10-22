import config
import logging
import datetime
import re
import os


class Organizer:

    def __init__(self):
        self.fullBackupFilenameExtension = 'full'
        self.incrementalBackupFilenameExtension = 'incremental'
        self.dateTimeRegexString = '\d\d\d\d-\d\d-\d\d-\d\d-\d\d-\d\d'

        self.configurations = config.Config()
        self.logFile = self.configurations.getLogFile()

        # Initialize the logger:
        logging.basicConfig(filename=self.logFile, level=logging.INFO, format='[%(levelname)s] %(asctime)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')

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

    def getTimeOfLastFullBackup(self, backupEntry):
        fileExtension = backupEntry.getFilenameExtension()
        name = backupEntry.getName()
        regexFullString = name + '_' + self.dateTimeRegexString + '_' + self.fullBackupFilenameExtension + fileExtension
        files = os.listdir(self.configurations.getBackupDirectory())
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


    def getTimeOfLastFullBackupBeforeDate(self, backupEntry, date=datetime.datetime.now()):
        fileExtension = backupEntry.getFilenameExtension()
        name = backupEntry.getName()
        regexFullString = name + '_' + self.dateTimeRegexString + '_' + self.fullBackupFilenameExtension + fileExtension
        files = os.listdir(self.configurations.getBackupDirectory())
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
                if dt <= date:
                    dateTimes.append(dt)

        if not dateTimes:
            raise NoBackupException
        return max(dateTimes)


    def getIncrementalTimesBetweenDates(self, backupEntry, startDate, endDate=datetime.datetime.now()):
        """

        """
        fileExtension = backupEntry.getFilenameExtension()
        name = backupEntry.getName()
        regexIncrementalString = name + '_' + self.dateTimeRegexString + '_' + self.incrementalBackupFilenameExtension + fileExtension
        files = os.listdir(self.configurations.getBackupDirectory())
        dateTimes = []
        for f in files:
            if re.match(regexIncrementalString, f):
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
                if dt >= startDate and dt <= endDate:
                    dateTimes.append(dt)

        return sorted(dateTimes)



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
        files = os.listdir(self.configurations.getBackupDirectory())
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


class NoBackupException(Exception):
    pass
