import csv
from constants import ACCOUNTING_SUBJECTS, REDUCED_TAX_RATE_STORES
from utils import guess_accounting_subject, guess_reduced_tax_rate


def process_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='shift_jis') as infile, open(
            output_file, mode='w', newline='',
            encoding='shift_jis') as outfile:

        # ファイルの全行をリストとして読み込む
        all_lines = infile.readlines()

        # 最初の4行をスキップし、5行目からCSVデータを対象とする
        data_lines = all_lines[4:]  # 最初の4行をスキップ

        # 5行目以降のデータをDictReaderで読み込み
        reader = csv.DictReader(data_lines)
        writer = csv.writer(outfile)

        # 出力ファイルのヘッダー行を書き込む
        writer.writerow(["日付", "入出金", "勘定科目", "摘要", "軽減税率", "備考"])

        # データを処理し、書き込む
        for row in reader:
            # CSV内のデータを取り出す
            date = row["利用日"]
            amount = row["利用金額"]
            store_name = row["ご利用店名及び商品名"]
            remarks = row["備考"]

            # 勘定科目と軽減税率を推測
            accounting_subject = guess_accounting_subject(
                store_name, ACCOUNTING_SUBJECTS)
            reduced_tax_rate = guess_reduced_tax_rate(store_name,
                                                      REDUCED_TAX_RATE_STORES)

            # 軽減税率が適用される場合は「※」を設定
            reduced_tax_rate_indicator = "※" if reduced_tax_rate else ""

            # CSVに書き込む行を作成
            write_info = [
                f'{date}',  # 日付
                f'{amount}',  # 入出金
                f'{accounting_subject}',  # 勘定科目
                f'{store_name}',  # 摘要
                f'{reduced_tax_rate_indicator}',  # 軽減税率
                f'{remarks}'  # 備考
            ]

            # 作成した情報をCSVに書き込む
            writer.writerow(write_info)
