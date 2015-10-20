import configparser
import os

HOME_DIRECTORY = os.path.expanduser('~')

# Specify the possible paths to the config files. The first items in the list
# have higher priorities:
CONFIG_FILES = ['/etc/backup_config', os.path.join(HOME_DIRECTORY, '.config/backup_config'),
    os.path.join(HOME_DIRECTORY, 'development/backup/backup_config')]


class Config:
    def __init__(self):
        hasConfig = False
        for elem in CONFIG_FILES:
            if os.path.isfile(elem):
                self.configFile = elem
                hasConfig = True
                break
        if not hasConfig:
            raise NoConfigFileException

        self.config = configparser.ConfigParser()
        self.config.read(self.configFile)

        if 'Default' not in self.config:
            raise NoDefaultSectionException

        if 'BackupDirectory' not in self.config['Default']:
            raise NoBackupDirectoryException

        if 'RecoveryDirectory' not in self.config['Default']:
            raise NoRecoveryDirectoryException

        if 'LogFile' not in self.config['Default']:
            raise NoLogFileException

        self.backupDirectory = self.config['Default']['BackupDirectory']
        self.recoveryDirectory = self.config['Default']['RecoveryDirectory']
        self.logFile = self.config['Default']['LogFile']

        if not os.path.isdir(self.backupDirectory):
            raise NoBackupDirectoryException

        if not os.path.isdir(self.recoveryDirectory):
            raise NoRecoveryDirectoryException

        self.entries = []
        hasSection = False
        for section in self.config.sections():
            if section == 'Default':
                continue

            hasSection = True
            name = section
            if 'Directory' not in self.config[section]:
                raise InvalidSectionException
            if 'Compression' not in self.config[section]:
                raise InvalidSectionException
            directory = self.config[section]['Directory']
            compressionType = self.config[section]['Compression']

            if compressionType == 'tar':
                pass
            elif compressionType == 'gz':
                pass
            elif compressionType == 'gzip':
                compressionType = 'gz'
            elif compressionType == 'bz2':
                pass
            elif compressionType == 'bzip2':
                compressionType = 'bz2'
            elif compressionType == 'xz':
                pass
            else:
                raise InvalidCompressionException

            if not os.path.isdir(directory):
                raise InvalidDirectoryException

            entry = BackupEntry(name, directory, compressionType)
            self.entries.append(entry)

        if not hasSection:
            raise NoEntrySectionException

    def getBackupDirectory(self):
        return self.backupDirectory

    def getRecoveryDirectory(self):
        return self.recoveryDirectory

    def getLogFile(self):
        return self.logFile

    def getBackupEntries(self):
        return self.entries




class BackupEntry:
    def __init__(self, name, directory, compressionType):
        self.name = name
        self.directory = directory
        self.compressionType = compressionType

    def getName(self):
        return self.name

    def getDirectory(self):
        return self.directory

    def getCompressionType(self):
        return self.compressionType

    def getFilenameExtension(self):
        if self.compressionType == 'tar':
            return '.tar'
        elif self.compressionType == 'gz':
            return '.tar.gz'
        elif self.compressionType == 'bz2':
            return '.tar.bz2'
        elif self.compressionType == 'xz':
            return '.tar.xz'
        else:
            raise InvalidCompressionException



class NoConfigFileException(Exception):
    pass

class NoDefaultSectionException(Exception):
    pass

class NoBackupDirectoryException(Exception):
    pass

class NoRecoveryDirectoryException(Exception):
    pass

class NoLogFileException(Exception):
    pass

class InvalidSectionException(Exception):
    pass

class InvalidDirectoryException(Exception):
    pass

class InvalidCompressionException(Exception):
    pass

class NoEntrySectionException(Exception):
    pass
