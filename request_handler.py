import os
import shutil
from http.server import BaseHTTPRequestHandler
from file_handler import handle_file_upload
from csv_handler import process_csv
from constants import UPLOAD_DIR


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
            <html>
            <body>
            <h1>Upload CSV</h1>
            <form enctype="multipart/form-data" method="POST">
                <input type="file" name="file" /><br>
                <label for="pattern">Processing Pattern:</label>
                <select name="pattern">
                    <option value="pattern1">Pattern 1</option>
                    <option value="pattern2">Pattern 2</option>
                </select><br>
                <input type="submit" value="Upload" />
            </form>
            </body>
            </html>
        ''')

    def do_POST(self):
        # ファイルのアップロード処理
        uploaded_file_name, file_path, pattern = handle_file_upload(self, UPLOAD_DIR)

        if file_path:
            # CSV変換処理
            output_file_name = f'output_{uploaded_file_name}'
            output_file_path = os.path.join(UPLOAD_DIR, output_file_name)
            process_csv(file_path, output_file_path, pattern)

            # 変換後ファイルの提供
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{output_file_name}"')
            self.end_headers()

            with open(output_file_path, 'rb') as f:
                shutil.copyfileobj(f, self.wfile)
