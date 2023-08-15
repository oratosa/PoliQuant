drop table if exists `poliquant.dwh.m_sessions`
;

create table `poliquant.dwh.m_sessions` as
select distinct session
from `poliquant.dwh.meeting_list`
;