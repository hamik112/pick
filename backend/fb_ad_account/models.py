from django.db import models


class FbAdAccount(models.Model):
    CATEGORY_DEFAULT = 0
    CATEGORY_LOAN = 1
    CATEGORT_NGO = 2
    CATEGORY_CARD = 3
    CATEGORY_TRAVLE = 4
    CATEGORY_SHOPPINGMALL = 5
    CATEGORY_ETC = 6
    CATEGORY_INSURANCE = 7
    CATEGORY_BEAUTY = 8

    ACCOUNT_CATEGORY_CHOICE = (
        (CATEGORY_DEFAULT, 'Default Cateogry'),
        (CATEGORY_LOAN, 'Loan'),
        (CATEGORT_NGO, 'NGO'),
        (CATEGORY_CARD, 'Card'),
        (CATEGORY_TRAVLE, 'Travel'),
        (CATEGORY_SHOPPINGMALL, 'Shopping Mall'),
        (CATEGORY_ETC, 'ETC'),
        (CATEGORY_INSURANCE, 'Insurance'),
        (CATEGORY_BEAUTY, 'Beauty')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    ad_account_id = models.BigIntegerField()
    act_account_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    account_status = models.IntegerField(default=2)
    account_category = models.IntegerField(default=CATEGORY_DEFAULT, choices=ACCOUNT_CATEGORY_CHOICE)

    @property
    def account_category_label(self):
        return self.get_account_category_display()

    class Meta:

        db_table = "fb_ad_accounts"
