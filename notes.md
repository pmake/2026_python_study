# 上課環境開發注意事項
##一次性提交commit和push而不留個資在本地電腦

-  1. 臨時身份 Commit
git -c user.name="[USER_NAME]" -c user.email="[EMAIL_ADDRESS]" commit -m "[COMMIT_MESSAGE]"

-  2. 臨時憑證 Push (會詢問一次 Token，但不儲存)
git -c credential.helper= push origin main
