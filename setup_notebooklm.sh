#!/bin/bash
source .venv/bin/activate

echo "========================================================"
echo "NotebookLM MCP 인증 재시도 (디버그 모드)"
echo "========================================================"
echo "1. 이전 프로필 초기화 중..."
rm -rf chrome_profile_notebooklm
rm -f notebooklm-config.json

echo "2. 초기화 및 인증 시작..."
echo "--------------------------------------------------------"
echo "잠시 후 크롬 브라우저가 열립니다."
echo "구글 로그인을 완료하고, NotebookLM 페이지가 뜰 때까지 기다려 주세요."
echo "브라우저가 자동으로 닫히더라도, 이 터미널 창을 확인해 주세요."
echo "--------------------------------------------------------"

# 디버그 모드로 init 실행 (전역 --debug 플래그 사용)
notebooklm-mcp --debug init https://notebooklm.google.com/notebook/7acc2737-c783-43ff-af4c-e360ad02cf2c

echo "========================================================"
echo "스크립트 실행이 완료되었습니다."
echo "성공했다면 위 로그에 'Configuration saved' 등이 표시됩니다."
echo "실패했다면 에러 로그를 확인해 주세요."
echo "엔터 키를 누르면 터미널을 종료합니다."
read -p "Press Enter to exit..."
