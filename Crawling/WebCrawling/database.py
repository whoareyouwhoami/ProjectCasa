## Database connection
import os
import json
import logging
import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger('run_log')

class CasaDB:
    crawling_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(crawling_path, 'credentials/db.json')

    with open(db_path) as db_json:
        req = json.load(db_json)

    def __init__(self, ):
        try:
            self.connection = psycopg2.connect(
                host=self.req['HOST'],
                user=self.req['USER'],
                port=self.req['PORT'],
                database=self.req['DATABASE'],
                password=self.req['PASSWORD'],
            )

            self.connection.autocommit = True
            self.cur = self.connection.cursor(cursor_factory=RealDictCursor)
            # self.cur = self.connection.cursor()

            print("Connected to database")
            logger.debug('Connected to database')

        except Exception as err:
            print("Database connection error")
            logger.error('Database connection error: ')
            logger.error(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def db_insert(self, type, val=None, id=None):
        if type == 'apartment':
            sql = "INSERT INTO crawling_db.apartment_table(district_id, apartment_id, apartment_addr_town, apartment_builder, apartment_build_year, apartment_build_month, apartment_floor_min, apartment_floor_max, apartment_parking) " \
                  "VALUES((SELECT district_id FROM crawling_db.district_table WHERE district_name = '" + val + "'), %(apartment_id)s, %(apartment_addr_town)s, %(apartment_builder)s, %(apartment_build_year)s, %(apartment_build_month)s, %(apartment_floor_min)s, %(apartment_floor_max)s, %(apartment_parking)s);"

        elif type == 'school':
            sql = "INSERT INTO crawling_db.school_table(apartment_id, school_name, school_dist, school_addr_district, school_addr_town, school_students) " \
                  "VALUES(%(apartment_id)s, %(school_name)s, %(school_dist)s, (SELECT district_id FROM crawling_db.district_table WHERE district_name ='" + val + "'), %(school_addr_town)s, %(school_students)s);"

        elif type == 'price':
            sql = "INSERT INTO crawling_db.price_table(apartment_id, area, period, year, month, amount, amount_original)" \
                  "VALUES(%(apartment_id)s, %(area)s, %(period)s, %(year)s, %(month)s, %(amount)s, %(amount_original)s);"
        elif type == 'name':
            sql = "UPDATE crawling_db.apartment_table SET apartment_name = '" + val + "' WHERE apartment_id = '" + id + "';"
        else:
            raise ValueError('Wrong types')

        return sql

    def db_select(self, type, val):
        if type == 'district':
            sql = "SELECT district_id FROM crawling_db.district_table WHERE district_name = '" + val + "';"
        elif type == 'apartment':
            sql = "SELECT table_id FROM crawling_db.apartment_table WHERE apartment_id = '" + val + "';"
        else:
            sql = ""
        return sql

    def db_execute(self, query, type=None, data=None):
        try:
            self.cur.execute(query, data)
        except Exception as err:
            print('Something went wrong. Please try again.')
            print(err)

            logger.error('Error while executing a query')
            logger.error(err)
            return

        if type == 'select':
            result = self.cur.fetchall()
            if not result:
                return False

            return result

    def db_close(self):
        self.connection.close()