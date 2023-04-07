def change_db_creds(db_config):
    db_config.set("username",
                  input("Database username: "))
    db_config.set("password",
                input("Database username: "))