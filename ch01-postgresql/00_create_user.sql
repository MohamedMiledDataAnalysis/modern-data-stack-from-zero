-- Run as the postgres superuser: sudo -u postgres psql -f 00_create_user.sql
CREATE USER meridian_user WITH PASSWORD 'meridian2024';
CREATE DATABASE meridian_db OWNER meridian_user;
