# MVP syncthing-ignored

## Scripts
- `events.py` st disk events reader (api key from env `$STAPIKEY`)
- `gen.py` st ignorelist generator, takes root folder as parameter

## WIP Algo
1. Load token and folder id from config/env
2. Check ignores for .stglobalignore inclusion
3. Check ignores for folders descendant to current
4. Connect to /rest/events/disk
5. Read event
6. If created or moved descendant to already ignored - continue
7. Re-generate contents for .stglobalignore
8. Re-read .stglobalignore
9. Write if necessary
