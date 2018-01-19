from django.db import models


class AccountPixelMapping(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)

    fb_ad_account = models.ForeignKey('fb_ad_account.FbAdAccount', db_constraint=False, null=False)
    event_mapping_name = models.CharField(max_length=128)
    pixel_event_name = models.CharField(max_length=128)

    class Meta:
        db_table = "account_piexel_mappings"
