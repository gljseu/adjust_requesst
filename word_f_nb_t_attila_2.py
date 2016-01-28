# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

online_provider = ["app_homepage", "nm_listing_poi", "nuomi_listing", "nuomi_keywords", "keywords_poi", "nm_listing_emp", "keywords_emp", "emp_detail", "nm_list_emp_poi", "nm_deal_to_poi", "poigroupon", "understand", "nm_hot_deal", "nm_uiituan", "nm_deal_monitor", "nm_poi_to_deal", "keyword_prophet", "poi_detail", "nm_pc_hot_home", "poi_detail_list", "goods_facet", "nm_yingxiao", "range_detail", "gense_gd"]

def parse_and_putinto_file(infile, outfile):    
    handler = open(infile, 'r')
    out_handler = open(outfile, 'a')
    index = 0
    for line in open(infile):        
        index += 1

        try:
            line = handler.readline()
            provider, param = parse_line(line)

            param = param.strip()
            #temp
            #param = param.strip().replace(' ', '')
            if ('' == provider) or (not provider in online_provider):
                continue

            if '",,' in param or '", ,' in param:
                continue
            #if '",,' in param:
            #    continue
            ''' 
            if ("wifi" in param) and ("wifi_conn" in param):                
                param = param.decode("utf-8") 
                param_arr = json.loads(param, encoding="utf-8")
                param_arr["wifi"] = json.dumps(param_arr["wifi"], ensure_ascii = False)
                param_arr["wifi_conn"] = json.dumps(param_arr["wifi_conn"], ensure_ascii = False)
                try: 
                    param = json.dumps(param_arr, ensure_ascii=False)
                except Exception:
                    param = json.dumps(param_arr)
            '''
        except Exception:
            line2 = line.strip("\n")
            print line2
            continue

        out_handler.write(provider + "\t0\n")
        out_handler.write(param + "\n")

    handler.close()
    out_handler.close()

def parse_line(line):
    line = line.strip()
    segments = line.split("\t")
    head = json.loads(segments[1])
    provider = head['provider']

    param = segments[2]
    #for json is {x,,y}
    #try:
    #    temp = json.loads(param)
    #except Exception:
    #    temp = json.loads(param, ensure_ascii=False)

    return provider, param

#delete func
def assemble_req(provider, param):
    first_line = provider + "\t0\n"
    second_line = param + "\n"
    req = first_line + second_line
    return req

def main(argv):
    if 3 != len(argv):
        print 'Usage: python word_f_nb_t_attila.py infile outfile'
        return 1

    parse_and_putinto_file(argv[1], argv[2])
    return 0

if '__main__' == __name__:
    print sys.argv
    main(sys.argv)
