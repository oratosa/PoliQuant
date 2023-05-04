drop table if exists `poliquant.source.m_representatives`
;
create table `poliquant.source.m_representatives` (
    profileURL STRING OPTIONS(description="Profile website"),
    name STRING OPTIONS(description="Kanji name"),
    furigana STRING OPTIONS(description="furigana name"),
    party STRING OPTIONS(description="Political party"),
    district STRING OPTIONS(description="Electoral district"),
    elected_times INT64 OPTIONS(description="Elected times")
)
;