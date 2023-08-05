drop table if exists `poliquant.mart.meeting_list`
;

create table `poliquant.mart.meeting_list` as
select 
  m.issue_id
  ,m.session
  ,m.name_of_house
  ,m.name_of_meeting
  ,m.issue
  ,m.date
  ,m.speech_id
  ,m.speech_order
  ,m.speaker
  ,case when r.name is not null then 1
        when c.name is not null then 2
        else 3 end
        as politician_type
  ,case when r.name is not null then "衆議院議員"
        when c.name is not null then "参議院議員"
        else "不明" end
        as politician_type_name
  ,coalesce(r.profile_url, c.profile_url) as profile_url 
  ,coalesce(r.party, c.party) as party
  ,coalesce(r.district_id, c.district_id) as district_id
  ,coalesce(r.district, c.district) as district
  ,coalesce(r.district_detail, c.district_detail) as district_detail
  ,r.elected_times as representative_elected_times
  ,c.expiration_date as counsilor_expiration_date
  ,m.speech_url
  ,m.meeting_url
  ,m.pdf_url
from 
  (select 
    issue_id
    ,session
    ,name_of_house
    ,name_of_meeting
    ,issue
    ,date
    ,speech_id
    ,speech_order
    ,speaker
    ,speech_url
    ,meeting_url
    ,pdf_url
  from `poliquant.dwh.meeting_list`
  where speaker != "会議録情報"
  ) as m
left join `poliquant.dwh.m_representatives` as r
  on  m.speaker = r.name
left join `poliquant.dwh.m_councilors` as c
  on  m.speaker = c.name
  and m.session = cast(c.session as INTEGER)
;