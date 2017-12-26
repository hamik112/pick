from django.db import models


class FbAdAccount(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    ad_account_id = models.BigIntegerField()
    act_account_id = models.CharField(max_length=64)
    name = models.CharField(max_length=128)
    account_status = models.IntegerField(default=2)
    account_category = models.ForeignKey('account_category.AccountCategory', models.CASCADE, db_constraint=False, null=False)

    class Meta:
        db_table = "fb_ad_accounts"
