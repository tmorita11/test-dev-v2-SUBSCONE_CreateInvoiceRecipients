import json
import urllib.parse
import common_function
from datetime import datetime
from lib.s3_accessor import S3Accessor
from lib.sql_server_accessor import SQLServerAccessor

# 請求書の通知先情報取得クエリ
INVOICE_NOTIFY_QUERY = """
    SELECT
        CAI.CUST_NM1,
        CAI.MAIL_EMAIL,
        HBA.ISSUE_NO,
        CAI.CUST_CD,
        HBA.BILL_MONTH
    FROM
        HIST_BILL_AMOUNT AS HBA
        INNER JOIN CUST_ACNT_INFO CAI 
        ON HBA.RETAIL_TYPE_CD = CAI.RETAIL_TYPE_CD
        AND HBA.CUST_CD = CAI.CUST_CD
    WHERE
        HBA.RETAIL_TYPE_CD = ?
        AND HBA.BILL_MONTH = ?
"""


def lambda_handler(event, context):
    # EventBridgeの定数から取得
    sendgrid_template_id = event.get("sendgrid_template_id")
    retail_type_cd = event.get("retail_type_cd")
    bill_month = event.get("bill_month")

    try:
        # SQL Serverに接続してクエリを実行
        with SQLServerAccessor() as sql_server_accessor:
            result = sql_server_accessor.fetch_all(
                INVOICE_NOTIFY_QUERY, (retail_type_cd, bill_month))

        if not result:
            raise ValueError(
                f"No invoice notification data found for retail_type_cd: {retail_type_cd}, bill_month: {bill_month}"
            )

        # クエリ結果をJSONに変換
        json_data = json.dumps(result, ensure_ascii=False, indent=2)

        # タグを辞書として定義
        tags_dict = {
            "sendgrid_template_id": sendgrid_template_id,
            "bill_month": bill_month
        }

        # S3にアップロード
        S3Accessor(retail_type_cd).upload_json_data(
            file_name=f"to_sendgrid_{get_current_jst_time()}.json",
            json_data=json_data,
            tags=urllib.parse.urlencode(tags_dict)
        )

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return generate_error_response(404, "No Data Found", str(ve))

    except Exception as e:
        print(f"An error occurred {e}")
        return generate_error_response(500, "Internal Server Error", str(e))

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully')
    }


def get_current_jst_time():
    current_jst_time = datetime.now(common_function.getJST())
    # YYYYMMDDHHMMSS形式に変換
    formatted_time = current_jst_time.strftime('%Y%m%d%H%M%S')
    # ミリ秒を取得
    milliseconds = current_jst_time.microsecond // 1000

    return f"{formatted_time}_{str(milliseconds).zfill(3)}"


def generate_error_response(status_code, error_type, message):
    error_message = message.encode('utf-8')
    decoded_message = error_message.decode('utf-8')

    response_body = {
        'error': error_type,
        'message': decoded_message
    }

    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }
