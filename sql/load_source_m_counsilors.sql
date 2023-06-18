TRUNCATE TABLE `poliquant.source.m_counsilors`
;

LOAD DATA INTO `poliquant.source.m_counsilors`
(
    profile_url STRING OPTIONS(description="Profile website"),
    name STRING OPTIONS(description="Kanji name"),
    furigana STRING OPTIONS(description="furigana name"),
    party STRING OPTIONS(description="Political party"),
    district STRING OPTIONS(description="Electoral district"),
    expiration_date STRING OPTIONS(description="Expiration date"),
    session STRING OPTIONS(description="Session")
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://poliquant/data/politician_list/counsilors/counsilors_master_*.csv']
  )
;
