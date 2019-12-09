import traceback

LATEST_USER_VERSION = 2

from . import botDB

def getCurrentVersion():
    with botDB.Database() as db:
        return db.execute("PRAGMA user_version;").fetchone()[0]

def checkAndRunMigration():
    with botDB.Database() as db:
        try:
            currentVersion = getCurrentVersion()
            db.execute("BEGIN TRANSACTION;") # Incase of error during migration can rollback

            while currentVersion != LATEST_USER_VERSION:
                if currentVersion == 0: # Migrate from v0 to v1
                    # Changes
                    db.execute('CREATE TABLE DailyMemberCountStats(Date text NOT NULL UNIQUE PRIMARY KEY, MemberCount integer NOT NULL);')
                    
                    #Update Version
                    db.execute('PRAGMA user_version = 1;')
                    currentVersion = 1
                if currentVersion == 1:
                    # Changes
                    db.execute('CREATE TABLE fancyStats(statType text NOT NULL UNIQUE PRIMARY KEY, enabled integer NOT NULL CHECK(enabled IN (0,1)), channelID integer DEFAULT NULL);')
                    db.execute('INSERT INTO fancyStats (statType, enabled) VALUES("Member Count", 0);')
                    db.execute('INSERT INTO fancyStats (statType, enabled) VALUES("Channel Count", 0);')

                    # Update Version
                    db.execute('PRAGMA user_version = 2;')
                    currentVersion = 2

        except:
            db.execute("ROLLBACK;") # Rollback any changes to last known good state before transactions started
            print("Error with Database Migration: \n" + traceback.format_exc())

            
