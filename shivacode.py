Re-check exact path
dir "C:\Users\C879571\IdeaProjects\rebate-rules\frontend\node_modules\@isaacs\cliui\node_modules\ansi-styles" -Recurse
dir "C:\Users\C879571\IdeaProjects\rebate-rules\frontend\node_modules\error-ex" -Recurse

Search entire drive
Get-ChildItem -Path C:\Users\C879571\ -Recurse -Include "ansi-styles","error-ex" -ErrorAction SilentlyContinue

Check Windows Installer/Temp
Get-ChildItem C:\Windows\Installer -Recurse | findstr ansi
Get-ChildItem $env:TEMP -Recurse | findstr error-ex

