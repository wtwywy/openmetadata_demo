"""
    sample data
"""

import connection
from metadata.generated.schema.entity.data.table import TableData
import pandas as pd

from Script import entity

def put_sample_data_from_csv(table_fqn, file_path):
    """
        ตั้ง sample data ให้กับตาราง
        ชื่อไฟล์ไม่จำเป็นต้องเป็นชื่อตาราง
        จะแทนที่ sample data ก่อนหน้าของตาราง
    """
    con = connection.get_connection_obj()
    df = pd.read_csv(file_path, header=0, index_col=False)
    print(df)
    table = entity.get_entity_by_name(table_fqn, 'table')
    data = TableData(
        columns=df.columns,
        rows=df.values.tolist()
    )
    con.ingest_table_sample_data(table, data)
    
