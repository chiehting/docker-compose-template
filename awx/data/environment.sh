DATABASE_USER=awx
DATABASE_NAME=awx
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_PASSWORD=awxpass
AWX_ADMIN_USER=admin
AWX_ADMIN_PASSWORD=password

# Install packages
ansible-galaxy collection install kubernetes.core
