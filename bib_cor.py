## This script aims to unify the format of .bib for vision and robotics
## Recommend that the user prepare a new .bib for each paper writing, which is easy to check  
## Unified standars:
## 1. title case
## 2. add 'Proceedings of the'
## 3. add the abbreviation of the proceedings, including CVPR/ICCV/ECCV/ICRA/IROS, waiting for supplementation；
## 4. delete the publication year in booktitle
## 5. check if pages exist
## 6. in case of article, check if volume and number exist
## 7. filter out the duplicate ref
## Have a nice day! Please create a new issue if needed.
## 2021/4/5, Guangze Zheng

filename = 'test.bib'  #file path

## proceedings
CVPR = 'computer vision and pattern recognition'
ICCV = 'international conference on computer vision'
ECCV = 'european conference on computer vision'
ICRA = 'international conference on robotics and automation'
IROS = 'intelligent robots and systems'

## judge the type of conference
def ifconfin(dictionary, string):
    for k in dictionary:
        if k in string:
            return dictionary[k]

## modify the description of booktitle in proceedings
def CVPR_modi(booktitle):
    booktitle = 'Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)'
    return booktitle

def ICCV_modi(booktitle):
    booktitle = 'Proceedings of the IEEE International Conference on Computer Vision (ICCV)'
    return booktitle

def ECCV_modi(booktitle):
    booktitle = 'Proceedings of the European Conference on Computer Vision (ECCV)'
    return booktitle

def ICRA_modi(booktitle):
    booktitle = 'Proceedings of the IEEE International Conference on Robotics and Automation (ICRA)'
    return booktitle

def IROS_modi(booktitle):
    booktitle = 'Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)'
    return booktitle

## check if pages exist
def checkpages(string):
    result = 'pages={' in string and 'pages={}' not in string
    return result

## check if volume exist
def checkvol(string):
    result = 'volume={' in string and 'volume={}' not in string
    return result

## check if num exist
def checknum(string):
    result = 'number={' in string and 'number={}' not in string
    return result

Conf_Dict = {CVPR : CVPR_modi,  
             ICCV : ICCV_modi,
             ECCV : ECCV_modi,
             ICRA : ICRA_modi,
             IROS : IROS_modi}

## remember the current ref info and all the titles
data = ''
ref_titles = [] 

## create a new .bib
new_filename = filename[:-4] + '_cor.bib'
nf = open(new_filename,'w') 

with open(filename, "r") as f:  
    lines = f.readlines()
    lines.append('@')
    for i in lines:
        if i == lines[0]:
            data += i
        elif i[0] == '@':
            data = data.expandtabs(tabsize=1)
            papertype = data[1:4].lower()
            index_title = data.index(' title={')
            index_t_b = index_title + len(' title={')
            index_t_e = data.index('}', index_t_b)

            ## add double brace
            if data[index_t_b + 1] != '{':
                data = '{'.join([data[:index_t_b], data[index_t_b: ]])
                data = '}'.join([data[:index_t_e+1], data[index_t_e+1: ]])
            
            ## title case
            title = data[index_t_b+1 : index_t_e]
            Title = title.title()
            if Title not in ref_titles:
                ref_titles.append(Title)
                data = data.replace(title, Title, 1)

                ## check if pages exist
                if not checkpages(data):
                    #raise Exception("No pages, please check or add the pages manually!")
                    print(f"No pages for {Title[1:-1]}")
                    
                ## booktitle of proceedings
                if papertype == 'inp':
                    index_booktitle = data.index('booktitle={')
                    index_b_b = index_booktitle + len('booktitle={')
                    index_b_e = data.index('}',index_booktitle)
                    booktitle = data[index_b_b : index_b_e]
                    booktitle_lower = booktitle.lower() 
                    modi = ifconfin(Conf_Dict, booktitle_lower)
                    real_booktitle = modi(booktitle)
                    data = data.replace(booktitle, real_booktitle, 1)

                ##  check if volume&number exists
                elif papertype == 'art':
                    if not checkvol(data):
                        #raise Exception("No volume, please check!")
                        print(f"No volume for {Title[1:-1]}")
                    if not checknum(data):
                        #raise Exception("No number, please check!")
                        print(f"No number for {Title[1:-1]}")
                
                nf.write(data) 
                data = ''
                data += i
        else:
            data += i 

nf.close() 

    