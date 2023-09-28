import csv
import mysql.connector

# Open the CSV file
with open('Data\chunk.csv', 'r', encoding='utf-8') as csvfile:

    # Create a reader object
    reader = csv.reader(csvfile, delimiter=',')

    # Skip header
    next(reader, None)

    # Iterate over the rows in the CSV file
    for row in reader:

        # Create a connection to the MySQL database
        conn = mysql.connector.connect(host="localhost", port='3306', user="root", password='Karan@786', database='levo_transport')
        cursor = conn.cursor()

        # Storing the values of cell into the local variables
        geographic_region = row[0].strip()
        licence_number = row[1].strip()
        licence_type = row[2].strip()
        operator_name = row[3].strip()
        operator_type = row[4].strip()
        correspondence_address = row[5].strip()
        OCAddress = row[6].strip()
        transport_manager = row[7].strip()
        number_of_vehicles_authorised = row[8].strip()
        number_of_trailers_authorised = row[9].strip()
        vehicles_specified = row[10].strip()
        trailers_specified = row[11].strip()
        director_or_partner = row[12].strip()
        license_status = row[13].strip()
        continuation_date = row[14].strip()
        company_reg_number = row[15].strip()

        ###################################### geographicregionmaster ###################################
        # Check if the value exists in the geographicregionmaster table
        cursor.execute('SELECT ID FROM geographicregionmaster WHERE Name = %s', (geographic_region,))
        result = cursor.fetchone()

        # If the value does not exist, insert it into the table & get the latest inserted primary key.
        if result is None:
            cursor.execute('INSERT INTO geographicregionmaster (Name) VALUES (%s)', (geographic_region,))
            conn.commit()
            geographic_region = cursor.lastrowid
           
        else:
            geographic_region = result[0]
        ###################################### geographicregionmaster - ENDS ############################
   
        ###################################### licence_type_master ######################################
        cursor.execute('SELECT ID FROM licence_type_master WHERE Name = %s', (licence_type,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO licence_type_master (Name) VALUES (%s)', (licence_type,))
            conn.commit()
            licence_type = cursor.lastrowid
            
        else:
            licence_type = result[0]
        ###################################### licence_type_master - ENDS ###############################

        ###################################### licence_status_master ####################################
        cursor.execute('SELECT ID FROM license_status_master WHERE Name = %s', (license_status,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO license_status_master (Name) VALUES (%s)', (license_status,))
            conn.commit()
            license_status = cursor.lastrowid
        else:
            license_status = result[0]
        
        ###################################### license_status_master - ENDS #############################

        ###################################### operatormaster ###########################################
        cursor.execute('SELECT ID FROM operatormaster WHERE Name = %s', (operator_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO operatormaster (Name, Operator_Type, Correspodence_Address, OCAddress, Company_Reg_No) VALUES (%s, %s, %s, %s, %s)', (operator_name, operator_type, correspondence_address, OCAddress, company_reg_number,))
            conn.commit()
            operator_name = cursor.lastrowid
        else:
            operator_name = result[0]
        ###################################### operatormaster - ENDS ####################################

        ###################################### operator_user ############################################
        if director_or_partner:
            parts = director_or_partner.split("(", 1)
            name_part = parts[0].strip()
            role_part = parts[1].rstrip(")").strip()

        cursor.execute('SELECT ID FROM operator_user WHERE Name = %s AND Role = %s AND FK_Operator_Master = %s', (name_part, role_part, operator_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO operator_user (Name, Role, FK_Operator_Master) VALUES (%s, %s, %s)', (name_part, role_part, operator_name,))
            conn.commit()
            name_part = cursor.lastrowid
        else:
            name_part = result[0]
        ###################################### operator_user - ENDS #####################################
   
        ###################################### licence_details ##########################################
        cursor.execute('INSERT INTO licence_details (licence_number, Transport_Manager, Number_Of_Vehicles_Authorised, Number_Of_Trailers_Authorised, Vehicles_Specified, Trailers_Specified, Continuation_Date, FK_Geographic_Region, FK_Licence_Type, FK_License_Status, FK_Operator_User, FK_Operator_Master) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (licence_number, transport_manager, number_of_vehicles_authorised, number_of_trailers_authorised, vehicles_specified, trailers_specified, continuation_date, geographic_region, licence_type, license_status, name_part, operator_name,))
        conn.commit()
        ###################################### licence_details - ENDS ###################################

        # Close the cursor object
        cursor.close()

        # Close the connection to the MySQL database
        conn.close()