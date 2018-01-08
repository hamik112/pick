from ad_set.models import AdSet
from rest_framework import serializers

class AdSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdSet
        fields = ('account_id', 'created_at', 'updated_at', 'created_by', 'updated_by', 'account_name', 'campaign_name',
        'campaign_id', 'campaign_objective', 'adset_id', 'adset_name', 'age_min', 'age_max', 'gender', 'include_interests',
        'exclude_interests', 'include_behaviors', 'exclude_behaviors', 'custom_audiences', 'excluded_custom_audiences',
        'daily_budget', 'lifetime_budget', 'targeting')
