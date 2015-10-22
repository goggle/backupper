#!/usr/bin/env python
from utils import Organizer
from recover import Recover

if __name__ == '__main__':
    organizer = Organizer()
    recover = Recover(organizer)
    recover.recoverBackupUpToDate()
