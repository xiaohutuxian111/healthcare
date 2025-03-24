import datetime
import random
from collections import defaultdict
from functools import lru_cache

from faker import Faker
from faker.contrib.pytest.plugin import faker


class FakerUtil:
    def __init__(self):
        self.fake = Faker('zh_cn')

    def get_fake_name(self) -> str:
        return self.fake.name()

    def get_fake_phone(self) -> str:
        return self.fake.phone_number()

    def get_fake_email(self) -> str:
        return self.fake.email()

    def get_fake_address(self) -> str:
        return self.fake.address()

    def get_fake_date(self) -> str:
        return self.fake.date()

    def get_fake_date_time(self) -> datetime:
        return self.fake.date_time()

    def get_fake_text(self) -> str:
        return self.fake.text()

    def get_fake_word(self) -> str:
        return self.fake.word()

    def get_street_address(self):
        return self.fake.street_address()


class IDcardInfoUtils(FakerUtil):
    def __init__(self):
        super().__init__()
        self.area_dict = self.load_area_codes()

    @lru_cache()
    def load_area_codes(self):
        area_dict = defaultdict()
        with open('area_codes_info.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    area_code, area_address = parts
                    area_dict[area_code] = area_address
        return area_dict

    @staticmethod
    def get_nation():
        nations = ['汉族', '蒙古族', '回族', '藏族', '维吾尔族', '苗族', '彝族', '壮族', '布依族', '朝鲜族', '满族',
                   '侗族', '瑶族', '白族', '土家族', '哈尼族', '哈萨克族', '傣族', '黎族', '僳僳族', '佤族', '畲族',
                   '高山族', '拉祜族', '水族', '东乡族', '纳西族', '景颇族', '柯尔克孜族', '土族', '达斡尔族', '仫佬族',
                   '羌族', '布朗族', '撒拉族', '毛南族', '仡佬族', '锡伯族', '阿昌族', '普米族', '塔吉克族', '怒族',
                   '乌孜别克族',
                   '俄罗斯族', '鄂温克族', '德昂族', '保安族', '裕固族', '京族', '塔塔尔族', '独龙族', '鄂伦春族',
                   '赫哲族',
                   '门巴族', '珞巴族', '基诺族']
        return random.choice(nations)

    def idcard_info(self):
        name = self.get_fake_name()
        idcard_no = self.get_idcard_no()
        nation = self.get_nation()
        gender = '女' if int(idcard_no[-2]) % 2 == 0 else '男'
        birth_date = idcard_no[6:14]
        address = self.area_dict[idcard_no[:6]] + self.get_street_address()

        expiry_year = self.__get_expiry_year(birth_date)

        return {
            '姓名': name,
            '性别': gender,
            '民族': nation,
            '出生日期': birth_date,
            '住址': address,
            '公民省份号码': idcard_no,
            '有效期': expiry_year,
        }

    @classmethod
    def __get_expiry_year(cls, birth_date: str):
        # 计算当前人员的有效期
        birth_date = datetime.datetime.strptime(birth_date, '%Y%m%d')
        today = datetime.date.today()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        if age < 18:
            return 5
        elif 18 <= age <= 45:
            return 20
        else:
            return '长期'

    def get_area_code(self) -> str:
        return random.choice(list(self.area_dict.keys()))

    def get_idcard_no(self) -> str:
        # 生成前6位地址码（假设随机生成）
        # address_code = ''.join(random.choices('0123456789', k=6))
        address_code = self.get_area_code()
        # 生成8位出生日期
        start_date = datetime.date(1900, 1, 1)
        end_date = datetime.date.today()
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        birth_date = start_date + datetime.timedelta(days=random_days)
        birth_date_str = birth_date.strftime('%Y%m%d')

        # 生成顺序码
        order_code = ''.join(random.choices('0123456789', k=3))

        # 生成校验码
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        id_card_base = address_code + birth_date_str + order_code
        checksum = sum(int(id_card_base[i]) * weights[i] for i in range(17))
        check_code = check_codes[checksum % 11]

        return id_card_base + check_code



IDcardInfo = IDcardInfoUtils()



