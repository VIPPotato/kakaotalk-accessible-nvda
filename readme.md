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