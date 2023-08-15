drop table if exists `poliquant.mart.m_councilors_aggregated`
;

create table `poliquant.mart.m_councilors_aggregated` as
select 
  c.profile_url
  ,c.name
  ,c.furigana
  ,c.party
  ,2 as politician_type
  ,"参議院議員" as politician_type_name
  ,c.district_id
  ,c.district
  ,c.district_detail
  ,c.expiration_date
  ,c.session
  ,agg.name_of_house
  ,ifnull(agg.num_of_attendance, 0) as num_of_attendance
from `poliquant.dwh.m_councilors` as c
left join 
  (
    select 
      session
      ,name_of_house
      ,speaker
      ,count(distinct issue_id) as num_of_attendance
    from (
      select 
        issue_id
        ,session
        ,name_of_house
        ,speaker
      from `poliquant.dwh.meeting_list`
      where speaker != "会議録情報"
    ) 
    group by session, name_of_house, speaker
  ) agg
  on c.name = agg.speaker and c.session = agg.session
;
