#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from zipfile import ZipFile
import os
import sys


def parse_dependency_info(dependency_info):
    parts = dependency_info.split('---NOTICE----------------------------------------------------------')
    if len(parts) < 2:
        raise ValueError("The '---NOTICE----------------------------------------------------------' separator and the first part are missing.")

    filename_part = parts[0].strip()

    part2_parts = parts[1].split('---LICENSE---------------------------------------------------------', 1)
    notice_part = part2_parts[0].rstrip()

    license_part = None
    if len(part2_parts) > 1 and part2_parts[1].strip() != '':
        license_part = part2_parts[1].rstrip()

    return filename_part, notice_part, license_part


def load_dependency_maps():
    base_directory = 'dependency-maps'

    dependency_maps = {}

    for root, _, files in os.walk(base_directory):
        for filename in files:
            if filename.startswith('.'):
                continue  # Skip hidden files

            path_parts = os.path.relpath(root, base_directory).split(os.path.sep)
            if len(path_parts) == 0:
                continue  # Skip if the relative path is empty

            license_type = path_parts[0]  # The first part of the relative path is the license type

            # Create the inner map if the licenseType doesn't exist in the dependency_maps
            if license_type not in dependency_maps:
                dependency_maps[license_type] = {}

            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                # False parameter here is for convenience, and might not be the nicest thing.
                # Once we've found a matching bundle, we are going to switch that to True,
                # and we are going to use this info to know whether we need to add the info
                # to the NOTICE and LICENSE files.
                dependency_maps[license_type][filename] = parse_dependency_info(file_content)

    return dependency_maps

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return file_content

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main(nar_path, output_path):
    with ZipFile(nar_path, 'r') as zipObj:
        listOfFiles = zipObj.namelist()

    bundleDir = 'META-INF/bundled-dependencies/' 

    bundledDeps = [pathInNar.replace(bundleDir, '', 1) for pathInNar in listOfFiles if pathInNar.startswith(bundleDir)]
    # bundledDeps contains an empty string (root) that's why checking x is not empty
    third_party_bundles = [x for x in bundledDeps if x and not x.startswith('nifi-')]

    third_party_bundles.sort()

    dependency_maps = load_dependency_maps()

    license_builder = read_file('static/asf-license')
    notice_builder = read_file('static/asf-notice')

    subcomponents_appended = False
    used_headers = []

    debug_log = 'Licensing info found for these bundles:'

    for license_type, dependency in dependency_maps.items():
        for dependency_id, dependency_info in dependency.items():
            for third_party_bundle in third_party_bundles:
                if third_party_bundle.startswith(dependency_id):
                    debug_log += '\n  - ' + dependency_id + ':'

                    if license_type not in used_headers:
                        used_headers.append(license_type)
                        notice_builder += '\n\n' + read_file('static/notice-headers/' + license_type)

                    notice_builder += '\n' + dependency_info[1]
                    debug_log += ' NOTICE'

                    opt_license = dependency_info[2]
                    if opt_license:
                        if not subcomponents_appended:
                            license_builder += '\n' +read_file('static/asf-license-subcomponents')
                            subcomponents_appended = True

                        debug_log += ' and LICENSE'
                        license_builder += '\n' + opt_license

                    debug_log += ' found'

                    if dependency_info[0] != third_party_bundle:
                        debug_log += ', WARNING: version mismatch'

                    third_party_bundles.remove(third_party_bundle)

    if third_party_bundles:
        debug_log += '\nLicensing info not found for these bundles:'
        for not_found in third_party_bundles:
            debug_log += '\n  - ' + not_found

    print(debug_log)

    write_file(output_path + '/LICENSE', license_builder)
    write_file(output_path + '/NOTICE', notice_builder)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 linot.py <path_to_nar> <path_to_output>")
    else:
        nar_path = sys.argv[1]
        output_path = sys.argv[2]
        main(nar_path, output_path)

