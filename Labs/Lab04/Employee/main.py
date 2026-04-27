from setup import connect_to_db, create_database, create_tables
from load import load_data, show_tables, get_relation_names
from drop import drop_tables
connc = connect_to_db()

if connc is not None:
    create_database(connc,"employee_db")
    
    connc = connect_to_db("employee_db")

    if connc is not None:
        create_tables(connc)
        rel_name = get_relation_names(connc)
        load_data(connc, rel_name)
        show_tables(connc)
        connc.close()
