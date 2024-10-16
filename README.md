# test-dev-v2-SUBSCONE_CreateInvoiceRecipients
請求書通知: 通知先リストを作成(月次起動)

## 概要
このLambda関数は、請求書通知機能の月次起動処理を行います。
- EventBridgeにより本Lambdaを起動
  - スケジュール: 月次
  - 入力定数:
    - 事業所コード
    - 請求月
    - テンプレート番号(SendGrid)
- DBから事業所コード、請求月を元に通知リストを取得し、S3にファイル（JSON形式）として保存(※)します。<br/>※StepFunctionでも利用する請求月、テンプレートをタグに設定

## 動作確認手順
1. AWSコンソールにアクセス
   - 環境: [test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients](https://ap-northeast-1.console.aws.amazon.com/lambda/home?region=ap-northeast-1#/functions/test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients?tab=code)
1. Lambda関数のテストを実行
   - Lambda管理画面でテストイベントを設定し、以下のJSONを入力します。
        ```
        {
          "retail_type_cd": "R0601DJICPA001",
          "bill_month": "202412",
          "sendgrid_template_id": "d-d05f126e78d44992930f6a2cd17cbb52"
        }
        ```
   - 「実行」ボタンを押下してLambda関数を実行します。
2. CloudWatch Logsの確認
  - AWSコンソールで「CloudWatch」にアクセスしてエラーになっていないことを確認
    - 環境: [/aws/lambda/test-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients](https://ap-northeast-1.console.aws.amazon.com/cloudwatch/home?region=ap-northeast-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Ftest-dev-v2-SUBSCONE_InvoiceNotify_CreateRecipients)
  - S3にファイルが配置されることを確認
    - パス: s3://dev-v2-subscone-s3-export/{事業所コード}/input/invoice
    - ファイル: to_sendgrid_to_sendgrid_YYYYMMDDHHMMSS_nnn.json
