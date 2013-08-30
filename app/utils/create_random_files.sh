NUMBER_OF_FILES=1000
SIZE_OF_FILES=1024 # In bytes
cd example_files
rm *
dd if=/dev/urandom of=masterfile bs=1 count=$(($NUMBER_OF_FILES * $SIZE_OF_FILES))
split -b $NUMBER_OF_FILES -a 10 masterfile
cd ..
python change_times.py
