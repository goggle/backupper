#!/usr/bin/env python
from utils import Organizer
from backup import Backup

if __name__ == '__main__':
    organizer = Organizer()
    backup = Backup(organizer)
    backup.performIncrementalBackup()
    
