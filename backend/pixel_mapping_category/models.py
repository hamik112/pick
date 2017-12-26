from django.db import models

class PixelMappingCategory(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    category_label_kr = models.CharField(max_length=128)
    category_label_en = models.CharField(max_length=128)

    class Meta:
        db_table = "pixel_mapping_category"