DROP TABLE IF EXISTS `poliquant.source.m_representatives`
;
CREATE TABLE `poliquant.source.m_representatives` 
(
    profile_url STRING OPTIONS(description="Profile website"),
    name STRING OPTIONS(description="Kanji name"),
    furigana STRING OPTIONS(description="furigana name"),
    party STRING OPTIONS(description="Political party"),
    district STRING OPTIONS(description="Electoral district"),
    elected_times STRING OPTIONS(description="Elected times")
)
;