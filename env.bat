@echo off
set DATABASE_URL=postgresql://postgres:mainakamau@localhost/apex_db
set DATABASE_TEST_URL=postgresql://postgres:mainakamau@localhost/test_db
set APP_SETTINGS=development
set FLASK_APP=run.py
set SECRET_KEY='84c72df8da901d8e28c0af3f73574c73'
set FLASK_ENV=development