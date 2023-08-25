TRUNCATE TABLE `poliquant.source.m_representatives`
;

LOAD DATA INTO `poliquant.source.m_representatives`
(
    profile_url STRING OPTIONS(description="Profile website"),
    name STRING OPTIONS(description="Kanji name"),
    furigana STRING OPTIONS(description="furigana name"),
    party STRING OPTIONS(description="Political party"),
    district STRING OPTIONS(description="Electoral district"),
    elected_times STRING OPTIONS(description="Elected times"),
    as_of_date STRING OPTIONS(description="As of date")
)
FROM FILES (
  format = 'CSV',
  uris = ['gs://poliquant/data/input/politician_list/representative/representatives_master_*.csv']
)
;
