#!/bin/sh


oldDir=$(pwd)

cd $(dirname $0)


######################

target="../templates.py"

######################

printf '\n' > $target

for builder in */build.sh
do
	echo "running $builder ... "

	printf $(basename $(dirname $builder)) >> $target
	printf ' = """' >> $target

	$builder 1>> $target

	printf '"""' >> $target

done

printf '\n'  >> $target

#####################

cd $oldDir
