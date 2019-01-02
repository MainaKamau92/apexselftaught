@echo off

set DATABASE_URL=postgresql://postgres:mainakamau@localhost/apex_db
set DATABASE_TEST_URL=postgresql://postgres:mainakamau@localhost/test_db
set SECRET_KEY='c9f130b893249c892bdc589a95cc59c8'
set FLASK_APP=run.py
set FLASK_ENV=development
set APP_SETTINGS=development