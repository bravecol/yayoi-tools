import csv
from constants import ACCOUNTING_SUBJECTS, REDUCED_TAX_RATE_STORES, CSV_ENCODING
from utils import guess_accounting_subject, guess_reduced_tax_rate


def process_csv(input_file, output_file, pattern):
    with open(input_file, mode='r',
              encoding=CSV_ENCODING) as infile, open(output_file,
                                                     mode='w',
                                                     newline='',
                                                     encoding=CSV_ENCODING) as outfile:
        all_lines = infile.readlines()
        data_lines = all_lines[4:]  # 最初の4行をスキップ

        reader = csv.DictReader(data_lines)
        writer = csv.writer(outfile)

        # 出力ファイルのヘッダー行を書き込む
        writer.writerow(["日付", "入出金", "勘定科目", "摘要", "軽減税率", "備考"])

        for row in reader:
            # パターンごとの処理分岐
            if pattern == 'pattern1':
                write_info = create_csv_row_pattern1(row)
            elif pattern == 'pattern2':
                write_info = create_csv_row_pattern2(row)
            writer.writerow(write_info)


def create_csv_row_pattern1(row):
    date = row["利用日"]
    amount = row["利用金額"]
    store_name = row["ご利用店名及び商品名"]
    remarks = row["備考"]

    accounting_subject = guess_accounting_subject(store_name, ACCOUNTING_SUBJECTS)
    reduced_tax_rate = guess_reduced_tax_rate(store_name, REDUCED_TAX_RATE_STORES)
    reduced_tax_rate_indicator = "※" if reduced_tax_rate else ""

    return [
        date,  # 日付
        amount,  # 入出金
        accounting_subject,  # 勘定科目
        store_name,  # 摘要
        reduced_tax_rate_indicator,  # 軽減税率
        remarks  # 備考
    ]


def create_csv_row_pattern2(row):
    # pattern2 用のCSV行の作成処理
    date = row["利用日"]
    amount = row["利用金額"]
    store_name = row["ご利用店名及び商品名"]
    remarks = row["備考"]

    accounting_subject = "Pattern 2: " + guess_accounting_subject(store_name, ACCOUNTING_SUBJECTS)
    reduced_tax_rate = guess_reduced_tax_rate(store_name, REDUCED_TAX_RATE_STORES)
    reduced_tax_rate_indicator = "※" if reduced_tax_rate else ""

    return [
        date,  # 日付
        amount,  # 入出金
        accounting_subject,  # 勘定科目（pattern2 の場合）
        store_name,  # 摘要
        reduced_tax_rate_indicator,  # 軽減税率
        remarks  # 備考
    ]
