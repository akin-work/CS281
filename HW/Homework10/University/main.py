from Database import Database as DB

if __name__ == "__main__":
    DB.create_database("sports")
    
    DB.drop_database("sports")
    
    with DB() as db:
        db.factory_reset()
        db.show_schema()
        
    # OR 
    db = DB()
    db.factory_reset()
    db.show_schema()
    db.close()
        