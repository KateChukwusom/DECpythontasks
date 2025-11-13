"""--We import these modules, we import psycopg2 library which allows python to connect to and talk to a postgresql database, we need it to interact with our
 webformdatabase.
-- We import RealDictCursor, it makes each row from the database return as a dictionary instead of a tuple and also makes  it
easier to mapfields to jira.
--  The utils directory has the log_setup python file that imports custom get_logger function, which configures
logging for the module(each module has it's own log file).
--Import config, this imports config.py file which reads .env variables to ensure
no hardcoded passwords
---Import sqlite3 t read from the local tracker sqlite database to find last processed date"""


import psycopg2
from psycopg2.extras import RealDictCursor
from jira_autopackage.utils.log_setup import get_logger
from jira_autopackage.utils import config
import sqlite3
import time


""" This creates a logger named "fetch_records", everything this module logs goes to the logs/fetch_records.log file"""
logger = get_logger("Fetch_records")



def get_last_processed_date():
    """This function reads the latest processed submitted_date from the SQLIte database tracker,
    this tells us where to continue batch processing."""

    try:
        conn = sqlite3.connect("tracker/tracker.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(createdat) FROM processed_records;")
        result = cursor.fetchone()[0]
        conn.close()

        if result:
            logger.info(f"last processed date: {result}")
            return result
        logger.warning("No processed date found")
        return None
    except Exception as e:
        logger.error(f"Error:{e}")
        return None

def fetch_records(batch_size=30):
    """
    -- Fetch a batch of submissions incrementally from the webform postgres database
    -- Credentials come from the .env via config.py
    -- check if database exists
    -- check if table has data
    -- fetch the next 30 records 
    -- Returns a list of dictionaries
    """

    #This 'conn' variable hold a resource later or remain none if the creation fails and the last_processed_date reads tracker state to know where to continue
    last_processed_date = get_last_processed_date()
    conn = None
    #Create a connection to the postgres, load credentials from .env using config.py
    try:
        conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )

        logger.info("Connected to webform database successfully")

        #create cursor object and use the special cursor to return each row as a dictionary, the query variable pulls all rows using cursor and sends to the database
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT COUNT(*) FROM phonerequest;")
        total_rows = cursor.fetchone()["count"]

        #Retrieves all rows from the cursor, if count is zero, log a warning and return an empty list--nothing to process


        if total_rows == 0:
            logger.warning("Database exists but contains no records")
            return []
        """Incremental/first run query:If last processed date exists, we fetch only rows submitted after that date 
        to ensure incremental load. if no last date, we fetch the earliest batch size rows ordered ascending"""
        if last_processed_date:
            query = """
			SELECT newusername, samplename, phonenumber, departmentname, job, emailaddress,
                        costcenter, telephonelinesandinstallations, handsetsandheadsets, timeframe,
                        dateneededby, approximateendingdate, "Comments", createdat FROM phonerequest
			WHERE createdat > %s
			ORDER BY createdat ASC
			LIMIT %s;
		"""

            params = (last_processed_date, batch_size)
        else:
            query = """
			SELECT newusername, samplename, phonenumber, departmentname, job, emailaddress,
			costcenter, telephonelinesandinstallations, handsetsandheadsets, timeframe, dateneededby,
			approximateendingdate, "Comments", createdat
			FROM phonerequest
			ORDER BY createdat ASC
			LIMIT %s;
			"""
            params = (batch_size,)



        cursor.execute(query,params)
        rows = cursor.fetchall()
        records = [dict(row) for row in rows]

        logger.info(f"Batch Fetched: {len(records)} records.")

        if not records:
            logger.info("No new records available for batch processing")
            return []

        return records
    except Exception as e:
        logger.error(f"Error fetching records from data base: {e}")
#In case of error, it returns an empty list instead of crashing the pipeline
        return []

    finally:
        if conn:
            conn.close()
            logger.info("Webform database connection closed")
