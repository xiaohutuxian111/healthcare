import datetime
import random
from functools import lru_cache

from faker import Faker


class FakerUtil:
    def __init__(self):
        self.fake = Faker('zh_cn')
        self.area_info = self.load_area_codes()

    @lru_cache()
    def load_area_codes(self):
        area_info = []
        with open('area_codes_info.txt', 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    area_code, area_address = parts
                    area_info.append({'area_code':area_code,'area_address':area_address})
        return area_info

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

    def get_area_code(self) -> str:
        area = random.choice(self.area_info)
        print(area)
        return area['area_code']

    def get_area_address(self) -> str:
        area = random.choice(self.area_info)
        return area['area_address']

    def get_fake_idcard(self) -> str:
        # 生成前6位地址码（假设随机生成）
        # address_code = ''.join(random.choices('0123456789', k=6))
        address_code = self.get_area_code()
        print(address_code)

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


if __name__ == '__main__':
    f = FakerUtil()
    print(f.get_fake_idcard())
