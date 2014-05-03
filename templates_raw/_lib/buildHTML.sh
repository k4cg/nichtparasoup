#!/bin/sh



######

selfPath=$(cd $(dirname $0); pwd)


path2lib=$selfPath

path2lib_yuic="$path2lib/yuicompressor-2.4.8.jar"
path2lib_buildHTML="$path2lib/buildHTMLfromParts.py"

stripOnBuildMarker="@striponbuild"

###########

oldDir=$(pwd)

if [ $# -ge 1 ];
then
	cd $1
fi

#############

base=$(pwd)

targetPath="$base/built/"

targetFile="$targetPath/built.html"

mainTpl="$(basename $base).html"

##########


if java -version &>/dev/null
then
	hasJava=1
else
	hasJava=0
	echo "no java found - will copy instead of compressing" >&2
fi



for css in $(find . -type f -maxdepth 1 -iname "*.css")
do
	sed -e "s/^.*$stripOnBuildMarker.*$//g" $css  1> $targetPath/$css
	if [ $hasJava -eq 1 ]
	then
		mv $targetPath/$css $targetPath/$css.raw
		java -jar $path2lib_yuic --line-break 0 --type css --charset utf-8  < $targetPath/$css.raw  1> $targetPath/$css
	fi
done

for js in $(find . -type f -maxdepth 1 -iname "*.js")
do
	sed -e "s/^.*$stripOnBuildMarker.*$//g" $js  1> $targetPath/$js
	if [ $hasJava -eq 1 ]
	then
		mv $targetPath/$js $targetPath/$js.raw
		java -jar $path2lib_yuic --line-break 0 --type js --charset utf-8  < $targetPath/$js.raw  1> $targetPath/$js
	fi
done


cp $mainTpl $targetPath/$mainTpl


$path2lib_buildHTML $targetPath/$mainTpl 1>$targetFile

cat $targetFile

########

cd $oldDir;