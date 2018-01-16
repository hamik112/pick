from django.db import models

class PixelMappingCategory(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    category_label_kr = models.CharField(max_length=128)
    category_label_en = models.CharField(max_length=128)

    def get_pixel_mapping_categories(self):
        try:
            pixel_mapping_categories = PixelMappingCategory.objects.all()

            return pixel_mapping_categories
        except Exception as e:
            return None

    def get_pixel_mapping_category_by_label(self, label):
        try:
            pixel_mapping_category = PixelMappingCategory.objects.get(category_label_en=label)

            return pixel_mapping_category
        except PixelMappingCategory.DoesNotExist:
            try:
                pixel_mapping_category = PixelMappingCategory.objects.get(category_label_en=label)

                return pixel_mapping_category
            except PixelMappingCategory.DoesNotExist:
                return None

    def get_pixel_mapping_category_by_id(self, id):
        try:
            pixel_mapping_category = PixelMappingCategory.objects.get(pk=id)
            return pixel_mapping_category

        except PixelMappingCategory.DoesNotExist:
            return None

    class Meta:
        db_table = "pixel_mapping_category"