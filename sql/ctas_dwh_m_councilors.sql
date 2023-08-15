drop table if exists `poliquant.dwh.m_councilors`
;

create table `poliquant.dwh.m_councilors` as
select 
  m.profile_url,
  m.name,
  m.furigana,
  case 
    when m.party = "民主" then "国民"
    when m.party = "無所属" then "無"
    else m.party
    end as party,
  d.id as district_id,
  m.district,
  case when d.type = "小選挙区" then "1" --参議院選挙区は各都道府県ごとに1つのため、すべて1とする
    else d.type 
    end as district_detail,
  m.expiration_date,
  cast(m.session as INT64) as session
from `poliquant.source.m_councilors` as m
left join `poliquant.source.m_councilors_district` as d
on m.district = d.district
;