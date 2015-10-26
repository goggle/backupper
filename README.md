# Backupper



Example config file:


[Default]
# Specify the directory, where the backups should be stored:
BackupDirectory = /path/to/backup/directory
# Specify the directory, where the recovery should be extracted:
RecoveryDirectory = /path/to/recovery/directory
# Specify the logfile:
LogFile = /path/to/logfile/logfile

# For each directory to backup, specify a entry section of the form [Name]
[ExampleName]
# The directory to backup:
Directory = /path/to/directory
# The compression type. Following options are valid:
# 	tar: No compression, just store the files in a tar archiv.
#	gz or gzip: Use gzip to store the files in a tar.gz archiv.
#	bz2 or bzip2: Use bzip to store the files in a tar.bz2 archiv.
#	xz: Use xz to store the files in a tar.xz archiv.
Compression = gz


