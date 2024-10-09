import os
import cgi
from constants import CSV_ENCODING


def handle_file_upload(handler, upload_dir):
    # ファイルのアップロード処理
    content_type, pdict = cgi.parse_header(handler.headers['Content-Type'])
    if content_type == 'multipart/form-data':
        pdict['boundary'] = pdict['boundary'].encode(CSV_ENCODING)
        fields = cgi.parse_multipart(handler.rfile, pdict)

        # アップロードされたファイルの情報を取得 (ファイル名の取得)
        file_field = fields.get('file')
        if file_field:
            uploaded_file = file_field[0]  # アップロードされたファイルデータ
            uploaded_file_name = handler.headers[
                'filename'] if 'filename' in handler.headers else 'uploaded_file.csv'
        else:
            return None, None, None

        pattern = fields.get('pattern')[0]  # パターン情報を取得

        # アップロードディレクトリの確認・作成
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # ファイルパスの作成
        file_path = os.path.join(upload_dir, uploaded_file_name)

        # ファイルの保存
        with open(file_path, 'wb') as f:
            f.write(uploaded_file)

        return uploaded_file_name, file_path, pattern
    return None, None, None
