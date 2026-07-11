@echo off
REM Run comprehensive Nuclei exploration scans sequentially (long-running).
setlocal
cd /d c:\projects\spiderfeet
set N=.tools\bin\nuclei.exe
set T=.tools\nuclei-templates
set O=.docs\docs-for-cli-tools\exploration_scratch\nuclei
set F=-silent -jsonl -omit-raw -omit-template -no-interactsh -etags dos,fuzz,misc -duc -retries 1 -c 25 -timeout 10
set S=-severity critical -severity high

if not exist "%O%" mkdir "%O%"

echo [%date% %time%] scanme all templates...
"%N%" -u http://scanme.nmap.org %F% -t "%T%" -jle "%O%\scanme_all_templates.jsonl" 2>"%O%\scanme_all_templates.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] bbc all templates...
"%N%" -u https://www.bbc.co.uk %F% -t "%T%" -jle "%O%\bbc_all_templates.jsonl" 2>"%O%\bbc_all_templates.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] scanme critical+high...
"%N%" -u http://scanme.nmap.org %F% -t "%T%" %S% -jle "%O%\scanme_critical_high.jsonl" 2>"%O%\scanme_critical_high.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] bbc critical+high...
"%N%" -u https://www.bbc.co.uk %F% -t "%T%" %S% -jle "%O%\bbc_critical_high.jsonl" 2>"%O%\bbc_critical_high.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] sbs critical+high...
"%N%" -u https://www.sbs.com.au %F% -t "%T%" %S% -jle "%O%\sbs_critical_high.jsonl" 2>"%O%\sbs_critical_high.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] praetorian critical+high...
"%N%" -u https://praetorian.com %F% -t "%T%" %S% -jle "%O%\praetorian_critical_high.jsonl" 2>"%O%\praetorian_critical_high.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] cloudflare critical+high...
"%N%" -u https://www.cloudflare.com %F% -t "%T%" %S% -jle "%O%\cloudflare_critical_high.jsonl" 2>"%O%\cloudflare_critical_high.stderr.txt"
echo exit=%errorlevel%

echo [%date% %time%] done.

echo [%date% %time%] converting JSONL exports to JSON bundles (records[])...
python .seed\scripts\cli_corpus\convert_nuclei_jsonl_exports.py
echo convert exit=%errorlevel%
