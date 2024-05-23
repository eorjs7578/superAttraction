from django.db import models

class ExchangeRate(models.Model):
    result = models.IntegerField()  # 결과 코드
    cur_unit = models.CharField(max_length=10)  # 통화코드
    cur_nm = models.CharField(max_length=50)  # 국가/통화명
    ttb = models.CharField(max_length=20)  # 전신환(송금) 받으실 때
    tts = models.CharField(max_length=20)  # 전신환(송금) 보내실 때
    deal_bas_r = models.CharField(max_length=20)  # 매매 기준율
    bkpr = models.CharField(max_length=20)  # 장부가격
    yy_efee_r = models.CharField(max_length=20)  # 년환가료율
    ten_dd_efee_r = models.CharField(max_length=20)  # 10일환가료율
    kftc_deal_bas_r = models.CharField(max_length=20)  # 서울외국환중개 매매기준율
    fktc_bkpr = models.CharField(max_length=20)  # 서울외국환중개 장부가격

    def __str__(self):
        return f"{self.cur_nm} ({self.cur_unit})"



class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField()
    join_deny = models.IntegerField()
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField()
    intr_rate2 = models.FloatField()
    save_trm = models.IntegerField()