import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from csv_handler import process_csv
import shutil

# アップロードディレクトリの作成
UPLOAD_DIR = 'uploads'
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # アップロードフォームの提供
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html>
            <body>
            <h1>Upload CSV</h1>
            <form enctype="multipart/form-data" method="POST">
                <input type="file" name="file" />
                <input type="submit" value="Upload" />
            </form>
            </body>
            </html>
        ''')

    def do_POST(self):
        # ファイルのアップロード処理
        content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
        if content_type == 'multipart/form-data':
            # 修正箇所: pdict['boundary'] が str なので decode() を削除
            pdict['boundary'] = pdict['boundary'].encode(
                'shift_jis')  # str → bytesに変換
            fields = cgi.parse_multipart(self.rfile, pdict)
            uploaded_file = fields.get('file')[0]
            file_path = os.path.join(UPLOAD_DIR, 'uploaded.csv')

            # ファイルの保存
            with open(file_path, 'wb') as f:
                f.write(uploaded_file)

            # CSV変換処理
            output_file = os.path.join(UPLOAD_DIR, 'output.csv')
            process_csv(file_path, output_file)

            # 変換後ファイルの提供
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition',
                             'attachment; filename="output.csv"')
            self.end_headers()

            with open(output_file, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
