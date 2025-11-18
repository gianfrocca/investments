#!/bin/bash

# Investment Tracker Restore Script
# Restore database from backup file

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file>"
    echo "Example: ./restore.sh /backups/investment_backup_20241201_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Warning: This will overwrite the current database!"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Starting restore at $(date)"

# Decompress if gzipped
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c $BACKUP_FILE | PGPASSWORD=$POSTGRES_PASSWORD pg_restore \
        -h db \
        -U $POSTGRES_USER \
        -d $POSTGRES_DB \
        --clean \
        --if-exists
else
    PGPASSWORD=$POSTGRES_PASSWORD pg_restore \
        -h db \
        -U $POSTGRES_USER \
        -d $POSTGRES_DB \
        --clean \
        --if-exists \
        $BACKUP_FILE
fi

echo "Restore completed successfully at $(date)"
