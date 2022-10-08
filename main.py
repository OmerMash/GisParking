import os
import json
import time
from pathlib import Path
import os.path
import pandas as pd
import shutil
import csv
import filecmp


def update_changes(data_file, data_file_1, case):
    global lst
    lst = []
    df = pd.read_csv(data_file, header=None)
    df1 = pd.read_csv(data_file_1, header=None)
    if case == 'Park_5':
        rows = [df.at[0, 1], df.at[1, 1], df.at[2, 1], df.at[3, 1]]
        rows1 = [df1.at[0, 1], df1.at[1, 1], df1.at[2, 1], df1.at[3, 1]]
        place = 0
        for row, row1 in zip(rows, rows1):
            df.at[place, 1] = row1
            lst.append(row1)
            place += 1
    else:   # ParkSpaces_6 case
        place = 0
        rows = []
        rows1 = []
        while place < df.__len__():
            rows.append([df.at[place, 1]])
            rows1.append([df1.at[place, 1]])
            place += 1
        place = 0
        for row, row1 in zip(rows, rows1):
            df.at[place, 1] = row1
            lst.append(row1)
            place += 1
        place = 0
        for row, row1 in zip(rows, rows1):
            df.at[place, 1] = row1
            lst.append(row1)
            place += 1
    return lst


def even_parks(park5, park6):
    p1_counter = 0
    p2_counter = 0
    p3_counter = 0
    p4_counter = 0
    with open(park5) as f_park5:
        with open(park6) as f_park6:
            p5 = json.load(f_park5)
            p6 = json.load(f_park6)
            for feature in p6["features"]:
                if feature["properties"]["ParkId"] == '1' and feature["properties"]["taken"] == '1':
                    p1_counter += 1
                elif feature["properties"]["ParkId"] == '2' and feature["properties"]["taken"] == '1':
                    p2_counter += 1
                elif feature["properties"]["ParkId"] == '3' and feature["properties"]["taken"] == '1':
                    p3_counter += 1
                elif feature["properties"]["ParkId"] == '4' and feature["properties"]["taken"] == '1':
                    p4_counter += 1
            for feature in p5["features"]:
                if feature["properties"]["id"] == '1':
                    feature["properties"]["takenSpace"] = p1_counter
                    feature["properties"]["emptySpace"] = str(int(feature["properties"]["totalSpace"]) - int(feature["properties"]["takenSpace"]))
                elif feature["properties"]["id"] == '2':
                    feature["properties"]["takenSpace"] = p2_counter
                    feature["properties"]["emptySpace"] = str(int(feature["properties"]["totalSpace"]) - int(feature["properties"]["takenSpace"]))
                elif feature["properties"]["id"] == '3':
                    feature["properties"]["takenSpace"] = p3_counter
                    feature["properties"]["emptySpace"] = str(int(feature["properties"]["totalSpace"]) - int(feature["properties"]["takenSpace"]))
                elif feature["properties"]["id"] == '4':
                    feature["properties"]["takenSpace"] = p4_counter
                    feature["properties"]["emptySpace"] = str(int(feature["properties"]["totalSpace"]) - int(feature["properties"]["takenSpace"]))
                content = str(p5).replace("'", '"')
    with open(park5, "w") as outfile:
        outfile.write(content)


def update_json_values(j, updates, case):
    with open(j) as f:
        content_file = json.load(f)
        place = 0
        if case == 'ParkSpaces_6':
            left_str1 = '["[[[{'
            left_str2 = '["[[[[{'
            right_str1 = '}]]]"]'
            right_str2 = '}]]]]"]'
            for feature in content_file['features']:
                feature['properties'] = updates[place]
                content_file['features'][place]['properties'] = feature['properties']
                place += 1
            a = str(content_file).replace(left_str1, "{").replace(right_str1, "}").replace(left_str2, "{").replace(right_str2, "}")
            content = json.dumps(a, indent=4).replace("'", "\"").replace('\\', '').replace('["{"id"', '{"id"').replace('"}"]', '"}')
            with open(j, "w") as outfile:
                outfile.write(content)
        else:
            for feature in content_file['features']:
                feature['properties'] = updates[place]
                content_file['features'][place]['properties'] = feature['properties']
                place += 1
            s = str(content_file).replace("\"", "")
            content = json.dumps(s, indent=4).replace("'", "\"")
            with open(j, "w") as outfile:
                outfile.write(content)


def csv_to_json(csvFilePath, jsonFilePath):
    data = {}  # create a dictionary
    with open(csvFilePath, encoding='utf-8') as csvf:  # Open a csv reader called DictReader
        csv_reader = csv.DictReader(csvf)
        for rows in csv_reader:  # Convert each row into a dictionary and add it to data
            key = rows['Feature']
            data[key] = rows
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
                jsonf.write(json.dumps(data, indent=4))


def rename_file(old_name, new_name):        # rename file and put it in place
    os.rename(old_name, new_name)


def changed(file_a, file_b):
    if filecmp.cmp(file_a, file_b):
        return False
    return True


def line_prepender(result, line):
    with open(result, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def write_csv_file(data, data_file_name):
    data_file = open(data_file_name, 'w')  # open a file for writing
    csv_writer = csv.writer(data_file)  # create the csv writer object
    feature_data = data['features']
    for feature in feature_data:
        csv_writer.writerow(feature.values())  # Writing data of CSV file
    data_file.close()


def read_json(j):
    data = json.load(open(j))
    return data


def change_extension(path, to):     # change json extension to js extension: js extension marks that the content of the file should be script following javascript syntax, and also human-readable.
    p = Path(path)
    if to == 'json':
        p.rename(p.with_suffix('.json'))
    elif to == 'js':
        p.rename(p.with_suffix('.js'))
    elif to == 'csv':
        p.rename(p.with_suffix('.csv'))


def remove_prefix(file, line):
    with open(file, 'r+') as f:
        content = f.read()
        new_content = content.replace(line, "", 1).lstrip()
        f.seek(0)
        f.truncate()
        f.write(new_content)


def remove_suffix(file):        # remove last character of file
    with open(file, 'r+') as f:
        f.seek(0, 2)  # move the cursor to the end of the file
        size = f.tell()
        f.truncate(size - 1)


def get_files(file1, file2):
    shutil.copyfile(file1, '/Users/admin/PycharmProjects/GisParking/Park_5.js')
    shutil.copyfile(file2, '/Users/admin/PycharmProjects/GisParking/ParkSpaces_6.js')


if __name__ == '__main__':
    print("WELCOME TO THE PARKING-LOT MANAGEMENT SOFTWARE")
    print("this software updates regularly for parking-lot changes and presents a real-time state of the parking-lots")

    # get QGIS json data files
    get_files('/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/Park_5.js',
              '/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/ParkSpaces_6.js')

    # remove prefix to get legal json file contents
    remove_prefix('/Users/admin/PycharmProjects/GisParking/Park_5.js', 'var json_Park_5 = ')
    remove_prefix('/Users/admin/PycharmProjects/GisParking/ParkSpaces_6.js', 'var json_ParkSpaces_6 = ')

    # change files extension from .js to .json
    change_extension('/Users/admin/PycharmProjects/GisParking/Park_5.js', 'json')
    change_extension('/Users/admin/PycharmProjects/GisParking/ParkSpaces_6.js', 'json')

    # load json files into pandas object
    json1 = read_json('Park_5.json')
    json2 = read_json('ParkSpaces_6.json')

    # duplicate files for change detecting comparison
    write_csv_file(json1, 'data_file.csv')
    write_csv_file(json1, 'data_file1.csv')
    write_csv_file(json2, 'data_file2.csv')
    write_csv_file(json2, 'data_file3.csv')

    while 1:    # detect changes and update app respectively
        # ParkSpaces_6 handling
        if changed('/Users/admin/PycharmProjects/GisParking/data_file2.csv', '/Users/admin/PycharmProjects/GisParking/data_file3.csv'):
            print('change detected!')
            updates_list = update_changes('/Users/admin/PycharmProjects/GisParking/data_file2.csv', '/Users/admin/PycharmProjects/GisParking/data_file3.csv', 'ParkSpaces_6')
            shutil.copyfile('data_file3.csv', 'data_file2.csv')
            update_json_values('ParkSpaces_6.json', updates_list, 'ParkSpaces_6')
            remove_prefix('ParkSpaces_6.json', "\"")
            remove_suffix('ParkSpaces_6.json')
            shutil.copyfile('ParkSpaces_6.json', 'tmpPark_6.json')        # keep original, export copy
            line_prepender('tmpPark_6.json', 'var json_ParkSpaces_6 = ')
            change_extension('tmpPark_6.json', 'js')
            rename_file('tmpPark_6.js', '/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/ParkSpaces_6.js')  # export file 1: send updated json to data folder to replace old file
            updates_list.clear()

            # Park_5 handling
            updates_list = update_changes('/Users/admin/PycharmProjects/GisParking/data_file.csv', '/Users/admin/PycharmProjects/GisParking/data_file1.csv', 'Park_5')
            shutil.copyfile('data_file1.csv', 'data_file.csv')      # update csv data_file to be equal to data_file1 for future comparisons on main while loop
            update_json_values('Park_5.json', updates_list, 'Park_5')        # update json file Park_5.json with the specific values that has changed
            remove_prefix('Park_5.json', "\"")
            remove_suffix('Park_5.json')
            even_parks('Park_5.json', 'ParkSpaces_6.json')
            shutil.copyfile('Park_5.json', 'tmpPark_5.json')        # keep original, export copy
            line_prepender('tmpPark_5.json', 'var json_Park_5 = ')
            change_extension('tmpPark_5.json', 'js')
            rename_file('tmpPark_5.js', '/Users/admin/Desktop/Omer/Study/Year D/Summer Semester/GIS/latest/HitParking0.2/data/Park_5.js')  # export file 1: send updated json to data folder to replace old file
            updates_list.clear()

        time.sleep(5)   # sleep between loop rounds
