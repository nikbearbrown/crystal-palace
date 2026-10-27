# O-CHATS — Chatsworth Great Stove + Victoria lily house (1840s)

```
blender -b -P scripts/build_chatsworth.py -- --out rounds/ch01.blend
blender -b rounds/ch01.blend -P scripts/check_set.py -- --out checks/ch01
scripts/render_round.sh ch01 ALL
```
