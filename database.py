import psycopg2

def postgresql_connection():
  con = psycopg2.connect(
    database="test",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
  )


con = psycopg2.connect(
  database="NEFAZ",
  user="postgres",
  password="postgres",
  host="localhost",
  port="5432"
)

cur = con.cursor()

# cur.execute("""CREATE TABLE New_January (
#             id SERIAL PRIMARY KEY,
#             model_id INT,
#             plan_id INT,
#             assembly_day INT,
#             assembly_month INT,
#             welding_day INT,
#             welding_month INT,
#             change_id INT,
#             FOREIGN KEY (model_id) REFERENCES model_directory (id),
#             FOREIGN KEY (plan_id) REFERENCES User_Directory (id),
#             FOREIGN KEY (change_id) REFERENCES User_Directory (id));""")

# cur.execute("""CREATE TABLE model_directory (
#               id SERIAL PRIMARY KEY,
#               model VARCHAR(255) PRIMARY KEY);
#             """)

# model_id = int(input())
# plan_id = int(input())
# assembly_day = int(input())
# assembly_month = int(input())
# welding_day = int(input())
# welding_month = int(input())
# change_id = int(input())
#
#
# cur.execute("""insert into new_january (model_id, plan_id, assembly_day, assembly_month, welding_day, welding_month, change_id) values (%s,%s,%s,%s,%s,%s,%s)""", (model_id, plan_id, assembly_day, assembly_month, welding_day, welding_month, change_id))

cur.execute("""CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            user_name VARCHAR(255),
            password VARCHAR(255))""")

con.commit()


