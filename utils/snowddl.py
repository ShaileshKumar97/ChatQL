import pandas as pd


class Snowddl:
    """
    Snowddl class loads DDL files for various tables in a database.
    
    Attributes:
        ddl_dict (dict): dictionary of DDL files for various tables in a database.
        
    Methods:
        load_ddls: loads DDL files for various tables in a database.
    """

    def __init__(self):
        self.ddl_dict = self.load_ddls()

    @staticmethod
    def load_ddls():
        ddl_files = {
            "CUSTOMER": "sql/ddl_customer.csv",
            "LINEITEM": "sql/ddl_lineitem.csv",
            "NATION": "sql/ddl_nation.csv",
            "ORDERS": "sql/ddl_orders.csv",
            "PARTS": "sql/ddl_part.csv",
            "PARTSUPP": "sql/ddl_partsupp.csv",
            "REGION": "sql/ddl_region.csv",
            "SUPPLIER": "sql/ddl_supplier.csv",
        }

        return {
            table_name: pd.read_csv(file_name, index_col=None)
            for table_name, file_name in ddl_files.items()
        }
