drop table if exists `poliquant.dwh.m_councilors`
;

create table `poliquant.dwh.m_councilors` as
select 
  m.profile_url,
  m.name,
  m.furigana,
  m.party,
  d.id as district_id,
  m.district,
  case when d.type = "小選挙区" then null 
  else d.type 
  end as district_detail,
  m.expiration_date,
  m.session
from `poliquant.source.m_councilors` as m
left join `poliquant.source.m_councilors_district` as d
on m.district = d.district
;