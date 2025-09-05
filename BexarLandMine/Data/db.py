import sqlite3
import os


class DB():
    def __init__(self, db_file: str):
        self._db_file = db_file
        is_new_db = not os.path.isfile(self._db_file)
        self.connection = sqlite3.connect(self._db_file)
        self.connection.setconfig(sqlite3.SQLITE_DBCONFIG_ENABLE_FKEY, True)
        if is_new_db:
            self._create_db_tables()

    def _db_executer(query_formatter):
        def wrapper(self, *args, **kwargs):
            sql, cur, values = query_formatter(self, *args, **kwargs)
            cur.execute(sql, values)
            self.connection.commit()
            return
        return wrapper

    def _create_db_tables(self):
        cur = self.connection.cursor()
        self._create_owner_table(cur)
        self._create_account_table(cur)
        self._create_amounts_table(cur)
        pass

    @_db_executer
    def _create_owner_table(self, cur: sqlite3.Cursor):
        query = """CREATE TABLE IF NOT EXISTS owner(
                id INTEGER PRIMARY KEY,
                owner_name_address TEXT
                );"""
        return query, cur, ()

    @_db_executer
    def _create_account_table(self, cur: sqlite3.Cursor):
        query = """CREATE TABLE IF NOT EXISTS account(
                account_number INTEGER CONSTRAINT pk_account PRIMARY KEY,
                owner_id INTEGER CONSTRAINT fk_account_owner REFERENCES owner(id),
                account_property_address TEXT UNIQUE,
                account_legal_description TEXT UNIQUE,
                account_exemptions TEXT,
                account_jurisdictions TEXT
                );"""
        return query, cur, ()

    @_db_executer
    def _create_amounts_table(self, cur: sqlite3.Cursor):
        query = """CREATE TABLE IF NOT EXISTS amounts(
                account_number INTEGER CONSTRAINT fk_amounts_account_number REFERENCES account(account_number),
                amount_year INTEGER CONSTRAINT nn_amount_year NOT NULL,
                amount_cent_year_tax_levy INTEGER,
                amount_cent_prior_years_due INTEGER,
                amount_cent_last_amount_paid INTEGER,
                amount_cent_total_market_value INTEGER,
                amount_cent_land_value INTEGER,
                amount_cent_improvement_value INTEGER,
                amount_cent_capped_value INTEGER,
                amount_cent_ag_value INTEGER,
                CONSTRAINT pk_amounts PRIMARY KEY (account_number, amount_year)
                );"""
        return query, cur, ()

    @_db_executer
    def get_owner(self, owner_address: str):
        cur = self.connection.cursor()
        query = """SELECT id FROM owner
        WHERE owner_name_address = ? ;"""
        values = (owner_address,)
        return query, cur, values

    @_db_executer
    def add_owner(self, owner_address: str):
        cur = self.connection.cursor()
        query = """INSERT INTO owner (owner_name_address)
        VALUES(?);"""
        values = (owner_address,)
        return query, cur, values

    @_db_executer
    def add_account(self, account_num: int, owner_id: int,
                    property_address: str, legal_description: str,
                    exemptions: str = None, jurisdictions: str = None):
        cur = self.connection.cursor()
        if exemptions:
            exemptions = f"""'{exemptions}'"""
        if jurisdictions:
            jurisdictions = f"""'{jurisdictions}'"""
        query = """INSERT INTO account (
                account_number, owner_id, account_property_address,
                account_legal_description, account_exemptions,
                account_jurisdictions)
        VALUES (?, ?, ?, ?, ?, ?);"""
        values = (account_num, owner_id, property_address, legal_description,
                  exemptions, jurisdictions)
        breakpoint()
        return query, cur, values

    @_db_executer
    def add_amounts(self, account_num: int, amount_year: int,
                    cent_year_tax_levy: int,
                    cent_prior_years_due: int, cent_last_amount_paid: int,
                    cent_total_market_value: int, cent_land_value: int,
                    cent_improvement_value: int, cent_capped_value: int,
                    cent_ag_value: int):
        cur = self.connection.cursor()
        query = """INSERT INTO amounts (
                account_number, amount_year, amount_cent_year_tax_levy,
                amount_cent_prior_years_due,
                amount_cent_last_amount_paid, amount_cent_total_market_value,
                amount_cent_land_value, amount_cent_improvement_value,
                amount_cent_capped_value, amount_cent_ag_value)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
        values = (account_num, amount_year, cent_year_tax_levy,
                  cent_prior_years_due, cent_last_amount_paid,
                  cent_total_market_value, cent_land_value,
                  cent_improvement_value, cent_capped_value, cent_ag_value)
        return query, cur, values

    def __repr__(self): 
        return f"DB({self._db_file})"
