#!/usr/bin/env python
from utils import Organizer
from remove import Remove

if __name__ == '__main__':
    organizer = Organizer()
    remove = Remove(organizer)
    remove.removePreviousBackupCycles()
