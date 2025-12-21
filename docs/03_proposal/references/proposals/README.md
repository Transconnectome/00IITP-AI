# Related Proposals (관련/참고 제안서)

이 폴더는 “현재 IITP 제안서”를 쓰면서 참고할 **이전 제안서/샘플/유사 과제 제안서**를 보관합니다.

## 어디에 무엇을 두나?

- **현재 제안서 작업본(이 repo의 주 문서)**: `docs/03_proposal/`  
  - `outline.md`, `sections/` 중심으로 “내용”을 관리
- **관련/참고 제안서(읽기 전용 레퍼런스)**: `docs/03_proposal/references/proposals/`
- **최종 제출본**: `docs/03_proposal/submissions/`  
  - 제출 날짜/버전으로 폴더를 나눠 보관

## Git에 커밋할지?

- 원본 PDF는 종종 **기밀/저작권/개인정보** 이슈가 있을 수 있습니다. (외부 공유/원격 push 전 확인 권장)
- 현재 설정은 **PDF는 커밋 가능**, 대신 자동 생성물은 제외:
  - 커밋 가능: `docs/03_proposal/references/proposals/*.pdf`
  - 기본 제외: `docs/03_proposal/references/proposals/parsed/`, `ocr_previews/`

## 네이밍 규칙(권장)

- `YYYY_program_project_owner_vX.ext`  
  예) `2024_IITP_AI_ConnectomeLab_v3.hwp`

## 각 제안서 옆에 메모 파일(권장)

관련 제안서 파일과 같은 이름의 메모를 함께 두세요:

- `2024_IITP_AI_ConnectomeLab_v3.md`

메모에 최소 포함:

- 출처/제출처/연도
- 이 제안서에서 “재사용 가능한 문장/구조/그림 아이디어”
- 이번 제안서에 적용 시 주의점(평가항목/양식 차이)


