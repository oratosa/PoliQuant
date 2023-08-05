drop table if exists `poliquant.dwh.m_representatives`
;

create table `poliquant.dwh.m_representatives` as
select 
  r.profile_url,
  r.name,
  r.furigana,
  r.party,
  d.id as district_id,
  r.district,
  r.district_detail,
  r.elected_times,
  r.as_of_date
from
  (
    select 
      profile_url,
      name,
      furigana,
      party,
      regexp_replace(district, r'(\(\D\))|\d','') as district,
      case 
        when regexp_contains(district, r'\(\D\)') then "比例"
        when regexp_contains(district, r'\d') then "小選挙区"  
        end as type,
      case 
        when regexp_contains(district, r'\(\D\)') then "比例"
        when regexp_contains(district, r'\d') then regexp_replace(district, r'\D','')  
        end as district_detail,
      elected_times,
      as_of_date
    from `poliquant.source.m_representatives`
  ) r
left join `poliquant.source.m_representatives_district` as d
    on r.district = d.district
    and r.type = d.type 
;