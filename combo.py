import sys
import codecs
for k in range(len(sys.argv) - 1):
    input_file = open("C:\\Users\\Luke\\Desktop\\" + sys.argv[k + 1] + ".csv", encoding="utf-8")
    comb_file = codecs.open("C:\\Users\\Luke\\Desktop\\combo.csv", "w+", "utf-8")
    temp = ''
    if k == 0:
        comb_file.write("Author,Citation_Count,Year" + "\n")
    for line in input_file:
        temp = line.split(",")
        leng = len(temp)
        if len(temp[leng - 2]) > 0 and len(temp[leng - 1]) > 0:
            comb_file.write(sys.argv[k + 1] + "," + temp[leng - 2] + "," + temp[leng - 1])
    input_file.close()
    comb_file.close()
arr1 = [0] * 50
arr2 = [0] * 50
f = open("C:\\Users\\Luke\\Desktop\\combo.csv", encoding="utf-8")
next(f)
for line in f:
    temp = line.split(",")
    index = 2019 - int(temp[1])
    if temp[0] == sys.argv[1]:
        arr1[index] += int(temp[2])
f.close()
f = codecs.open("C:\\Users\\Luke\\Desktop\\combo1.csv", "a", "utf-8")
for z in range(len(arr1)):
    if arr1[z] > 0:
        f.write(sys.argv[1] + "," + str(2019 - z) + "," + str(arr1[z]) + "\n")
for z in range(len(arr1)):
    if arr2[z] > 0:
        f.write(sys.argv[2] + "," + str(2019 - z) + "," + str(arr2[z]) + "\n")
f.close()
