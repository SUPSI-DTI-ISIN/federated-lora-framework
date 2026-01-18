#!/bin/sh

set -e

echo "Waiting for MinIO to be ready..."
until (/usr/bin/mc alias set myminio "$MINIO_SERVICE_URL" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"); do
  echo "Waiting for MinIO to come online..."
  sleep 2
done

echo "Creating bucket: flow-bucket"
/usr/bin/mc mb myminio/flow-bucket || echo "Bucket already exists"

cat > /tmp/flow-data-rw.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
      "Resource": ["arn:aws:s3:::flow-bucket/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::flow-bucket"]
    }
  ]
}
EOF

echo "Creating policy: flow-data-rw"
/usr/bin/mc admin policy create myminio flow-data-rw /tmp/flow-data-rw.json || echo "Policy already exists"

echo "Creating user: $AWS_ACCESS_KEY_ID"
/usr/bin/mc admin user add myminio "$AWS_ACCESS_KEY_ID" "$AWS_SECRET_ACCESS_KEY" || echo "User already exists"

echo "Attaching policy to user $AWS_ACCESS_KEY_ID"
/usr/bin/mc admin policy attach myminio flow-data-rw --user="$AWS_ACCESS_KEY_ID" || echo "Policy already attached to user"

echo "All setup tasks completed successfully!"