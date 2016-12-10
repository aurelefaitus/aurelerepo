#!/bin/bash
cp ../ExampleLoad.jmx .
sed -i '/<?xml/,/<hashTree>/d' ExampleLoad.jmx
sed -i '/<TestPlan/,/<hashTree>/d' ExampleLoad.jmx
sed -i '/<ThreadGroup/,/<hashTree>/d' ExampleLoad.jmx
sed -i '$ d' ExampleLoad.jmx
sed -i '$ d' ExampleLoad.jmx
sed -i '$ d' ExampleLoad.jmx
#sed -i 's/        /      /g' ExampleLoad.jmx

cat TFHeader > ExampleLoadTF2.jmx
cat ExampleLoad.jmx >> ExampleLoadTF2.jmx
cat TFFooter >> ExampleLoadTF2.jmx

