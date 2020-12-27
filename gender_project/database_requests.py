# SQLAlchemy
from  sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd

# response on URL like : http://127.0.0.1:5000/count/u10003/B00002
def get_response_on_category_in_session(session_id, category, session):
    result = session.execute(
        "SELECT * FROM (SELECT session_id AS SESSION_ID, category_a AS CATEGORY, count(*) AS COUNT from product GROUP BY session_id, category_a " + \
        "UNION SELECT session_id, category_b, count(*) from product GROUP BY session_id, category_b " + \
        "UNION SELECT session_id, category_c, count(*) from product GROUP BY session_id, category_c " + \
        "UNION SELECT session_id, category_d, count(*) from product GROUP BY session_id, category_d) AS counter " + \
        "WHERE SESSION_ID = :val1 AND CATEGORY = :val2", {'val1': session_id, 'val2': category}).first()

    if result:
        response = {'SESSION_ID': result[0], 'CATEGORY': result[1], 'COUNT': result[2]}
    else:
        response = {'SESSION_ID': session_id, 'CATEGORY': category, 'COUNT': 0}
    return response

# transform table of categories to list categories on session
def get_category_sequence(array):
    #     print(type(array))
    return " ".join([" ".join(row[-4:]) for row in array])

# create vector on session_id
# data is created by SQL requests on 2 tables (session, product)
def create_vector(session_id, session):
    result = []
    categories = session.execute("SELECT * FROM product " + \
                                 "WHERE session_id = :val1", {'val1': session_id}).fetchall()
    time_data = session.execute("SELECT * FROM session " + \
                                "WHERE session_id = :val1", {'val1': session_id}).first()
    if categories and time_data:
        categories = get_category_sequence(categories)
        result.append(time_data[1].day)
        result.append(pd.Timestamp(time_data[1]).dayofweek)
        result.append(time_data[1].hour)
        result.append(categories)
        duration = (time_data[2] - time_data[1]).seconds
        number_of_views = int(len(categories.split()) / 4)
        result.append(number_of_views)
        result.append(duration / number_of_views)
        columns = 'day dayofweek start_hour categories number_of_views average_time_per_view'.split()
        return pd.DataFrame(data=[result], columns=columns)
    else:
        return None

# get response on URL like: http://127.0.0.1:5000/predict/u25000
def get_prediction_response(session_id, session, production_model):
    mapping_answer = {0: 'female', 1: 'male'}
    vector = create_vector(session_id, session)
    if vector is not None:
        prediction = production_model.predict(vector)[0]
        answer = mapping_answer[prediction]
        response = {'SESSION_ID': session_id, 'PREDICTION': answer}
    else:
        response = {'SESSION_ID': session_id, 'PREDICTION': 'UNKNOWN_SESSION_ID'}
    return response
