#!/bin/sh

GIT_COMMNAD="git"
MAVEN_COMMNAD="mvn"

if ! type "$GIT_COMMNAD" > /dev/null; then
    echo "$GIT_COMMNAD command doesn't exist! Please install git here"
    exit 0
fi
if ! type "$MAVEN_COMMNAD" > /dev/null; then
    echo "$MAVEN_COMMNAD command doesn't exist! Please install maven here"
    exit 0
fi

echo "getting copy of azure-media-processor-java from github...."
git clone https://github.com/yokawasa/azure-media-processor-java.git
cd azure-media-processor-java

echo "try compiling the project and see if it works...."
mvn compile

echo "done!"
exit 0
