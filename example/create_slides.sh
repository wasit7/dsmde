jupyter nbconvert $(find . -name '*.ipynb') --to slides
rm ./tutorials/*
mv *.html ./tutorials