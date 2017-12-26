from django.db import models

class PickdataAccountTarget(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)

    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', models.CASCADE, db_constraint=False, null=False)
    target_audience_id = models.BigIntegerField()

    pixel_mapping = models.ForeignKey('pixel_mapping.PixelMapping', models.CASCADE, db_constraint=False, null=False)
    rentention_days = models.IntegerField()
    target_status = models.IntegerField()
    extra_pixel_mapping_id = models.IntegerField(null=True)

    class Meta:
        db_table = "pickdata_account_targets"
