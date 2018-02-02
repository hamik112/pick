from django.db import models

import datetime
import traceback
import logging

logger = logging.getLogger(__name__)

# Create your models here.

class AdSetInsight(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=64)
    updated_by = models.CharField(max_length=64)

    age = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    account_id = models.CharField(max_length=64)
    campaign_id = models.CharField(max_length=64)
    adset_id = models.CharField(max_length=64)
    ad_id = models.CharField(max_length=64)
    objective = models.CharField(max_length=32)
    date_start = models.DateTimeField()
    date_stop = models.DateTimeField()
    call_to_action_clicks = models.IntegerField(default=0)
    canvas_avg_view_percent = models.FloatField(default=0)
    canvas_avg_view_time = models.FloatField(default=0)
    actions = models.TextField(null=True)
    carousel_actions = models.TextField(null=True)
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    inline_link_clicks = models.IntegerField(default=0)
    spend = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    unique_actions = models.TextField(null=True)
    unique_clicks = models.IntegerField(default=0)
    unique_inline_link_clicks = models.IntegerField(default=0)
    cost_per_10_sec_video_view = models.TextField(null=True)
    cost_per_action_type = models.TextField(null=True)
    cost_per_estimated_ad_recallers = models.FloatField(default=0)
    cost_per_inline_link_click = models.FloatField(default=0)
    cost_per_inline_post_engagement = models.FloatField(default=0)
    cost_per_outbound_click = models.TextField(null=True)
    cost_per_total_action = models.FloatField(default=0)
    cost_per_unique_action_type = models.TextField(null=True)
    cost_per_unique_click = models.FloatField(default=0)
    cost_per_unique_inline_link_click = models.FloatField(default=0)
    cost_per_unique_outbound_click = models.TextField(null=True)
    cpc = models.FloatField(default=0)
    cpm = models.FloatField(default=0)
    cpp = models.FloatField(default=0)
    ctr = models.FloatField(default=0)
    estimated_ad_recall_rate = models.FloatField(default=0)
    frequency = models.FloatField(default=0)
    inline_link_click_ctr = models.FloatField(default=0)
    inline_link_clicks = models.IntegerField(default=0)
    inline_post_engagement = models.IntegerField(default=0)
    outbound_clicks = models.TextField(null=True)
    outbound_clicks_ctr = models.TextField(null=True)
    social_clicks = models.IntegerField(default=0)
    social_impressions = models.IntegerField(default=0)
    social_reach = models.IntegerField(default=0)
    social_spend = models.IntegerField(default=0)
    total_action_value = models.IntegerField(default=0)
    total_actions = models.IntegerField(default=0)
    total_unique_actions = models.IntegerField(default=0)
    unique_actions = models.TextField(null=True)
    unique_clicks = models.IntegerField(default=0)
    unique_ctr = models.FloatField(default=0)
    unique_inline_link_click_ctr = models.FloatField(default=0)
    unique_inline_link_clicks = models.IntegerField(default=0)
    unique_link_clicks_ctr = models.FloatField(default=0)
    unique_outbound_clicks = models.TextField(null=True)
    unique_outbound_clicks_ctr = models.TextField(null=True)
    unique_social_clicks = models.IntegerField(default=0)
    video_10_sec_watched_actions = models.TextField(null=True)
    video_30_sec_watched_actions = models.TextField(null=True)
    video_avg_percent_watched_actions = models.TextField(null=True)
    video_avg_time_watched_actions = models.TextField(null=True)
    video_p100_watched_actions = models.TextField(null=True)
    video_p25_watched_actions = models.TextField(null=True)
    video_p50_watched_actions = models.TextField(null=True)
    video_p75_watched_actions = models.TextField(null=True)
    video_p95_watched_actions = models.TextField(null=True)
    website_ctr = models.TextField(null=True)

    class Meta:
        db_table = "ad_set_insights"
        unique_together = ("adset_id", "date_start", "date_stop")