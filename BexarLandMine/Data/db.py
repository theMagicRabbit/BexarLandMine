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
        def wrapper(*args, **kwargs):
            sql, cur = query_formatter(*args, **kwargs)
            return cur.execute(sql)
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
        return query, cur

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
        return query, cur

    @_db_executer
    def _create_amounts_table(self, cur: sqlite3.Cursor):
        query = """CREATE TABLE IF NOT EXISTS amounts(
                account_number INTEGER CONSTRAINT fk_amounts_account_number REFERENCES account(account_number),
                amount_year INTEGER,
                amount_cent_year_tax_levy INTEGER,
                amount_cent_year_amount_due INTEGER,
                amount_cent_prior_years_due INTEGER,
                amount_cent_last_amount_paid INTEGER,
                amount_cent_total_market_value INTEGER,
                amount_cent_land_value INTEGER,
                amount_cent_improvement_value INTEGER,
                amount_cent_capped_value INTEGER,
                amount_cent_ag_value INTEGER,
                CONSTRAINT pk_amounts PRIMARY KEY (account_number, amount_year)
                );"""
        return query, cur

    def __repr__(self):
        return f"DB({self._db_file})"
