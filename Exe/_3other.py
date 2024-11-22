"""
    ข้อมูลอื่น ๆ ที่ต้องมีข้อมูลจาก step _1 ก่อน
"""
# data lineage
from Script import lineage
lineage.add_lineage_from_yaml("Data/lineage.yaml")

# custom sample data
from Script import sample_data
sample_data.put_sample_data_from_csv('DWH.SetDB.dbo.C2WInvalidData','Data/sample_data/C2WInvalidData.csv')

# assign tag/term to column
from Script import classification
classification.assign_tag_to_column_from_yaml('Data/assign_tag/column_tag.yaml')