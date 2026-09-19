#!/usr/bin/env python3
"""Allow screenshots of authenticated diagnostic view, never key-entry view.

Source ZIP is SHA-pinned separately. Fails closed if upstream MainActivity
does not match the audited Stage 4 code.
"""
from pathlib import Path

p=Path("android/app/src/main/java/dev/esphub/zero/MainActivity.kt")
s=p.read_text(encoding="utf-8")
a='''            fields.values.forEach {it.setText("");it.isEnabled=false}
            message.text="Wi-Fi em uso. Buscando nós com desafio HMAC; nenhum dado antes de autenticar."
'''
b='''            fields.values.forEach {it.setText("");it.isEnabled=false}
            message.text="Wi-Fi em uso. Buscando nós com desafio HMAC; nenhum dado antes de autenticar."
            // Keys were cleared from all UI fields: permit screenshots of telemetry only.
            window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)
'''
c='''    private fun stopClient(){
        sessionEpoch++
'''
d='''    private fun stopClient(){
        // Prevent screenshots before fields are made editable for new secrets.
        window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        sessionEpoch++
'''
for old,new in ((a,b),(c,d)):
    if s.count(old)!=1: raise SystemExit("FAIL CLOSED: unexpected MainActivity source")
    s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
assert s.count("window.setFlags(WindowManager.LayoutParams.FLAG_SECURE,WindowManager.LayoutParams.FLAG_SECURE)")==1
assert s.count("window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)")==1
assert s.count("window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)")==1
assert s.index("fields.values.forEach {it.setText(\"\");it.isEnabled=false}") < s.index("window.clearFlags(WindowManager.LayoutParams.FLAG_SECURE)")
assert s.index("window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)") < s.index("fields.values.forEach {it.isEnabled=true;it.setText(\"\")}")
print("PASS: screenshot restriction present during key entry and cleared only after UI keys are erased")
