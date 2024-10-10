# test-dev-v2-SUBSCONE_CreateInvoiceRecipients
請求書通知リストファイル作成(月次起動)

## 概要
このLambda関数は、請求書通知機能の月次起動処理を行います。
- DBから通知リストを取得し、S3にファイル（JSON形式）として保存します。

## 動作確認手順
1. AWSコンソールにアクセス
   - 環境: [test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients](https://ap-northeast-1.console.aws.amazon.com/lambda/home?region=ap-northeast-1#/functions/test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients?tab=code)
1. Lambda関数のテストを実行
   - Lambda管理画面でテストイベントを設定し、以下のJSONを入力します。
        ```
        {
          "retail_type_cd": "R0601DJICPA001",
          "bill_month": "202412",
        }
        ```
   - 「実行」ボタンを押下してLambda関数を実行します。
2. CloudWatch Logsの確認
  - AWSコンソールで「CloudWatch」にアクセスしてエラーになっていないことを確認
    - 環境: [/aws/lambda/test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients](https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Ftest-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients)
  - S3にファイルが配置されることを確認
    - パス: s3://dev-v2-subscone-s3-export/{事業所コード}/input/invoice
    - ファイル: to_sendgrid_to_sendgrid_YYYYMMDDHHMMSS_nnn.json
