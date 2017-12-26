from django.db import models

class NeoAccount(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', models.CASCADE, db_constraint=False, null=False)
    neo_adv_id = models.IntegerField()
    neo_accouint_id = models.IntegerField()

    class Meta:
        db_table = "neo_accounts"