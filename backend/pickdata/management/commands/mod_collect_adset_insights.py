from ad_set.models import AdSet
from ad_set_insight.models import AdSetInsight
from utils.facebookapis import api_init
from utils.facebookapis.ad_account import ad_accounts
from utils.facebookapis.ad_account import ad_sets as ad_sets_api
from facebookads.exceptions import FacebookRequestError

import logging
import traceback
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

logger = logging.getLogger('mod_pickdata')

'''
ex) python manage.py mod_collect_adset_insights --settings=pickdata.settings.dev
'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        self.stdout.write("--- collect collect adset module start ---")

    def handle(self, *args, **options):
        self.stdout.write("--- collect collect adset module handle ---")
        try:
            api_init.api_init_by_system_user()

            my_accounts = ad_accounts.get_my_ad_accounts()

            # SAMPLE
            # my_accounts = [
            #     {
            # 		"id": 'act_894360037304328',
            # 		'name': "KB국민카드(엠포스)"
            # 	}
            # ]

            for my_account in my_accounts:
                account_id = my_account.get('id')
                account_name = my_account.get('name')

                ad_sets = ad_accounts.get_my_ad_sets(account_id)

                for ad_set in ad_sets:
                    ad_set = ad_set._json
                    adset_id = ad_set.get('id')
                    insights = ad_sets_api.get_insight_by_ad_set(adset_id,
                        params={
                            "date_preset": "lifetime",
                            "time_increment": 1
                        })
                    if insights != None:
                        for insight in insights:
                            # Adset ad_insights
                            account_id = insight.get('account_id')
                            campaign_id = insight.get('campaign_id')
                            campaign_objective = insight.get('objective')
                            adset_id = insight.get('adset_id')
                            ad_id = insight.get('ad_id')
                            date_start = insight.get('date_start')
                            date_stop = insight.get('date_stop')
                            call_to_action_clicks = insight.get('call_to_action_clicks')
                            canvas_avg_view_percent = insight.get('canvas_avg_view_percent')
                            canvas_avg_view_time = insight.get('canvas_avg_view_time')
                            impressions = insight.get('impressions')
                            clicks = insight.get('clicks')
                            spend = insight.get('spend')
                            reach = insight.get('reach')
                            actions = insight.get('actions')
                            cost_per_10_sec_video_view = insight.get('cost_per_10_sec_video_view')
                            cost_per_action_type = insight.get('cost_per_action_type')
                            cost_per_estimated_ad_recallers = insight.get('cost_per_estimated_ad_recallers')
                            cost_per_inline_link_click = insight.get('cost_per_inline_link_click')
                            cost_per_inline_post_engagement = insight.get('cost_per_inline_post_engagement')
                            cost_per_outbound_click = insight.get('cost_per_outbound_click')
                            cost_per_total_action = insight.get('cost_per_total_action')
                            cost_per_unique_action_type = insight.get('cost_per_unique_action_type')
                            cost_per_unique_click = insight.get('cost_per_unique_click')
                            cost_per_unique_inline_link_click = insight.get('cost_per_unique_inline_link_click')
                            cost_per_unique_outbound_click = insight.get('cost_per_unique_outbound_click')
                            cpc = insight.get('cpc')
                            cpm = insight.get('cpm')
                            cpp = insight.get('cpp')
                            ctr = insight.get('ctr')
                            estimated_ad_recall_rate = insight.get('estimated_ad_recall_rate')
                            frequency = insight.get('frequency')
                            inline_link_click_ctr = insight.get('inline_link_click_ctr')
                            inline_link_clicks = insight.get('inline_link_clicks')
                            inline_post_engagement = insight.get('inline_post_engagement')
                            outbound_clicks = insight.get('outbound_clicks')
                            outbound_clicks_ctr = insight.get('outbound_clicks_ctr')
                            social_clicks = insight.get('social_clicks')
                            social_impressions = insight.get('social_impressions')
                            social_reach = insight.get('social_reach')
                            social_spend = insight.get('social_spend')
                            total_action_value = insight.get('total_action_value')
                            total_actions = insight.get('total_actions')
                            total_unique_actions = insight.get('total_unique_actions')
                            unique_actions = insight.get('unique_actions')
                            unique_clicks= insight.get('unique_clicks')
                            unique_ctr = insight.get('unique_ctr')
                            unique_inline_link_click_ctr = insight.get('unique_inline_link_click_ctr')
                            unique_inline_link_clicks = insight.get('unique_inline_link_clicks')
                            unique_link_clicks_ctr = insight.get('unique_link_clicks_ctr')
                            unique_outbound_clicks = insight.get('unique_outbound_clicks')
                            unique_outbound_clicks_ctr = insight.get('unique_outbound_clicks_ctr')
                            unique_social_clicks = insight.get('unique_social_clicks')
                            video_10_sec_watched_actions = insight.get('video_10_sec_watched_actions')
                            video_30_sec_watched_actions = insight.get('video_30_sec_watched_actions')
                            video_avg_percent_watched_actions = insight.get('video_avg_percent_watched_actions')
                            video_p100_watched_actions = insight.get('video_p100_watched_actions')
                            video_p25_watched_actions = insight.get('video_p25_watched_actions')
                            video_p50_watched_actions = insight.get('video_p50_watched_actions')
                            video_p75_watched_actions = insight.get('video_p75_watched_actions')
                            video_p95_watched_actions = insight.get('video_p95_watched_actions')
                            website_ctr = insight.get('website_ctr')

                            # ad_set_insight 데이터 insert
                            adset_insight = AdSetInsight()

                            adset_insight.created_by = "Module"
                            adset_insight.updated_by = "Module"

                            # age, gender 무시, insert 하지 않는다.
                            # adset_insight.age = age
                            # adset_insight.gender = gender
                            adset_insight.account_id = account_id
                            adset_insight.campaign_id = campaign_id
                            adset_insight.adset_id = adset_id
                            adset_insight.objective = campaign_objective
                            if ad_id == None:
                                adset_insight.ad_id = 0
                            else:
                                adset_insight.ad_id = ad_id
                            adset_insight.date_start = date_start
                            adset_insight.date_stop = date_stop
                            adset_insight.call_to_action_clicks = call_to_action_clicks
                            adset_insight.canvas_avg_view_percent = canvas_avg_view_percent
                            adset_insight.canvas_avg_view_time = canvas_avg_view_time
                            adset_insight.impressions = impressions
                            adset_insight.clicks = clicks
                            adset_insight.spend = spend
                            adset_insight.reach = reach
                            adset_insight.actions = actions
                            adset_insight.cost_per_10_sec_video_view = cost_per_10_sec_video_view
                            adset_insight.cost_per_action_type = cost_per_action_type
                            adset_insight.cost_per_estimated_ad_recallers = cost_per_estimated_ad_recallers
                            adset_insight.cost_per_inline_link_click = cost_per_inline_link_click
                            adset_insight.cost_per_inline_post_engagement = cost_per_inline_post_engagement
                            adset_insight.cost_per_outbound_click = cost_per_outbound_click
                            adset_insight.cost_per_total_action = cost_per_total_action
                            adset_insight.cost_per_unique_action_type = cost_per_unique_action_type
                            adset_insight.cost_per_unique_click = cost_per_unique_click
                            adset_insight.cost_per_unique_inline_link_click = cost_per_unique_inline_link_click
                            adset_insight.cost_per_unique_outbound_click = cost_per_unique_outbound_click
                            adset_insight.cpc = cpc
                            adset_insight.cpm = cpm
                            adset_insight.cpp = cpp
                            adset_insight.ctr = ctr
                            adset_insight.estimated_ad_recall_rate = estimated_ad_recall_rate
                            adset_insight.frequency = frequency
                            adset_insight.inline_link_click_ctr = inline_link_click_ctr
                            adset_insight.inline_link_clicks = inline_link_clicks
                            adset_insight.inline_post_engagement = inline_post_engagement
                            adset_insight.outbound_clicks = outbound_clicks
                            adset_insight.outbound_clicks_ctr = outbound_clicks_ctr
                            adset_insight.social_clicks = social_clicks
                            adset_insight.social_impressions = social_impressions
                            adset_insight.social_reach = social_reach
                            adset_insight.social_spend = social_spend
                            adset_insight.total_action_value = total_action_value
                            adset_insight.total_actions = total_actions
                            adset_insight.total_unique_actions = total_unique_actions
                            adset_insight.unique_actions = unique_actions
                            adset_insight.unique_clicks = unique_clicks
                            adset_insight.unique_ctr = unique_ctr
                            adset_insight.unique_inline_link_click_ctr = unique_inline_link_click_ctr
                            adset_insight.unique_inline_link_clicks = unique_inline_link_clicks
                            adset_insight.unique_link_clicks_ctr = unique_link_clicks_ctr
                            adset_insight.unique_outbound_clicks = unique_outbound_clicks
                            adset_insight.unique_outbound_clicks_ctr = unique_outbound_clicks_ctr
                            adset_insight.unique_social_clicks = unique_social_clicks
                            adset_insight.video_10_sec_watched_actions = video_10_sec_watched_actions
                            adset_insight.video_30_sec_watched_actions = video_30_sec_watched_actions
                            adset_insight.video_avg_percent_watched_actions = video_avg_percent_watched_actions
                            adset_insight.video_p100_watched_actions = video_p100_watched_actions
                            adset_insight.video_p25_watched_actions = video_p25_watched_actions
                            adset_insight.video_p50_watched_actions = video_p50_watched_actions
                            adset_insight.video_p75_watched_actions = video_p75_watched_actions
                            adset_insight.video_p95_watched_actions = video_p95_watched_actions
                            adset_insight.website_ctr = website_ctr

                            adset_insight.save()
                    else:
                        pass

            logger.info("collect adset insight module complete")
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("collect adset insight fail")
