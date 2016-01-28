# -*- coding: utf-8 -*-
import json
import argparse
import commands
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

from parse_conf import *

def load_conf(catg, conf):
    confHandler = INI_Conf(conf)
    catgConf = confHandler.get_values(catg)
    ratioKey = []
    ratio = []
    ratioTemp = []
    for catgKey in catgConf:
        ratioKey.append(str(catgKey))
        ratioTemp.append(int(catgConf[catgKey]))

    #ratio做按百分比计算
    su = sum(ratioTemp)
    for eachRatio in ratioTemp:
        temp = eachRatio * 10 / su
        ratio.append(int(temp))

    return {catg: ratioKey}, {catg: ratio}


def split_by_catg(catgKeys, oriReqSet):
    catg = (catgKeys.keys())[0]
    catgSplitHandler = {}
    splitFile = []
    for catgKey in catgKeys[catg]:
        temp = open(catg + '_' + catgKey, 'a') 
        catgSplitHandler[catgKey] = temp
        splitFile.append(catg + '_' + catgKey)

    reqHandler = open(oriReqSet)
    #需要对奇偶做判断
    index = 0
    lineTemp = ''
    parseFlag = True
    while True:
        line = reqHandler.readline().strip()
        if not line:
            break

        if 0 == index % 2:
            lineTemp = line
            index += 1
            continue

        try:
            line = line.decode("utf-8", "ignore")
            lineArr = json.loads(line)
        except Exception, ex:
            try:
                handlerTemp = open('temp', 'w')
                handlerTemp.write(line)
                handlerTemp.close()
                #过滤掉控制字符 使用shell命令比较简单，python没找到怎么过滤            
                #line = os.system('cat temp | col -b -l 1')
                (status, line) = commands.getstatusoutput('cat temp | col -b -l 1')
                lineArr = json.loads(line)
            except Exception:
                print "err=" + str(ex) + "; line=" + str(index+1) + " can't be parsed"
                print line
                parseFlag = False

        if catg in lineArr and True == parseFlag:
            #转为string后再做判断
            reqCatg = str(lineArr[catg])
            if reqCatg in catgKeys[catg]:
                catgSplitHandler[reqCatg].write(lineTemp + "\n "+ line + "\n")

        lineTemp = ''
        index += 1
        parseFlag = True

    reqHandler.close()
    for catgKey in catgKeys[catg]:
        catgSplitHandler[catgKey].close()

    return splitFile

#对切分文件按照比例重新组合
def merge_by_split(catgRatio, splitFile, destMergeFile):
    ratio = (catgRatio.values())[0]
    #re assemble dict
    splitNum = len(ratio)
    if splitNum != len(splitFile):
        print 'ratio conf count != split_file count'
        return -1

    #splitFile process Handler
    splitFileHandler = {}
    splitRatio = {}    
    for i in range(0, splitNum):
        splitRatio[splitFile[i]] = ratio[i]
        temp = open(splitFile[i])
        splitFileHandler[splitFile[i]] = temp

    #destMergeFile process Hander
    destMergeFileHandler = open(destMergeFile, 'a')

    #每次读取的临时数据
    temp = ''
    #文件被读完的标志
    finishTag = False
    while True:
        if True == finishTag:
            break

        for eachSplitFileName in splitFileHandler:
            #每次读取的行数
            lineNum = int(splitRatio[eachSplitFileName])
            for i in range(2*lineNum):
                line = splitFileHandler[eachSplitFileName].readline().strip()
                if not line:
                    finishTag = True
                    break
                temp += line + "\n"

            if True == finishTag:
                temp = ''
                break
       
        destMergeFileHandler.write(temp)
        #重置temp
        temp = ''

    for splitFileName in splitFileHandler:
        splitFileHandler[splitFileName].close()

    destMergeFileHandler.close()

    return 0

def adjust_catg(catg, adjustconf, srcReqSet, destReqSet):
    ratioKey, ratio = load_conf(catg, adjustconf)
    splitFile = split_by_catg(ratioKey, srcReqSet)
    res = merge_by_split(ratio, splitFile, destReqSet)
    return res


if '__main__' == __name__:
    parser = argparse.ArgumentParser(description='Get catgKey, src and dest file.')
    parser.add_argument('-t', '--catg_type', type=str, nargs='*', help='channel_type')
    parser.add_argument('-c', '--catg_conf', type=str, nargs='*', help='adjust.conf')
    parser.add_argument('-s', '--src_file', type=str, nargs='*', help='src.data')
    parser.add_argument('-d', '--dest_file', type=str, nargs='*', help='dest.data')
    args = parser.parse_args()
    #获取请求参数，少一个都不行
    try:
        catg = args.catg_type[0]
        conf = args.catg_conf[0]
        src  = args.src_file[0]
        dest = args.dest_file[0]
    except Exception:
        print "Usage: python adjust.py -t channel_type -c adjust.conf -s src.data -d dest.data\n"
        exit(0)

    res = adjust_catg(catg, conf, src, dest)
    if 0 == res:
        print "Finished!\n"
    else:
        print "ERROR!\n"
