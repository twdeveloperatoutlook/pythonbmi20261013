# BMI 計算器

使用 Flask 製作的成人 BMI 網頁計算器。輸入身高（公分）和體重（公斤）後，頁面會顯示 BMI（小數點後一位）、體位分類與生活建議。

主畫面的計算表單提供選填的姓名欄位，填寫後會在計算結果顯示姓名；未填姓名仍可正常計算。送出後會保留欄位內容，方便修改或更正輸入，姓名不會儲存至資料庫。

## 啟動

需安裝 Python 3.9 以上版本。在專案資料夾執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

接著開啟 http://127.0.0.1:5000/ 。若 PowerShell 不允許啟用虛擬環境，也可以使用 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` 和 `.\.venv\Scripts\python.exe app.py`。

## 計算方式

BMI = 體重（公斤）÷ 身高（公尺）²。分類採臺灣成人體位參考標準：低於 18.5 為體重過輕、18.5 至未滿 24 為健康體位、24 至未滿 27 為體重過重、27 以上為肥胖。頁面以顯示至小數點後一位的 BMI 進行分類。

體重過輕、過重或肥胖時，BMI 數值與體位分類文字會以紅色顯示；健康體位維持原有顏色。

這只是成人體位參考，不能取代專業醫療評估，也不適用於兒童、青少年或孕婦。

執行測試：`python -m unittest discover -s tests`

## 部署到 Azure Web App

`.github/workflows/deploy-azure.yml` 在 `main` 分支的應用程式、測試或 workflow 異動時執行，也可以從 GitHub Actions 手動觸發。流程會在 Windows runner 上執行測試、下載官方 Python 3.14.8 可嵌入版本，將 Python 與相依套件一起部署到 `NTUSTweb00`（資源群組 `NTUSTlab2026`）的 `staging` slot，搭配 GitHub `staging` environment。部署成功後，另一個 job 會等待 GitHub `production` environment 簽核；通過後重新登入 Azure，以 `az webapp deployment slot swap --slot staging --target-slot production` 將 staging 與 production 交換。站點透過 `web.config` 的 IIS HttpPlatformHandler 啟動 `serve.py`，以 Waitress 提供 Flask 服務。

此方法使用**隨部署包提供的 Python**，不依賴 Windows App Service 內建 Python 執行環境；HttpPlatformHandler 必須在目標站點可用。`NTUSTweb00` 目前是 Windows Web App，部署時會確認作業系統。

在 GitHub 儲存庫 **Settings → Secrets and variables → Actions** 確認：

- Repository secret `AZURE_CREDENTIALS`：Azure 服務主體的 `clientId`、`clientSecret`、`subscriptionId`、`tenantId` 組成的 JSON。此 Secret 已設定，不要把內容寫進程式碼。
- Repository variables `AZURE_WEBAPP_NAME`、`AZURE_RESOURCE_GROUP`：分別設定為 `NTUSTweb00`、`NTUSTlab2026`。若在 environment 層級覆寫，`staging` 與 `production` 必須指向相同的 Web App 與資源群組。

請先在 Azure Web App 建立 `staging` deployment slot，並確認 App Service 方案支援 deployment slots，且該 slot 的 HttpPlatformHandler 與必要應用程式設定已就緒。服務主體必須對 `NTUSTweb00` 及其 slots 具有部署與 slot swap 權限（例如該站點範圍的 **Website Contributor**）。

在 GitHub 儲存庫 **Settings → Environments** 建立 `staging` 與 `production`，並在 `production` 的 deployment protection rules 設定 **Required reviewers**；僅在 workflow 宣告 environment 不會自動啟用人工簽核。推送符合上述條件的 `main` 分支異動，或從 GitHub Actions 手動執行工作流程，確認 staging 部署結果後，再核准 production 部署以執行 swap。
