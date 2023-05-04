LOAD DATA OVERWRITE `poliquant.source.m_counsilors`
FROM FILES (
  format = 'CSV',
  uris = ['gs://poliquant/data/politician_list/counsilors_master.csv'])
  ;

