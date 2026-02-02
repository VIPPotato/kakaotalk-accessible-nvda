> Korean translation is available below.  
> 아래에 한국어 번역이 있습니다.

# KakaoTalk Accessible NVDA Add-on

## Overview
This NVDA add-on improves the accessibility of the desktop version of KakaoTalk for screen reader users. It specifically addresses issues where lists (such as friends lists, chat lists, and message histories) are not properly readable or navigable using NVDA.

## Features
*   **Improved List Navigation**: Forces proper focus handling for KakaoTalk's custom list controls (`EVA_VH_ListControl_Dblclk`), ensuring that list items are correctly announced when navigating with arrow keys.
*   **Focus Fixes**: Prevents focus from getting "stuck" on the parent container, ensuring the actual list items receive focus.

## Installation
1.  Download the latest release from the [Releases page](https://github.com/VIPPotato/kakaotalk-accessible-nvda/releases).
2.  Open the downloaded `.nvda-addon` file.
3.  Follow the prompts to install the add-on in NVDA.
4.  Restart NVDA when prompted.

## Usage
Once installed, the add-on works automatically. When you navigate lists within KakaoTalk (e.g., the Friends list or Chat list), NVDA should now correctly announce the focused item.

## Development
### Prerequisites
*   Python 3.11 or later
*   SCons (`pip install scons`)

### Building
To build the add-on from source:
1.  Clone the repository.
2.  Run `scons` in the root directory.
3.  The `.nvda-addon` package will be generated in the same directory.

## License
This project is licensed under the GNU General Public License, version 2 or later. See `COPYING.txt` for details.

---

# 카카오톡 접근성 향상 NVDA 애드온

## 개요
이 NVDA 애드온은 화면 읽기 프로그램 사용자를 위해 카카오톡 데스크톱 앱의 접근성을 개선합니다. 특히 친구 목록, 채팅 목록, 메시지 기록과 같은 목록이 NVDA에서 제대로 읽히거나 탐색되지 않는 문제를 해결하는 데 초점을 맞춥니다.

## 기능
*   **목록 탐색 개선**: 카카오톡의 커스텀 목록 컨트롤(`EVA_VH_ListControl_Dblclk`)에서 포커스 처리를 보정하여, 방향키로 이동할 때 항목이 올바르게 읽히도록 합니다.
*   **포커스 수정**: 포커스가 부모 컨테이너에 “고정”되는 현상을 방지하고, 실제 목록 항목이 포커스를 받도록 합니다.

## 설치
1.  [릴리스 페이지](https://github.com/VIPPotato/kakaotalk-accessible-nvda/releases)에서 최신 버전을 다운로드합니다.
2.  다운로드한 `.nvda-addon` 파일을 엽니다.
3.  NVDA 설치 안내에 따라 애드온을 설치합니다.
4.  안내가 나오면 NVDA를 재시작합니다.

## 사용 방법
설치 후 애드온은 자동으로 동작합니다. 카카오톡 내의 목록(예: 친구 목록, 채팅 목록)을 탐색하면 NVDA가 현재 항목을 올바르게 읽어야 합니다.

## 개발
### 준비물
*   Python 3.11 이상
*   SCons (`pip install scons`)

### 빌드
소스에서 애드온을 빌드하려면:
1.  이 저장소를 클론합니다.
2.  루트 디렉터리에서 `scons`를 실행합니다.
3.  같은 디렉터리에 `.nvda-addon` 패키지가 생성됩니다.

## 라이선스
이 프로젝트는 GNU General Public License 2 이상으로 배포됩니다. 자세한 내용은 `COPYING.txt`를 참고하세요.
