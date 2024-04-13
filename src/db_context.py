import psycopg2
import os
import logging
import sys
from src.prediction_history import PredictionHistory
from dotenv import load_dotenv

class DBContext:
    
    def __init__(self):
        load_dotenv()
        self.connection_string = os.environ["DATABASE_URL"]
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.connection_string)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cur.close()
        self.conn.close()
    
    def open_connection(self):
            """Connect to a Postgres database."""
            try:
                if(self.conn is None):
                    self.conn = psycopg2.connect(self.connection_string)
            except psycopg2.DatabaseError as e:
                logging.error(e)
                sys.exit()
            finally:
                logging.info('Connection opened successfully.')


    def create_history(self, air_temp, 
                    process_temp, 
                    rotational_speed, 
                    torque, 
                    tool_wear, 
                    energy_source, 
                    prediction_type, 
                    confidence_level, 
                    carbon_intensity, 
                    carbon_footprint,
                    run_frequency,
                    label0,
                    label1,
                    label2,
                    label3):
                       
                    
        """Inserts a new history record"""
        with self as cur:
            cur.execute(
                """
                INSERT INTO prediction_history (
                    air_temp, 
                    process_temp, 
                    rotational_speed, 
                    torque, 
                    tool_wear, 
                    energy_source, 
                    prediction_type, 
                    confidence_level, 
                    carbon_intensity, 
                    carbon_footprint,
                    run_frequency,
                    label0,
                    label1,
                    label2,
                    label3
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                RETURNING id
                """,
                (
                    air_temp, 
                    process_temp, 
                    rotational_speed, 
                    torque, 
                    tool_wear, 
                    energy_source, 
                    prediction_type, 
                    confidence_level, 
                    carbon_intensity, 
                    carbon_footprint,
                    run_frequency,
                    label0,
                    label1,
                    label2,
                    label3
                )
            )
            history_id = cur.fetchone()[0]  # Fetch the returned ID
            return history_id

    def find_history_by_id(self, history_id):
        """Finds a device by its primary key ID"""
        with self as cur:
            cur.execute(
                """
                SELECT * FROM prediction_history WHERE id = %s
                """,
                (history_id,)
            )
            return cur.fetchone()  # Might return None if no device is found

    
    def get_all_history(self):
        with self as cur:
            cur.execute("""
            SELECT * FROM prediction_history
            ORDER BY timestamp DESC 
            """)
            return [PredictionHistory(*record) for record in cur.fetchall()]

            