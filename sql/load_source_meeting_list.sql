LOAD DATA OVERWRITE `poliquant.source.meeting_list`
FROM FILES (
  format = 'JSON',
  uris = ['gs://poliquant/data/meeting_list/*.json'])
  ;
