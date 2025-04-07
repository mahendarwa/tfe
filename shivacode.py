#!/bin/bash

set -e

BUILD="$1"
WORKSPACE=$(pwd)

echo "Reading update.xml"
updatexmlresults=$(cat ./Teradata/src/update.xml)
folders=$(ls -d ./Teradata/src/*/)
deployfiles=()

while IFS= read -r line; do
  if [[ "$line" == *"<include"* ]]; then
    deployfile=$(echo "$line" | sed -e "s/.*file=//g" -e "s/[\"']//g" -e "s/>.*//g" -e "s/relativeToChangelogFile=true//g" | tr -d '<>/')
    deployfiles+=("$deployfile")
  fi
done <<< "$updatexmlresults"

rm -rf "${WORKSPACE}/PACKAGE"
for folder in $folders; do
  foldername=$(basename "$folder")
  mkdir -p "${WORKSPACE}/PACKAGE/src/${foldername}"
done

cp ./Teradata/pom.xml "${WORKSPACE}/PACKAGE/pom.xml"
cp ./Teradata/src/update.xml "${WORKSPACE}/PACKAGE/src/update.xml"

echo "Total include files: ${#deployfiles[@]}"

for file in "${deployfiles[@]}"; do
  if [[ "$file" != *"REPLACE WITH"* ]]; then
    dir=$(dirname "$file")
    mkdir -p "${WORKSPACE}/PACKAGE/src/${dir}"
    cp "./Teradata/src/${file}" "${WORKSPACE}/PACKAGE/src/${file}"
  else
    echo "Error: update.xml contains invalid file path: $file"
    exit 1
  fi
done

if grep -q -E "(PROC|Views)" <<< "${deployfiles[*]}"; then
  mkdir -p "${WORKSPACE}/PACKAGE/src/PVS"
  cp ./Teradata/src/PVS/pvs.sql "${WORKSPACE}/PACKAGE/src/PVS/pvs.sql"
fi

cp ./TD_INFA_CONTROL_FILE.Properties "${WORKSPACE}/PACKAGE/src/TD_INFA_CONTROL_FILE.Properties"

tar --exclude='.git' -czvf odms-teradata-release.tgz -C "${WORKSPACE}/PACKAGE" .

mvn -s /opt/jenkins/tools/apache-maven-3.3.9/conf/settings_https_artifactory.xml \
  -Durl=${ARTIFACTORY_URL} \
  -DgeneratePom=true \
  -Dfile=./odms-teradata-release.tgz \
  -DgroupId=com.cigna.healthspring.teradata \
  -DrepositoryId=Release \
  -Dversion=${BUILD} \
  -DartifactId=odms-teradata-release \
  deploy:deploy-file || echo "Ignore mvn exit code"

echo "Build uploaded: ${BUILD}"
echo "${ARTIFACTORY_URL}/com/cigna/healthspring/teradata/odms-teradata-release/${BUILD}"
