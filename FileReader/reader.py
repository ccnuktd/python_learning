import csv


def read_file_line(file_path: str, encoding='utf-8'):
    """
    逐行读取文件数据，默认以utf-8编码读取
    用此方法读出的line为str类型
    :param encoding:
    :param file_path:
    :return:
    """

    with open(file_path, 'r', encoding=encoding) as f:
        lines = f.readlines()
        for line in lines:
            yield line


def read_csv_line(file_path: str, encoding='utf-8'):
    """
    逐行读取csv文件数据，默认以utf-8编码读取
    用此方法读出的line为list
    :param file_path:
    :param encoding:
    :return:
    """

    with open(file_path, 'r', encoding=encoding) as f:
        reader = csv.reader(f)
        # 跳过首行
        next(reader)
        for line in reader:
            yield line


if __name__ == '__main__':
    pass
    # for line in read_file_line('./data.csv'):
    #     print(line)

    # for line in read_csv_line('./data.csv'):
    #     print(line)
