from .database import UserFetchFormat,connect_to_localDB,connect_to_rds
from typing import Union

def check_user(phone:str) -> Union[UserFetchFormat, str]:
    """ Fetch User info (name,phone,email,address,city,state,zipcode) if the phone number given by user exists in the db."""
    cursor, conn = connect_to_localDB('user.db')
    query = """
            SELECT 
                name,
                phone,
                email,
                address_line_1,
                address_line_2,
                city,
                state,
                zipcode 
            FROM users 
            WHERE phone = ?
        """
    # Removing extra whitespace and newline characters within the query
    cursor.execute(query, (phone,))
    row = cursor.fetchone()
    conn.close()
    if row:
        result=UserFetchFormat(
            name=row[0],
            phone_number = row[1],
            email_id= row[2],
            address= f"{row[3]} {row[4] if row[4] else ''}",
            city= row[5],
            state= row[6],
            pincode= row[7]
        )
        return result
    else:
        return {"message": "User does not exist"}
