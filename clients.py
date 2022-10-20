import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        #создание таблиц Clients и Phones
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Clients (
                    id SERIAL       PRIMARY KEY, 
                    first_name      VARCHAR(40) NOT NULL,
                    last_name       VARCHAR(40) NOT NULL,
                    e_mail          VARCHAR(40) NOT NULL
                    );
                    """)

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS Phones (
                    id SERIAL       PRIMARY KEY,
                    phone_number    CHAR(11),
                    client_id       INTEGER
                                    REFERENCES Clients(id)
                    );
                    """)

        conn.commit()


def add_client(conn, first_name='Name', last_name='Surname', e_mail='email', phone_number=None):
    with conn.cursor() as cur:
        # добавление клиента в Clients
        cur.execute("""
                    INSERT INTO Clients (first_name, last_name, e_mail)
                    VALUES (%s, %s, %s) RETURNING id;
                    """,   (first_name, last_name, e_mail))

        client_id = cur.fetchone()[0]        

        cur.execute("""
                    INSERT INTO Phones (phone_number, client_id)
                    VALUES (%s, %s) RETURNING id; 
                    """,   (phone_number, client_id))

        conn.commit()


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        # обновление номера телефона в Phones
        cur.execute("""
                    UPDATE Phones 
                       SET phone_number=%s CHAR(11)
                     WHERE id=%s;
                    """,   (phone_number, client_id))

        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, e_mail=None, phone_number=None):
    with conn.cursor() as cur:
        # обновление данных в Clients
        cur.execute("""
                    UPDATE Clients 
                       SET first_name=%s VARCHAR(40), last_name=%s VARCHAR(40), e_mail=%s VARCHAR(40)
                     WHERE id=%s;
                    """,   (first_name, last_name, e_mail, client_id))
        
        conn.commit()

        cur.execute("""
                    UPDATE Phones 
                       SET phone_number=%s
                     WHERE id=%s;
                    """,   (phone_number, client_id))

        conn.commit()


def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        # удаление телефона из Phones
        cur.execute("""
                    DELETE FROM Phones
                     WHERE id=%s
                       AND phone_number=%s;
                    """,   (client_id, phone_number))

        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        # удаление клиента из Clients и Phones
        cur.execute(""" 
                    DELETE FROM Phones
                     WHERE id=%s;
                    """,   (client_id,))

        conn.commit()

        cur.execute(""" 
                    DELETE FROM Clients
                     WHERE id=%s;
                    """,   (client_id,))
        
        conn.commit()


def find_client(conn, first_name=None, last_name=None, e_mail=None, phone_number=None):
    # поиск клиента по имени/фамилии/поче/телефону в Clients и Phones
    with conn.cursor() as cur:
        cur.execute("""
                    SELECT * 
                      FROM Clients as c
                           LEFT JOIN Phones as p
                           ON c.id = p.client_id
                     WHERE first_name=%s
                        OR last_name=%s
                        OR e_mail=%s
                        OR phone_number=%s
                    """,   (first_name, last_name, e_mail, phone_number))

        return cur.fetchall()
        

if __name__ == "__main__":
    with psycopg2.connect(database='clients_db', user='postgres', password='SN33Vf8m') as conn:
        create_db(conn)
        # add_client(conn, first_name='Name', last_name='Surname', e_mail='email', phone_number='89577598244')
        # add_client(conn, first_name='Name2', last_name='Surname2', e_mail='email2', phone_number='89577598245')
        # add_phone(conn, 1, '89576545244')
        # change_client(conn, 1, first_name='Name3', last_name='Surname3', e_mail='email3', phone_number=85973245245)
        # delete_phone(conn, 1, 89577598244)
        # delete_client(conn, 2)
        # print(find_client(conn, first_name=None, last_name=None, e_mail=None, phone_number='85973245245'))

    conn.close()