LOAD DATA OVERWRITE `poliquant.source.m_representatives`
FROM FILES (
  format = 'CSV',
  uris = ['gs://poliquant/data/politician_list/representatives_master.csv'])
  ;

