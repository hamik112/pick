from django.db import models

class PixelMappingCategory(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)
    category_label_kr = models.CharField(max_length=128)
    category_label_en = models.CharField(max_length=128)

    def get_default_pixel_mapping_categories(self):
        try:
            exclude_list = ['visit pages', 'visit specific pages', 'neo target', 'utm target', 'conversion url']
            pixel_mapping_categories = PixelMappingCategory.objects.exclude(category_label_en__in=exclude_list)
            return pixel_mapping_categories
        except Exception as e:
            return None

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

    def get_pixel_mapping_category_for_mapping_view(self):
        try:
            category_en_list = ['purchase', 'add to cart', 'registration', 'conversion complete', 'conversion 1step', 'conversion 2step', 'conversion 3step', 'conversion 4step', 'conversion 5step']

            pixel_mapping_category = PixelMappingCategory.objects.filter(category_label_en__in=category_en_list)

            return pixel_mapping_category
        except PixelMappingCategory.DoesNotExist:
            return None

    class Meta:
        db_table = "pixel_mapping_category"