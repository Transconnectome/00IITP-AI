# Overleaf Integration Guide (Step-by-Step)

## 1. 프로젝트 생성 (First Time Setup)
1.  **Overleaf 접속**: [https://www.overleaf.com](https://www.overleaf.com) 에 로그인합니다.
2.  **새 프로젝트**: 대시보드 좌측 상단의 초록색 **[New Project]** 버튼을 클릭합니다.
3.  **GitHub 가져오기**: 메뉴 중 **[Import from GitHub]**를 선택합니다.
    *   *Note: GitHub 계정 연동이 안 되어 있다면 연동 창이 뜹니다.*
4.  **저장소 선택**: `Transconnectome/00IITP-AI`를 검색하여 선택합니다.
5.  **생성 완료**: 프로젝트가 생성되고 편집기가 열립니다.

## 2. 메인 문서 설정 (Configuration)
Overleaf가 자동으로 `main.tex`를 찾지 못할 수 있습니다. 수동으로 지정해야 합니다.
1.  좌측 상단의 **[Menu]** 버튼을 클릭합니다.
2.  **Settings** 섹션의 **Main document** 드롭다운을 클릭합니다.
3.  목록에서 **`tex/main.tex`**를 찾아 선택합니다.
4.  **[Recompile]** 버튼을 누릅니다. -> 제안서 초안(Part 1~4)이 보이면 성공입니다!

## 3. 동기화 방법 (Syncing)
제가 터미널에서 작업을 수정하고 Push를 하면, Overleaf에서 다음을 수행하세요.
1.  좌측 상단 **[Menu]** 옆의 **GitHub 아이콘**을 클릭합니다.
2.  **[Pull GitHub changes into Overleaf]** 버튼을 클릭합니다.
3.  변경 사항이 반영됩니다.
