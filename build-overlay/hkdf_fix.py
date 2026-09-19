#!/usr/bin/env python3
"""Deterministic Stage 4 source correction. Archive is SHA-pinned before this runs.

Implement RFC 5869 HKDF-SHA256 using the already-linked mbedtls_md_hmac
primitive, preserving Kotlin's HKDF parameters and binary output.
"""
from pathlib import Path

src = Path("firmware/main/uplink.cpp")
content = src.read_text()
original = """    const auto* sha=mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
    const bool ok=sha&&mbedtls_hkdf(sha,salt,sizeof(salt),secret,32,info,base+1,derived,sizeof(derived))==0;
"""
replacement = """    // HKDF (RFC 5869) using HMAC-SHA256, independent of MBEDTLS_HKDF_C.
    // Extract: PRK = HMAC(salt, IKM). Expand: T(i)=HMAC(PRK,T(i-1)||info||i).
    uint8_t prk[32]{};
    uint8_t previous[32]{};
    uint8_t block[32+sizeof(info)+1]{};
    bool ok=mac(salt,sizeof(salt),secret,32,prk);
    size_t produced=0;
    uint8_t round=1;
    size_t prevLen=0;
    while(ok && produced<sizeof(derived)){
        memcpy(block,previous,prevLen);
        memcpy(block+prevLen,info,base+1);
        block[prevLen+base+1]=round++;
        ok=mac(prk,sizeof(prk),block,prevLen+base+2,previous);
        if(ok){
            const size_t count=(sizeof(derived)-produced<sizeof(previous))
                ? sizeof(derived)-produced : sizeof(previous);
            memcpy(derived+produced,previous,count);
            produced+=count;
            prevLen=sizeof(previous);
        }
    }
    wipe(prk,sizeof(prk));wipe(previous,sizeof(previous));wipe(block,sizeof(block));
"""
if content.count(original)!=1:
    raise SystemExit("FAIL: expected original HKDF call exactly once; no patch applied")
content=content.replace(original,replacement)
content=content.replace('#include "mbedtls/hkdf.h"\n','')
src.write_text(content)
print("Stage 4 firmware HKDF-SHA256 source corrected (HMAC extract + expand).")
