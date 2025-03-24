


shen = ''
shi = ''
area = ''

result_dict = []

with open('area_codes.txt','r' , encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip()
        if line.count('|')==1:
            shen = line.split('|')[1]
        if line.count('|')==2:
            shi = line.split('||')[1]
        if shen in ['北京市','天津市','上海市','重庆市']:
            shi = ''
        if ',' in line:
            area_code ,area_address = line.split(',')
            result_dict.append({
                'area_code': area_code,
                'area_address':shen+shi+area_address,

            })


with open('area_codes_info.txt',encoding='utf-8',mode='w') as f:
    for i in result_dict:
        f.write(i['area_code']+','+i['area_address']+'\n')

print(result_dict)


if __name__ == '__main__':
    print('130100||石家庄市'.count('|'))


