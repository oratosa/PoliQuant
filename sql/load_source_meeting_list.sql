TRUNCATE TABLE `poliquant.source.meeting_list`
;

LOAD DATA INTO `poliquant.source.meeting_list`
(
  numberOfRecords STRING OPTIONS(description="総結果件数"),
  numberOfReturn STRING OPTIONS(description="返戻件数"),
  startRecord STRING OPTIONS(description="開始位置"),
  nextRecordPosition STRING OPTIONS(description="次開始位置"),
  meetingRecord ARRAY
    <STRUCT
      <
      issueID STRING OPTIONS(description="会議録ID")
      ,imageKind STRING OPTIONS(description="イメージ種別（会議録・目次・索引・附録・追録）")
      ,searchObject STRING OPTIONS(description="検索対象箇所（議事冒頭・本文）")
      ,session STRING OPTIONS(description="国会回次")
      ,nameOfHouse STRING OPTIONS(description="院名")
      ,nameOfMeeting STRING OPTIONS(description="会議名")
      ,issue STRING OPTIONS(description="号数")
      ,date STRING OPTIONS(description="開催日付")
      ,closing STRING OPTIONS(description="閉会中フラグ")
      ,speechRecord ARRAY
        <STRUCT
          <
          speechID STRING OPTIONS(description="発言ID")
          ,speechOrder STRING OPTIONS(description="発言番号")
          ,speaker STRING OPTIONS(description="発言者名")
          ,speechURL STRING OPTIONS(description="発言URL")
          >
        >
      ,meetingURL STRING OPTIONS(description="会議録テキスト表示画面のURL")
      ,pdfURL STRING OPTIONS(description="会議録PDF表示画面のURL")
      >
    >
)
FROM FILES (
  format = 'JSON',
  uris = ['gs://poliquant/data/meeting_list/*.json']
)
;
