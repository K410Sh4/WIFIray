# WIFIray — ESPhub Zero

Projeto independente. O repositório não importa versões/branches antigas. O Marco 4 é **candidato de laboratório**: compilação e testes automatizados não comprovam funcionamento nas placas ou detecção humana.

## Como iniciar o build auditado

Faça upload, **sem descompactar**, do arquivo `ESPhub_Zero_STAGE4_AUDITED_BUILD_SOURCES.zip` na raiz deste repositório, em `main`. O workflow [WIFIray Stage 4](.github/workflows/wifiray-stage4.yml) verifica o SHA-256 do ZIP antes de extrair e verifica o manifesto de todos os arquivos do projeto.

SHA-256 exato exigido para o ZIP: `b4debb6189a9bd999d507aeb052bcd12bbc2a180a7582135bad392674090df7e`.

O workflow compila separadamente o ESP32-S3, o ESP32-C6, o ESP32 DevKit clássico e o APK Android. A entrega agregada de 1 APK + 3 FULL.bin só é criada se **todos** os builds e testes forem aprovados. Arquivos para o usuário ficam em **Actions → execução → Artifacts**.

## Segurança e limitações

Este repositório foi identificado como **público** na primeira auditoria. Não suba senhas Wi-Fi, segredos por placa, backups NVS, credenciais, chaves privadas nem um APK de release assinado com sua chave. Os `FULL.bin` são de laboratório até confirmação física de flash e testes nas placas.

O Android compila em configuração `debug`, não uma release assinada. Qualidade do CSI, rendimento, Secure Boot, Flash Encryption e precisão de presença ainda exigem testes reais.
