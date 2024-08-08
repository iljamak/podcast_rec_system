import html
import re
import sys

'''
not important, debugging
'''
def delete_symbol_csv(podcast_path,columns:int=2,encoding_='utf-8'):
    with open(podcast_path,'r',encoding=encoding_) as f:
        lines = f.readlines()
    
    with open(podcast_path,'w',encoding=encoding_) as f:
        i = 0
        for line in lines:
            if len(line.split(';')) == columns:
                f.write(line)
            else:
                print("Line {} has more that one ';'".format(i))
                text = re.match(r'(.*;)(https://podtail.com.*)',line)
                if text:
                    part1 = text.group(1)
                    part1 = str(part1).replace(';',' ')
                    part2 = text.group(2)
                    new_line = part1 + ';' + part2
                    f.write(new_line)
            i+=1
        print("Deleteing unwanted delimeters is done.")
def check_csv(podcast_path,columns,delimeter=';',encoding_='utf-8'):
    flag = 1
    with open(podcast_path,'r',encoding=encoding_) as f:
        lines = f.readlines()
    with open(podcast_path,'w',encoding=encoding_) as f:
        for index,line in enumerate(lines):
            if len(line.split(';')) == columns:
                f.write(line)
                


def unescape_html(podcast_path,enconding_='utf-8'):
    with open(podcast_path,'r',encoding=enconding_) as f:
        lines = f.readlines()
    with open(podcast_path,'w',encoding=enconding_) as f:
        for line in lines:
            line = html.unescape(line)
            f.write(line)
        print("Unescaping done")


if __name__ == "__main__":
    p='podcasts_en.csv'
    #unescape_html(podcast_path=p)
    #delete_symbol_csv(p)
    check_csv(p,9)