MAF=$1
ID=$2
STUB=$3
REMOVE=$4
MAFX=$5

echo "ID:"
echo $ID
echo "MAF:"
echo $MAF
echo "STUB:"
echo $STUB
echo "REMOVE:"
echo $REMOVE
echo "MAFX:"
echo $MAFX

if [ "${REMOVE,,}" = "remove" ]; then
	echo "REMOVE FAKE PROTEIN CHANGE, restore X"
	python /opt/src/fake_protien_change.py -m $MAF -d $ID -s $STUB -r -x $MAFX
else
    echo "MAKE FAKE PROTEIN CHANGE"
	python /opt/src/fake_protien_change.py -m $MAF -d $ID -s $STUB 
fi

ls $ID.*.maf

