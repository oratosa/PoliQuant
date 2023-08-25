TRUNCATE TABLE `poliquant.source.m_councilors`
;

LOAD DATA INTO `poliquant.source.m_councilors`
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
  uris = ['gs://poliquant/data/input/politician_list/councilor/councilors_master_*.csv']
  )
;
