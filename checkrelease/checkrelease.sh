#!/bin/sh

BGreen='\033[1;32m'       # Green
BRed='\033[1;31m'         # Red
Color_Off='\033[0m'       # Text Reset

mvn -v > /buildresult/mvnversion

echo -e "${BGreen}--- validating NiFi release ---${Color_Off}"
wget https://dist.apache.org/repos/dist/dev/nifi/KEYS
gpg --import KEYS

echo "${BGreen}--- downloading artifacts ---${Color_Off}"
wget https://dist.apache.org/repos/dist/dev/nifi/nifi-$1/nifi-$1-source-release.zip
wget https://dist.apache.org/repos/dist/dev/nifi/nifi-$1/nifi-$1-source-release.zip.asc
wget https://dist.apache.org/repos/dist/dev/nifi/nifi-$1/nifi-$1-source-release.zip.sha256
wget https://dist.apache.org/repos/dist/dev/nifi/nifi-$1/nifi-$1-source-release.zip.sha512

echo "${BGreen}--- verifying signatures ---$Color_Off"
gpg --verify -v nifi-$1-source-release.zip.asc

echo "${BGreen}--- verifying hashes ---${Color_Off}"
if [ $(shasum -a 256 nifi-$1-source-release.zip | awk '{ print $1 }') = $2 ]; then
  echo "${BGreen}--- sha 256 -> OK ---${Color_Off}"
else
  echo "${BRed}--- sha 256 -> NOK ---${Color_Off}"
  exit 1
fi

if [ $(shasum -a 512 nifi-$1-source-release.zip | awk '{ print $1 }') = $3 ]; then
  echo "${BGreen}--- sha 512 -> OK ---${Color_Off}"
else
  echo "${BRed}--- sha 512 -> NOK ---${Color_Off}"
  exit 1
fi

echo "${BGreen}--- unzipping source ---${Color_Off}"
unzip -q nifi-$1-source-release.zip

echo "${BGreen}--- building project ---${Color_Off}"
cd nifi-$1
mvn clean install -e -Pcontrib-check

echo "${BGreen}--- collecting assembly and logs ---${Color_Off}"
cp -r ./nifi-assembly/target /buildresult/assembly
mkdir /buildresult/testresult
find . -name 'surefire-reports' -exec cp -r --preserve=timestamps --parents \{\} /buildresult/testresult \;
