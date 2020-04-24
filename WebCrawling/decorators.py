# Decorators
import re
import logging
<<<<<<< HEAD
<<<<<<< HEAD

logger = logging.getLogger('run_log')

=======
import database

logger = logging.getLogger('run_log')

temp_db = database.CasaDB()

>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
import database

logger = logging.getLogger('run_log')

temp_db = database.CasaDB()

>>>>>>> upstream/master
def clean_address(address):
    addr = address.split(' ')[0:3]
    province, district, state  = addr[0], addr[1], addr[2]
    return province, district, state

def clean_apartment(func_apartment):
    def inner_function(*args, **kwargs):
        apartment_info = func_apartment(*args, **kwargs)

        clean_build = re.findall(r'[0-9]+', apartment_info[0])
        clean_floor = apartment_info[2].replace('층','').split('/')
        clean_parking = apartment_info[4].replace('대', '')

        # TODO: int conversion
        apartment_build_year = clean_build[0]
        apartment_build_month = clean_build[1]
        apartment_floor_min = clean_floor[0]
        apartment_floor_max = clean_floor[1]

        apartment_addr_province, apartment_addr_district, apartment_addr_town = clean_address(apartment_info[3])
        apartment_builder = apartment_info[1]
        if clean_parking == '-':
<<<<<<< HEAD
<<<<<<< HEAD
            apartment_parking = ''
=======
            apartment_parking = 0.0
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
            apartment_parking = 0.0
>>>>>>> upstream/master
        else:
            apartment_parking = clean_parking

        logger.debug('apartment_builder: ' + apartment_builder)
        logger.debug('apartment_build_year: ' + apartment_build_year)
        logger.debug('apartment_build_month: ' + apartment_build_month)
        logger.debug('apartment_floor_min: ' + apartment_floor_min)
        logger.debug('apartment_floor_max: ' + apartment_floor_max)
        logger.debug('apartment_addr_province: ' + apartment_addr_province)
        logger.debug('apartment_addr_district: ' + apartment_addr_district)
        logger.debug('apartment_addr_town: ' + apartment_addr_town)
<<<<<<< HEAD
<<<<<<< HEAD
        logger.debug('apartment_parking: ' + apartment_parking)

        apartment_dict = {'apartment_builder': apartment_builder,
=======
        logger.debug('apartment_parking: ' + str(apartment_parking))

        apartment_dict = {'apartment_addr_town': apartment_addr_town,
                          'apartment_builder': apartment_builder,
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
        logger.debug('apartment_parking: ' + str(apartment_parking))

        apartment_dict = {'apartment_addr_town': apartment_addr_town,
                          'apartment_builder': apartment_builder,
>>>>>>> upstream/master
                          'apartment_build_year': apartment_build_year,
                          'apartment_build_month': apartment_build_month,
                          'apartment_floor_min': apartment_floor_min,
                          'apartment_floor_max': apartment_floor_max,
<<<<<<< HEAD
<<<<<<< HEAD
                          'apartment_addr_province': apartment_addr_province,
                          'apartment_addr_district': apartment_addr_district,
                          'apartment_addr_town': apartment_addr_town,
                          'apartment_parking': apartment_parking}

        return apartment_dict
=======
                          'apartment_parking': apartment_parking}

        return apartment_addr_district, apartment_dict
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
                          'apartment_parking': apartment_parking}

        return apartment_addr_district, apartment_dict
>>>>>>> upstream/master
    return inner_function

def clean_school(func_school):
    def innner_function(*args, **kwargs):
        school_info = func_school(*args, **kwargs)

        if school_info is False:
            school_dict = {'school_name': '',
<<<<<<< HEAD
<<<<<<< HEAD
                           'school_dist': '',
                           'school_addr_province': '',
                           'school_addr_district': '',
=======
                           'school_dist': 0,
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
                           'school_dist': 0,
>>>>>>> upstream/master
                           'school_addr_town': '',
                           'school_students': ''}
            return school_dict

        clean_students = school_info[3].split('명')[0]

        clean_time = re.search(r'[0-9]+', school_info[1])
        time_intv = clean_time.span()[0]
        time_state = re.findall(r'[가-하]', school_info[1][time_intv:])
        if time_state == '시간':
            time = (clean_time.group()) * 60
            school_dist = str(time)
        else:
            school_dist = clean_time.group()

        school_name = school_info[0]
        school_students = re.sub(r'[^\w]', '', clean_students)
        school_addr_province, school_addr_district, school_addr_town = clean_address(school_info[2])

        logger.debug('school_name: ' + school_name)
        logger.debug('school_dist: ' + school_dist)
        logger.debug('school_addr_province: ' + school_addr_province)
        logger.debug('school_addr_district: ' + school_addr_district)
        logger.debug('school_addr_town: ' + school_addr_town)
        logger.debug('school_students: ' + school_students)

        school_dict = {'school_name': school_name,
<<<<<<< HEAD
<<<<<<< HEAD
                       'school_dist': school_dist,
                       'school_addr_province': school_addr_province,
                       'school_addr_district': school_addr_district,
=======
                       'school_dist': int(school_dist),
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
                       'school_dist': int(school_dist),
>>>>>>> upstream/master
                       'school_addr_town': school_addr_town,
                       'school_students': school_students}

        return school_dict
    return innner_function


def clean_tower(func_tower):
    def inner_function(*args, **kwargs):
        # id, name, bathroom, floor, area, household, floor_mx
        tower_info = func_tower(*args, **kwargs)

        if tower_info is False:
            return False

        clean_bathroom = tower_info[2].replace('개', '').split('/')

        tower_id = int(tower_info[0])
        tower_name = tower_info[1]
        tower_bathroom = clean_bathroom[0]
        tower_shower = clean_bathroom[1]
        tower_size = tower_info[4]
        tower_household = re.search(r'[0-9]+', tower_info[5]).group()

        logger.debug('tower_id: ' + str(tower_id))
        logger.debug('tower_name: ' + tower_name)
        logger.debug('tower_bathroom: ' + tower_bathroom)
        logger.debug('tower_shower: ' + tower_shower)
        logger.debug('tower_size: ' + tower_size)
        logger.debug('tower_household: ' + tower_household)

        return tower_id, tower_name, tower_bathroom, tower_shower, tower_size, tower_household
    return inner_function

def clean_price(func_price):
    def inner_function(*args, **kwargs):
        if func_price(*args, **kwargs) is False:
            return False

        price_period, price_amount, temp_id, temp_area = func_price(*args, **kwargs)

        result = {'apartment_id': [],
                  'area': [],
                  'period': [],
                  'year': [],
                  'month': [],
                  'amount_original' : [],
                  'amount': []}

        price_intv = {'천': 10000000, '억': 100000000}

        for idx, period in enumerate(price_period):
<<<<<<< HEAD
<<<<<<< HEAD
=======
            result = {}
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
            result = {}
>>>>>>> upstream/master
            clean_period = period.split('.')
            price_year = clean_period[0]
            price_month = clean_period[1]

            amount = price_amount[idx]
            amount_value = amount[:amount.find('(')]
            clean_amount = re.sub(r'[^\w]', '', amount_value)

            try:
                lim = re.search(r'[가-흐]', clean_amount).group()
            except AttributeError:
                lim = False

            if lim is not False and lim in price_intv:
<<<<<<< HEAD
<<<<<<< HEAD
                decimal = float(clean_amount.replace(lim, '.'))
=======
=======
>>>>>>> upstream/master
                amount_replace = clean_amount.replace(lim, '.')
                temp_idx = amount_replace.find('.')
                temp_check = len(amount_replace[temp_idx+1:])
                if temp_check == 3:
                    decimal = float(amount_replace[:temp_idx+1] + '0' + amount_replace[temp_idx+1:])
                else:
                    decimal = float(clean_amount.replace(lim, '.'))

<<<<<<< HEAD
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
>>>>>>> upstream/master
                final_amount = int(price_intv[lim] * decimal)
            else:
                try:
                    decimal = float(amount_value.replace(',', '.'))
                    final_amount = int(10000000 * decimal)
                except:
                    final_amount  = 0

<<<<<<< HEAD
<<<<<<< HEAD
            result['apartment_id'].append(temp_id)
            result['area'].append(temp_area)
            result['period'].append(period)
            result['year'].append(int(price_year))
            result['month'].append(int(price_month))
            result['amount_original'].append(amount_value)
            result['amount'].append(final_amount)
=======
=======
>>>>>>> upstream/master

            result['apartment_id'] = temp_id
            result['area'] = temp_area
            result['period'] = period
            result['year'] = int(price_year)
            result['month'] = int(price_month)
            result['amount'] = final_amount
            result['amount_original'] = amount_value

            select_price = temp_db.db_insert(type='price')
            temp_db.db_execute(select_price, type='insert', data=result)
<<<<<<< HEAD
>>>>>>> 6ac1fb8afdeb6bacad6f957a1aff4f79b0921535
=======
>>>>>>> upstream/master

        return result
    return inner_function