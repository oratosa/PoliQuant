DROP TABLE IF EXISTS `poliquant.source.meeting_list`
;
CREATE TABLE `poliquant.source.meeting_list`
(
  numberOfRecords INT64 OPTIONS(description="総結果件数"),
  numberOfReturn INT64 OPTIONS(description="返戻件数"),
  startRecord INT64 OPTIONS(description="開始位置"),
  nextRecordPosition INT64 OPTIONS(description="次開始位置"),
  meetingRecord ARRAY<STRUCT<
    issueID STRING OPTIONS(description="会議録ID")
  , imageKind STRING OPTIONS(description="イメージ種別（会議録・目次・索引・附録・追録）")
  , searchObject INT64 OPTIONS(description="検索対象箇所（議事冒頭・本文）")
  , session INT64 OPTIONS(description="国会回次")
  , nameOfHouse STRING OPTIONS(description="院名")
  , nameOfMeeting STRING OPTIONS(description="会議名")
  , issue STRING OPTIONS(description="号数")
  , date DATE OPTIONS(description="開催日付")
  , closing STRING OPTIONS(description="閉会中フラグ")
  , speechRecord ARRAY<STRUCT<
      speechID STRING OPTIONS(description="発言ID")
    , speechOrder INT64 OPTIONS(description="発言番号")
    , speaker STRING OPTIONS(description="発言者名")
    , speechURL STRING OPTIONS(description="発言URL")>>
  , meetingURL STRING OPTIONS(description="会議録テキスト表示画面のURL")
  , pdfURL STRING OPTIONS(description="会議録PDF表示画面のURL")>>
)
;