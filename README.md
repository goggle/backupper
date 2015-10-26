# Backupper

Backupper is a backup program written in Python 3. It's for people who want to have an easy way to have regular backups of certain directories, rather than the whole system. It supports full backups and incremental backups. Backupper has only been tested on Linux.

## Installation

Backupper comes with a distutils setup script. Just run
```
python setup.py --optimize=1
```

Backupper depends on python 3 and GNU tar (https://www.gnu.org/software/tar/), so make sure that you have these programs installed. Optional dependencies are gzip, bzip2 and xz, if you want to use compression, and systemd, if you want to use the provided systemd timer.

Arch Linux users can install backupper from the AUR: https://aur.archlinux.org/packages/backupper/
It also installs the systemd timer files, so you just need to activate "backupper-daily.timer", if you want to use it.


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

After having configured backupper, it is ready to use. Before being able to make incremental backups, we need to have a full backup of our directories. To let backupper perform a full backup, run 
```
backupper -f
```
or 
```
backupper --full-backup
```
Backupper will store the backups in the specified backup directory from the configuration file. It also stores a snapshot file there, where the file changes will be tracked.


From now on, we can let backupper create incremental backups, so only the changes from the previous available backup will be stored. To do this, run
```
backupper -i
```
or
```
backupper --incremental-backup
```
If you want to have automatically incremental backups, you can either run "backupper --incremental-backup" from a cronjob or use the provided systemd timer. See also the next section.


If you need to recover a backup, run
```
backupper -x
```
or 
```
backupper --recover
```
It will recover the newest saved backups into the specified recovery directory from the configuration file.
If you want to recover a backup only up to a certain date, you can run
```
backupper --partial-recover-to-date backup_entry date
```
where "backup_entry" is a specified entry in the configuration file and "date" is in the form year-month-day-hour:minute:second. For example, if we want to recover our "Documents" from the configuration file above up to Monday, October 26, 2015, 22:30, we would run
```
backupper --partial-recover-to-date Documents 2015-10-26-22:30:00
```


If you have several full backups stored and want to remove all the backups before the newest stored full backup, run 
```
backupper -r
```
or 
```
backupper --remove
```

### Systemd timers
Backupper provides a systemd timer to have a daily incremental backup. To use this, copy the provided systemd timer (timers/backupper-daily.timer) and systemd service file (timer/backupper-daily.service) to systemd service file path on your system (usually /etc/systemd/system/) and run 
```
systemctl enable backupper-daily.timer
```

### Logging
Backupper uses a log file specified in the configurations, to log all its activities. It's recommended to regularly check this log file for warnings and error, to make sure that everything works fine.


## General Recommodations
* Before using backupper, test if it works fine for you. Create a full backup of some stuff, edit/add/remove some files, create some incremental backups and recover the backups. Try also to recover to a certain date.
* Store your backups on another physical disk than your data. Otherwise, the backup is useless!
* Make sure that the user who runs backupper has the appropriate permissions for all the directories, which backupper accesses. So if for example you want to backup the whole /etc directory, backupper might need to run as root. Errors including permission problems are not caught yet!

