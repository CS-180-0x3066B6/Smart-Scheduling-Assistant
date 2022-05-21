counter=1
for i in *.tif
do

pad=""

if [ $counter -lt 100 ]; then
pad="0"
fi

if [ $counter -lt 10 ]; then
pad="00"
fi

mv $i $pad$counter.tif
counter=$(($counter+1))
done
