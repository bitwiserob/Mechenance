import psycopg2
import os
import logging
import sys

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


    def create_history(self,air_temp, process_temp, rotational_speed, torque, tool_wear, energy_source, 
                       prediction_type,
                       confidence_level,
                       carbon_intensity,
                       carbon_footprint,
                       
                       ):
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
                    carbon_footprint
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    carbon_footprint
                )
            )
            device_id = cur.fetchone()[0]  # Fetch the returned ID
            return device_id

    def find_device_by_id(self, device_id):
        """Finds a device by its primary key ID"""
        with self as cur:
            cur.execute(
                """
                SELECT * FROM device WHERE id = %s
                """,
                (device_id,)
            )
        return cur.fetchone()  # Might return None if no device is found

    def find_devices_by_type(self, device_type):
        """Finds devices based on their type"""
        with self as cur:
            cur.execute(
                """
                SELECT * FROM device WHERE device_type = %s
                """,
                (device_type,)
            )
            return cur.fetchall()

    def update_device(self, device_id, device_name, mac_address, device_type):
        """Updates an existing device"""
        with self as cur:
            cur.execute(
                """
                UPDATE device
                SET device_name = %s, mac_address = %s, device_type = %s
                WHERE id = %s
                """,
                (device_name, mac_address, device_type, device_id)
            )

    def delete_device(self, device_id):
        """Deletes a device"""
        with self as cur:
            cur.execute(
                """
                DELETE FROM device WHERE id = %s
                """,
                (device_id,)
            )