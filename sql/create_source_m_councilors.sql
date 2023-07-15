DROP TABLE IF EXISTS `poliquant.source.m_councilors`
;
CREATE TABLE `poliquant.source.m_councilors` 
(
    profile_url STRING OPTIONS(description="Profile website"),
    name STRING OPTIONS(description="Kanji name"),
    furigana STRING OPTIONS(description="furigana name"),
    party STRING OPTIONS(description="Political party"),
    district STRING OPTIONS(description="Electoral district"),
    expiration_date STRING OPTIONS(description="Expiration date"),
    session STRING OPTIONS(description="Session")
)
;