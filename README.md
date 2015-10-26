# Backupper

Backupper is a backup program written in python 3. It's for people who want to have an easy way to have regular backups of certain directories, rather than the whole system. It supports full backups and incremental backups. Backupper has only been tested on Linux.

## Installation

Backupper comes with a distutils setup script. Just run
```
python setup.py --optimize=1
```

Backupper depends on python 3 and Gnu tar (https://www.gnu.org/software/tar/), so make sure that you have these programs installed. Optional dependencies are gzip, bzip2 and xz, if you want to use compression.


## Configuration

Backupper can be configured through through a config file called backupper.conf. This config file can be stored either globally in /etc/backupper.conf or locally /home/user/.config/backupper.conf. If both files exist, the local version has precedence.

A config file might look like this:
```
[Default]
BackupDirectory = /mnt/second_harddisk/backup
RecoveryDirectory = /mnt/second_harddisk/
LogFile = /var/log/backupper.log

[Documents]
Directory = /home/goggle/Documents
Compression = xz

[Music]
Directory = /home/goggle/Photos
Compression = tar

[Data]
Directory = /home/goggle/data
Compression = bz2

[Projects]
Directory = /home/goggle/projects
Compression = gz
```

Each config file needs to have a [Default] section, where the global configuration options are set. The variable "BackupDirectory" specifies a path to a directory, where the backups are saved. The variable "RecoveryDirectory" must be set to a directory, where to backups are extracted. The "LogFile" variable specifies a log file to log the output of the backupper program.

For each directory that should be backed up, create a new [BackupName] entry. Set the "Directory" variable to the path of the directory to back up and choose a compression type stored in the "Compression" variable. Valid compression types are "tar" for no compression (it creates only a .tar file), "gz" or "gzip" for gzip compression (it creates a .tar.gz file), "bz2" or "bzip2" for bzip2 compression (it creates a .tar.bz2 file) and "xz" for xz compression (it creates a .tar.xz file).

## Usage
