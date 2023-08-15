drop table if exists `poliquant.mart.m_representatives_aggregated`
;

create table `poliquant.mart.m_representatives_aggregated` as
select 
  main.profile_url
  ,main.name
  ,main.furigana
  ,main.party
  ,main.politician_type
  ,main.politician_type_name
  ,main.district_id
  ,main.district
  ,main.district_detail
  ,main.elected_times
  ,main.session
  ,agg.name_of_house
  ,ifnull(agg.num_of_attendance, 0) as num_of_attendance
from
  (
    select 
      r.profile_url
      ,r.name
      ,r.furigana
      ,r.party
      ,1 as politician_type
      ,"衆議院議員" as politician_type_name
      ,r.district_id
      ,r.district
      ,r.district_detail
      ,r.elected_times
      ,s.session
    from `poliquant.dwh.m_representatives` as r
    cross join poliquant.dwh.m_sessions as s
  ) main
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
  on main.name = agg.speaker and main.session = agg.session
;
