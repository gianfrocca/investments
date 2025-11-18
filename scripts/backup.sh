#!/bin/bash

# Investment Tracker Backup Script
# This script creates automated backups of the PostgreSQL database

set -e

BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/investment_backup_$TIMESTAMP.sql"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

echo "Starting backup at $(date)"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform database backup
PGPASSWORD=$POSTGRES_PASSWORD pg_dump \
    -h db \
    -U $POSTGRES_USER \
    -d $POSTGRES_DB \
    -F c \
    -f $BACKUP_FILE

# Compress backup
gzip $BACKUP_FILE

echo "Backup completed: ${BACKUP_FILE}.gz"

# Remove old backups
find $BACKUP_DIR -name "investment_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Old backups cleaned up (retention: $RETENTION_DAYS days)"
echo "Backup completed successfully at $(date)"

# Optional: Send backup to remote storage (uncomment and configure)
# Example: AWS S3
# aws s3 cp ${BACKUP_FILE}.gz s3://your-bucket/backups/

# Example: Rsync to remote server
# rsync -avz ${BACKUP_FILE}.gz user@remote-server:/path/to/backups/
