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

echo "Check the java version that maven use in building and adjust it to pom.xml"
MARVEN_JAVA_VESION=`mvn --version |grep 'Java version' |awk '{print $3}' | cut -d'.' -f 1,2`
cp pom.xml pom.xml.org
if [ ${MARVEN_JAVA_VESION} != "1.8" ];
then
cat pom.xml.org | sed s,"<java.version>1.8</java.version>","<java.version>${MARVEN_JAVA_VESION}</java.version>",g  > pom.xml
fi

echo "try compiling the project and see if it works...."
mvn compile

echo "done!"
exit 0
