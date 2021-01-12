from __future__ import division
import sys
import collections
import joblib
import re


def preprocessing(OInfile1):
    infile=open(OInfile1,'r')
    Outfile='result.txt'
    outfile=open(Outfile,'w')


    Hash_Dict=collections.OrderedDict()

    for line in infile:
        l1 = line.strip().split('\t')
        Hash_Dict.setdefault(l1[1],l1[2])

    for k,v in Hash_Dict.items():
        outfile.write(str(21) +'\t'+k +'\t'+ v +'\n')

    infile.close()
    outfile.close()


def getFeature():
    Infile1=open('tumor.pileup','r')
    Infile2=open('result.txt','r')

    Outfile = open('fea.txt','w')

    Inline1=Infile1.readline()
    info=Inline1.strip().split('\t')
    Inline2=Infile2.readline()
    Inline2_list=Inline2.strip().split('\t')

    while 1:
        if len(info) < 5:
            Inline1 = Infile1.readline()
            if not Inline1:
                break;
            info = Inline1.strip().split('\t')
            continue
        if int(info[1])==int(Inline2_list[1]):
            chrs = info[0]  ###chr
            pos = info[1]  ###pos
            ref = info[2]  ###ref
            depth = float(info[3])  ###depth
            base = info[4]  ###base
            quality = info[5]  ###quality
            lists = [0.0]
            lists = lists * 12

            Outfile.write(pos)  ####pos
            Outfile.write('\t')

            lists[0] = depth
            j = 0
            base = re.sub(r'\d[A-Z,a-z]+', "", base)
            for i in range(len(base)):
                if base[i].isdigit():
                    continue
                elif base[i - 1].isdigit():
                    continue
                elif base[i - 1] == "^":
                    continue
                elif base[i] == '.':
                    lists[4] = lists[4] + 1  # 匹配到正链的个数
                    lists[8] = lists[8] + (ord(quality[j]) - 33)  # 正链匹配的质量
                    j = j + 1
                elif base[i] == ',':
                    lists[5] = lists[5] + 1  # 负链匹配的个数
                    lists[9] = lists[9] + (ord(quality[j]) - 33)  # 负链匹配的质量
                    j = j + 1
                elif base[i] == 'A' or base[i] == 'C' or base[i] == 'T' or base[i] == 'N' or base[i] == 'G':
                    lists[6] = lists[6] + 1  # 正链错配的个数
                    lists[10] = lists[10] + (ord(quality[j]) - 33)  # 正链错配的质量
                    j = j + 1
                elif base[i] == 'a' or base[i] == 'c' or base[i] == 't' or base[i] == 'n' or base[i] == 'g':
                    lists[7] = lists[7] + 1  # 负链错配的个数
                    lists[11] = lists[11] + (ord(quality[j]) - 33)  # 负链错配的质量
                    j = j + 1
                else:
                    continue
            if lists[0] != 0:
                lists[1] = lists[6] + lists[7]  # 正链错配总数＋负链错配总数
                lists[2] = lists[1] / lists[0]  # AF
                lists[3] = (lists[8] + lists[9] + lists[10] + lists[11]) / lists[0]  # 平均匹配质量值

            for i in range(0, 4):
                Outfile.write(str(lists[i]))
                Outfile.write('\t')
            Outfile.write( "\n")


            Inline1 = Infile1.readline()
            if not Inline1:
                break
            Inline2 = Infile2.readline()
            if not Inline2:
                break
            info = Inline1.strip().split('\t')
            Inline2_list = Inline2.strip().split('\t')
        elif int(info[1])>int(Inline2_list[1]):
            Inline2 = Infile2.readline()
            if not Inline2:
                break
            Inline2_list = Inline2.strip().split('\t')
        else:
            Inline1 = Infile1.readline()
            if not Inline1:
                break
            info = Inline1.strip().split('\t')

    Infile1.close()
    Infile2.close()
    Outfile.close()


def feaAddCN(OInfile2):
    infile_1 = open(OInfile2, 'r')
    infile_2 = open('fea.txt', 'r')

    Outfile = 'feaCN.txt'
    outfile = open(Outfile, 'w')

    file_list = []
    for line2 in infile_2:
        line2 = line2.strip().split('\t')
        file_list.append(line2)  # 把特征信息存入一个大的列表里
    for line1 in infile_1:
        if not line1:
            break
        line1 = line1.strip().split('\t')
        for i in range(len(file_list)):
            if int(file_list[i][0]) in range(int(line1[1]), int(line1[2]) + 1):
                file_list[i].append(line1[3])

    for i in range(len(file_list)):
        if len(file_list[i]) < 6:
            file_list[i].append('2')

    # 此时file_list=[]中的顺序是：pos、RD、总的错配数、AF、平均匹配质量、CN(共6列)
    for i in range(len(file_list)):
        strline = '\t'.join(file_list[i])
        outfile.write(strline + '\n')

    infile_1.close()
    infile_2.close()
    outfile.close()

def trained_SVM():
    X_Data = []
    Y_Data = []
    pos = []
    # 读取数据
    data = open("feaCN.txt", 'r')
    for line in data:
        x = []
        linex = line.strip().split('\t')
        pos.append(linex[0])
        # 加入5个特征信息
        for i in range(1, len(linex)):
            x.append(eval(linex[i]))
        X_Data.append(x)

    clf = joblib.load("SVM_model.m")
    y_pred = clf.predict(X_Data)

    outfile = open('svmSomaticresult.txt', 'w')
    for i in range(len(y_pred)):
        if y_pred[i] == 0:
            outfile.write(str(pos[i]) + '\t' + str(y_pred[i]) + '\n')

    data.close()
    outfile.close()


if __name__ == "__main__":
    OInfile1 = sys.argv[1]
    OInfile2 = sys.argv[2]
    preprocessing(OInfile1)
    getFeature()
    feaAddCN(OInfile2)
    trained_SVM()
