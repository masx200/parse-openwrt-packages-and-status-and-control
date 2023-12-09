# 导入json模块，用于处理JSON格式数据
import json

# 导入sys模块，获取用户输入信息
import sys

# 导入os模块，处理文件和路径名
import os


# 定义一个函数，从文件路径中提取基本名称（不带扩展名）
def get_base_name(file_path):
    return os.path.splitext(os.path.basename(file_path))[0]


# 主函数
def main() -> None:
    # 提示用户输入文本文件名
    print("请输入一个文本文件名：")

    # 读取用户输入的图片文件名，并去除首尾的空格和双引号
    input_file = sys.stdin.readline().strip().strip('"')
    print("你输入的一个文本文件名是：", input_file)

    filename = input_file

    # 读取文本文件
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    print("输入文本已读取", filename)

    packages = parse_packages(text)

    outputfile = get_base_name(filename) + ".json"

    # 将解析结果写入JSON文件
    with open(outputfile, "w") as file:
        json.dump(packages, file)

    print("解析结果已写入", outputfile)


# 存储单行字符串键值
oneLinesStringKeys = [
    "Source",
    "SourceName",
    "LicenseFiles",
    "Maintainer",
    "Package",
    "Version",
    "ABIVersion",
    "License",
    "Section",
    "Architecture",
    "Filename",
    "SHA256sum",
    "CPE-ID",
    "Alternatives",
    "Essential",
    "Status",
    "Auto-Installed",
    "Require-User",
]


# 创建一个空的数据字典，包含所有可能的键和None作为默认值
def create_empty_data():
    data = {
        "Package": None,
        "Version": None,
        "ABIVersion": None,
        "Depends": [],
        "License": None,
        "Section": None,
        "Architecture": None,
        "Installed-Size": 0,
        "Filename": None,
        "Size": 0,
        "SHA256sum": None,
        "Description": None,
        "Provides": [],
        "Conflicts": [],
        "CPE-ID": None,
        "Alternatives": None,
        "Essential": None,
        "Status": None,
        "Installed-Time": 0,
        "Auto-Installed": None,
        "Source": None,
        "Conffiles": None,
        "SourceName": None,
        "SourceDateEpoch": 0,
    }
    for key in oneLinesStringKeys:
        data[key] = None
    return data


# 解析文本内容并生成JSON格式数据
def parse_packages(text: str):
    # 初始化一个空字典，用于存储解析后的数据
    packages = {}
    current_key = None

    # (current_key =="Description") = False
    # (current_key =="Conffiles") = False
    data = create_empty_data()

    # 遍历文本中的每一行
    for line in text.split("\n"):
        if line.startswith("Package:"):
            current_key = "Package"
            # (current_key =="Conffiles") = False
            # (current_key =="Description") = False
            data = create_empty_data()

            package = line[len(line.split(":")[0]) + 1 :]
            data["Package"] = package.strip()
        elif line.startswith("Conflicts:"):
            current_key = "Conflicts"
            Conflicts = [
                s.strip() for s in line[len(line.split(":")[0]) + 1 :].split(",")
            ]
            data["Conflicts"] = Conflicts
        elif line.startswith("Provides:"):
            current_key = "Provides"
            Provides = [
                s.strip() for s in line[len(line.split(":")[0]) + 1 :].split(",")
            ]
            data["Provides"] = Provides
        elif line.startswith("CPE-ID:"):
            current_key = "CPE-ID"
            CPE_ID = line[len(line.split(":")[0]) + 1 :]
            data["CPE-ID"] = CPE_ID.strip()
        elif line.startswith("Alternatives:"):
            current_key = "Alternatives"
            Alternatives = line[len(line.split(":")[0]) + 1 :]
            data["Alternatives"] = Alternatives.strip()
        elif line.startswith("Status:"):
            current_key = "Status"
            Status = line[len(line.split(":")[0]) + 1 :]
            data["Status"] = Status.strip()
        elif line.startswith("ABIVersion:"):
            current_key = line.split(":")[0]
            ABIVersion = line[len(line.split(":")[0]) + 1 :]
            data["ABIVersion"] = ABIVersion.strip()
        elif line.startswith("Version:"):
            current_key = line.split(":")[0]
            version = line[len(line.split(":")[0]) + 1 :]
            data["Version"] = version.strip()
        elif line.startswith("Auto-Installed:"):
            current_key = line.split(":")[0]
            Auto_Installed = line[len(line.split(":")[0]) + 1 :]
            data["Auto-Installed"] = Auto_Installed.strip()
        elif line.startswith("Depends:"):
            current_key = line.split(":")[0]
            depends = [
                s.strip() for s in line[len(line.split(":")[0]) + 1 :].split(",")
            ]
            data["Depends"] = depends
        elif line.startswith("License:"):
            current_key = line.split(":")[0]
            License = line[len(line.split(":")[0]) + 1 :]
            data["License"] = License.strip()
        elif line.startswith("Section:"):
            current_key = line.split(":")[0]
            section = line[len(line.split(":")[0]) + 1 :]
            data["Section"] = section.strip()
        elif line.startswith("Architecture:"):
            current_key = line.split(":")[0]
            architecture = line[len(line.split(":")[0]) + 1 :]
            data["Architecture"] = architecture.strip()
        elif line.startswith("Installed-Size:"):
            current_key = line.split(":")[0]
            installed_size = int(line[len(line.split(":")[0]) + 1 :])
            data["Installed-Size"] = installed_size
        elif line.startswith("Installed-Time:"):
            current_key = line.split(":")[0]
            Installed_Time = int(line[len(line.split(":")[0]) + 1 :])
            data["Installed-Time"] = Installed_Time
        elif line.startswith("Filename:"):
            current_key = line.split(":")[0]
            filename = line[len(line.split(":")[0]) + 1 :]
            data["Filename"] = filename.strip()
        elif line.startswith("Essential:"):
            current_key = line.split(":")[0]
            Essential = line[len(line.split(":")[0]) + 1 :]
            data["Essential"] = Essential.strip()
        elif line.startswith("Size:"):
            current_key = line.split(":")[0]
            size = int(line[len(line.split(":")[0]) + 1 :])
            data["Size"] = size
        elif line.startswith("SourceDateEpoch:"):
            current_key = line.split(":")[0]
            SourceDateEpoch = int(line[len(line.split(":")[0]) + 1 :])
            data["SourceDateEpoch"] = SourceDateEpoch
        elif line.startswith("SHA256sum:"):
            current_key = line.split(":")[0]
            sha256sum = line[len(line.split(":")[0]) + 1 :]
            data["SHA256sum"] = sha256sum.strip()
        elif line.startswith("Conffiles:"):
            current_key = line.split(":")[0]
            # (current_key =="Description") = False
            # (current_key =="Conffiles") = True
            Conffiles = line[len(line.split(":")[0]) + 1 :]

            data["Conffiles"] = Conffiles.strip()
        elif line.startswith("Description:"):
            current_key = line.split(":")[0]
            # (current_key =="Description") = True
            # (current_key =="Conffiles") = False
            description = line[len(line.split(":")[0]) + 1 :]

            data["Description"] = description.strip()
            # assign the final description to the data dictionary.
            # This will be the same as the original text, but without the first paragraph and with newlines between paragraphs.
        elif (current_key == "Conffiles") == True:
            if data["Conffiles"] == None:
                data["Conffiles"] = ""
            data["Conffiles"] = data["Conffiles"].strip() + "\n" + line.strip()

            pass
        else:
            if (current_key == "Description") == True:
                if data["Description"] == None:
                    data["Description"] = ""
                data["Description"] = data["Description"].strip() + "\n" + line.strip()

            else:
                # print(line)
                if ":" in line:
                    if line.split(":")[0] not in oneLinesStringKeys:
                        print(line)
                    # print(line.split(":"))
                    current_key = line.split(":")[0]
                    data[line.split(":")[0]] = line[
                        len(line.split(":")[0]) + 1 :
                    ].strip()
                    # print(data)
                pass

        if "SHA256sum" in data and data["SHA256sum"] != None:
            key = data["SHA256sum"]
            if key not in packages:
                packages[key] = data
            else:
                value = packages[key]
                d2 = merge_dict_not_None(value, data)
                data = d2
                packages[key] = d2
        # print(data)
        if (
            data["Architecture"] != None
            and data["Package"] != None
            and data["Version"] != None
        ):
            key = data["Package"] + "_" + data["Version"] + "_" + data["Architecture"]
            if key not in packages:
                packages[key] = data
            else:
                value = packages[key]
                d2 = merge_dict_not_None(value, data)
                data = d2
                packages[key] = d2

        # print(json.dumps(data))
    return packages


def merge_dict_not_None(value, data):
    d2 = {}
    for dict1 in [data, value]:
        for k, v in dict1.items():
            if k not in d2:
                d2[k] = None

            if v != None:
                d2[k] = v
    return d2


if __name__ == "__main__":
    main()
