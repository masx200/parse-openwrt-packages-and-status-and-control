import re

# 导入json模块，用于处理JSON格式数据
import json

"""
    这个代码实现了一个简单的文本解析器，用于将一个包含特定格式的文本文件转换为JSON格式。程序首先从用户处获取输入的文本文件名，并读取该文件的内容。然后调用parse_packages()函数对文本内容进行解析，并将结果存储在一个字典中。最后，程序将这个字典转换为JSON格式，并将其写入到一个新的文件中。

parse_packages()函数通过遍历文本中的每一行，根据每行的开头来判断其对应的键，并将值存储在数据字典中。同时，它还会检查是否已经存在相同的键，如果存在，则会合并这两个键对应的值。

    
    """
# 导入sys模块，获取用户输入信息
import sys

# 导入os模块，处理文件和路径名
import os


# 定义一个函数，从文件路径中提取基本名称（不带扩展名）
def get_base_name(file_path: str):
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
        json.dump(packages, file, indent=4)

    print("解析结果已写入", outputfile)


multiLineArrayOfStringKeys = ["Tag", "Description", "Conffiles"]

# 存储单行字符串键值
oneLinesStringKeys = [
    "Npp-Description",
    "Npp-File",
    "Npp-Mimetype",
    "Npp-Name",
    "Python-Version",
    "Ruby-Versions",
    "Description-md5",
    "Build-Ids",
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
    "Priority",
    "Origin",
    "Original-Maintainer",
    "Bugs",
    "MD5sum",
    "SHA1",
    "SHA256",
    "Homepage",
    "Multi-Arch",
    "Built-Using",
    "Supported",
    "Modaliases",
]
oneLineArrayOfStringKeys = [
    "Task",
    "Npp-Applications",
    "Pre-Depends",
    "Recommends",
    "Replaces",
    "Breaks",
    "Suggests",
    "Depends",
    "Enhances",
    "Conflicts",
    "Provides",
]


# 创建一个空的数据字典，包含所有可能的键和None作为默认值
def create_empty_data():
    data = {
        "Package": None,
        "Version": None,
        "ABIVersion": None,
        "Depends": None,
        "License": None,
        "Section": None,
        "Architecture": None,
        "Installed-Size": None,
        "Filename": None,
        "Size": None,
        "SHA256sum": None,
        "Description": None,
        "Provides": None,
        "Conflicts": None,
        "CPE-ID": None,
        "Alternatives": None,
        "Essential": None,
        "Status": None,
        "Installed-Time": None,
        "Auto-Installed": None,
        "Source": None,
        "Conffiles": None,
        "SourceName": None,
        "SourceDateEpoch": None,
    }
    for key in oneLineArrayOfStringKeys:
        data[key] = None
    for key in oneLinesStringKeys:
        data[key] = None
    for key in multiLineArrayOfStringKeys:
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
        elif line.startswith("Version:"):
            current_key = line.split(":")[0]
            version = line[len(line.split(":")[0]) + 1 :]
            data["Version"] = version.strip()
        elif line.split(":")[0] in oneLineArrayOfStringKeys:
            current_key = line.split(":")[0]
            data[line.split(":")[0]] = [
                s.strip() for s in line[len(line.split(":")[0]) + 1 :].split(",")
            ]

        elif line.split(":")[0] in oneLinesStringKeys:
            current_key = line.split(":")[0]
            data[line.split(":")[0]] = line[len(line.split(":")[0]) + 1 :].strip()

        elif line.split(":")[0] in multiLineArrayOfStringKeys:
            current_key = line.split(":")[0]
            # (current_key =="Description") = True
            # (current_key =="Conffiles") = False
            content = line[len(line.split(":")[0]) + 1 :]

            data[line.split(":")[0]] = [content.strip()]
            data[line.split(":")[0]] = list(filter(None, data[line.split(":")[0]]))

        elif (
            (current_key in multiLineArrayOfStringKeys) == True
            and len(line) >= 1
            and line[0] == " "
        ):
            if data[current_key] == None:
                data[current_key] = []
            data[current_key].append(line.strip())
            data[current_key] = list(filter(None, data[current_key]))
        elif ":" in line and re.match(r"^[A-Za-z0-9\-]+$", line.split(":")[0]):
            current_key = line.split(":")[0]
            data[line.split(":")[0]] = line[len(line.split(":")[0]) + 1 :].strip()

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

        elif line.startswith("Auto-Installed:"):
            current_key = line.split(":")[0]
            Auto_Installed = line[len(line.split(":")[0]) + 1 :]
            data["Auto-Installed"] = "yes" == Auto_Installed.strip()
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
            data["Essential"] = "yes" == Essential.strip()
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

            data["Conffiles"] = [Conffiles.strip()]
            data["Conffiles"] = list(filter(None, data["Conffiles"]))
        elif line.startswith("Description:"):
            current_key = line.split(":")[0]
            # (current_key =="Description") = True
            # (current_key =="Conffiles") = False
            description = line[len(line.split(":")[0]) + 1 :]

            data["Description"] = [description.strip()]
            data["Description"] = list(filter(None, data["Description"]))
            # assign the final description to the data dictionary.
            # This will be the same as the original text, but without the first paragraph and with newlines between paragraphs.
        elif (current_key == "Conffiles") == True and len(line) >= 1 and line[0] == " ":
            if data["Conffiles"] == None:
                data["Conffiles"] = []
            data["Conffiles"].append(line.strip())
            data["Conffiles"] = list(filter(None, data["Conffiles"]))
            pass
        else:
            if (
                (current_key == "Description") == True
                and len(line) >= 1
                and line[0] == " "
            ):
                if data["Description"] == None:
                    data["Description"] = []
                data["Description"].append(line.strip())
                data["Description"] = list(filter(None, data["Description"]))
            else:
                # print(line)
                if ":" in line:
                    if line.split(":")[0] not in oneLinesStringKeys:
                        print(line)
                    # print(line.split(":"))

                    # print(data)
                pass

        # if "SHA256sum" in data and data["SHA256sum"] != None:
        # key = data["SHA256sum"]
        # if key not in packages:
        # packages[key] = data
        # else:
        # value = packages[key]
        # d2 = merge_dict_not_None(value, data)
        # data = d2
        # packages[key] = d2
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


# 合并两个字典，只保留非None值
def merge_dict_not_None(value: dict, data: dict):
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
