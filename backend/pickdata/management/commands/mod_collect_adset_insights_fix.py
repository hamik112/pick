import logging
import time
import traceback

from django.core.management.base import BaseCommand

from ad_set_insight.models import AdSetInsight
from utils.facebookapis import api_init
from utils.facebookapis.ad_account import ad_accounts
from utils.facebookapis.ad_account import insight

logger = logging.getLogger('mod_pickdata')

'''
ex) python manage.py mod_collect_adset_insights_fix --settings=pickdata.settings.production
ex) python manage.py mod_collect_adset_insights_fix --date_from=2018-02-01 --date_to=2018-02-05 --settings=pickdata.settings.production
'''


class Command(BaseCommand):
    def add_arguments(self, parser):
        self.stdout.write("--- collect collect adset insight module start ---")
        # parser.add_argument('date_from', nargs='+', default='None', type=str)
        # parser.add_argument('date_to', nargs='+', default='None', type=str)
        parser.add_argument('--date_from', nargs='+', default=None, type=str)
        parser.add_argument('--date_to', nargs='+', default=None, type=str)

    def handle(self, *args, **options):
        self.stdout.write("--- collect collect adset insight module handle ---")
        try:
            date_from = None
            date_to = None

            if options['date_from']:
                date_from = options['date_from'][0]
            if options['date_to']:
                date_to = options['date_to'][0]

            import datetime
            from utils.common import date_formatter

            if date_from == None or date_to == None:
                now = datetime.datetime.now()
                yesterday = now - datetime.timedelta(days=1)
                before_sevevday = now - datetime.timedelta(days=7)

                start_dt = before_sevevday.date()
                end_dt = yesterday.date()
            else:
                start_datetime = date_formatter.str_to_datetime(date_from)
                to_datetime = date_formatter.str_to_datetime(date_to)

                start_dt = start_datetime.date()
                end_dt = to_datetime.date()

            api_init.api_init_by_system_user()

            my_accounts = ad_accounts.get_my_ad_accounts()

            for my_account in my_accounts:
                account_id = my_account.get('id')
                account_name = my_account.get('name')

                print("account_id : ", account_id)
                print("account_name : ", account_name)
                logger.info(account_id)
                logger.info(account_name)

                date_list = date_formatter.daterange(start_dt, end_dt)

                for select_date in date_list:
                    select_date = select_date.strftime("%Y-%m-%d")
                    print("select_date : ", select_date)
                    logger.info(select_date)
                    ad_set_insights = insight.get_adset_level_select_date_insights(account_id, select_date)

                    for adset_insight in ad_set_insights:
                        self.insert_or_update_DB(adset_insight)
                        time.sleep(1)

                    ad_set_carousel_insights = insight.get_adset_level_select_date_carousel_insights(account_id, select_date)

                    for adset_carousel_insight in ad_set_carousel_insights:
                        if adset_carousel_insight.get('actions', [{'value': '0', 'action_type': 'link_click'}]) != [{'value': '0', 'action_type': 'link_click'}]:
                            self.insert_or_update_carousel_DB(adset_carousel_insight)
                            time.sleep(1)

            # logger.info(len(adset_insight_list))
            # logger.info(no_insights)
            logger.info("collect adset insight module complete")
        except Exception as e:
            print(traceback.format_exc())
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("collect adset insight fail")

    def insert_or_update_DB(self, item):

        account_id = item.get('account_id')
        campaign_id = item.get('campaign_id')
        campaign_objective = item.get('objective')
        adset_id = item.get('adset_id')
        ad_id = item.get('ad_id')
        date_start = item.get('date_start')
        date_stop = item.get('date_stop')
        call_to_action_clicks = item.get('call_to_action_clicks')
        canvas_avg_view_percent = item.get('canvas_avg_view_percent')
        canvas_avg_view_time = item.get('canvas_avg_view_time')
        impressions = item.get('impressions')
        clicks = item.get('clicks')
        spend = item.get('spend')
        reach = item.get('reach')
        actions = item.get('actions')
        cost_per_10_sec_video_view = item.get('cost_per_10_sec_video_view')
        cost_per_action_type = item.get('cost_per_action_type')
        cost_per_estimated_ad_recallers = item.get('cost_per_estimated_ad_recallers')
        cost_per_inline_link_click = item.get('cost_per_inline_link_click')
        cost_per_inline_post_engagement = item.get('cost_per_inline_post_engagement')
        cost_per_outbound_click = item.get('cost_per_outbound_click')
        cost_per_total_action = item.get('cost_per_total_action')
        cost_per_unique_action_type = item.get('cost_per_unique_action_type')
        cost_per_unique_click = item.get('cost_per_unique_click')
        cost_per_unique_inline_link_click = item.get('cost_per_unique_inline_link_click')
        cost_per_unique_outbound_click = item.get('cost_per_unique_outbound_click')
        cpc = item.get('cpc')
        cpm = item.get('cpm')
        cpp = item.get('cpp')
        ctr = item.get('ctr')
        estimated_ad_recall_rate = item.get('estimated_ad_recall_rate')
        frequency = item.get('frequency')
        inline_link_click_ctr = item.get('inline_link_click_ctr')
        inline_link_clicks = item.get('inline_link_clicks')
        inline_post_engagement = item.get('inline_post_engagement')
        outbound_clicks = item.get('outbound_clicks')
        outbound_clicks_ctr = item.get('outbound_clicks_ctr')
        social_clicks = item.get('social_clicks')
        social_impressions = item.get('social_impressions')
        social_reach = item.get('social_reach')
        social_spend = item.get('social_spend')
        total_action_value = item.get('total_action_value')
        total_actions = item.get('total_actions')
        total_unique_actions = item.get('total_unique_actions')
        unique_actions = item.get('unique_actions')
        unique_clicks = item.get('unique_clicks')
        unique_ctr = item.get('unique_ctr')
        unique_inline_link_click_ctr = item.get('unique_inline_link_click_ctr')
        unique_inline_link_clicks = item.get('unique_inline_link_clicks')
        unique_link_clicks_ctr = item.get('unique_link_clicks_ctr')
        unique_outbound_clicks = item.get('unique_outbound_clicks')
        unique_outbound_clicks_ctr = item.get('unique_outbound_clicks_ctr')
        unique_social_clicks = item.get('unique_social_clicks')
        video_10_sec_watched_actions = item.get('video_10_sec_watched_actions')
        video_30_sec_watched_actions = item.get('video_30_sec_watched_actions')
        video_avg_percent_watched_actions = item.get('video_avg_percent_watched_actions')
        video_p100_watched_actions = item.get('video_p100_watched_actions')
        video_p25_watched_actions = item.get('video_p25_watched_actions')
        video_p50_watched_actions = item.get('video_p50_watched_actions')
        video_p75_watched_actions = item.get('video_p75_watched_actions')
        video_p95_watched_actions = item.get('video_p95_watched_actions')
        website_ctr = item.get('website_ctr')

        # ad_set_insight model
        adset_insight = AdSetInsight()

        params = {}
        params["created_by"] = "Module"
        params["updated_by"] = "Module"

        # age, gender 무시, insert 하지 않는다.
        # adset_insight.age = age
        # adset_insight.gender = gender

        params["account_id"] = account_id
        params["campaign_id"] = campaign_id
        # params["adset_id"] = adset_id
        params["objective"] = campaign_objective
        if ad_id == None:
            params["ad_id"] = 0
        else:
            params["ad_id"] = ad_id

        # adset_insight.date_start = date_start
        # adset_insight.date_stop = date_stop

        params["call_to_action_clicks"] = call_to_action_clicks
        params["canvas_avg_view_percent"] = canvas_avg_view_percent
        params["canvas_avg_view_time"] = canvas_avg_view_time
        params["impressions"] = impressions
        params["clicks"] = clicks
        params["spend"] = spend
        params["reach"] = reach
        params["actions"] = actions
        params["cost_per_10_sec_video_view"] = cost_per_10_sec_video_view
        params["cost_per_action_type"] = cost_per_action_type
        params["cost_per_estimated_ad_recallers"] = cost_per_estimated_ad_recallers
        params["cost_per_inline_link_click"] = cost_per_inline_link_click
        params["cost_per_inline_post_engagement"] = cost_per_inline_post_engagement
        params["cost_per_outbound_click"] = cost_per_outbound_click
        params["cost_per_total_action"] = cost_per_total_action
        params["cost_per_unique_action_type"] = cost_per_unique_action_type
        params["cost_per_unique_click"] = cost_per_unique_click
        params["cost_per_unique_inline_link_click"] = cost_per_unique_inline_link_click
        params["cost_per_unique_outbound_click"] = cost_per_unique_outbound_click
        params["cpc"] = cpc
        params["cpm"] = cpm
        params["cpp"] = cpp
        params["ctr"] = ctr
        params["estimated_ad_recall_rate"] = estimated_ad_recall_rate
        params["frequency"] = frequency
        params["inline_link_click_ctr"] = inline_link_click_ctr
        params["inline_link_clicks"] = inline_link_clicks
        params["inline_post_engagement"] = inline_post_engagement
        params["outbound_clicks"] = outbound_clicks
        params["outbound_clicks_ctr"] = outbound_clicks_ctr
        params["social_clicks"] = social_clicks
        params["social_impressions"] = social_impressions
        params["social_reach"] = social_reach
        params["social_spend"] = social_spend
        params["total_action_value"] = total_action_value
        params["total_actions"] = total_actions
        params["total_unique_actions"] = total_unique_actions
        params["unique_actions"] = unique_actions
        params["unique_clicks"] = unique_clicks
        params["unique_ctr"] = unique_ctr
        params["unique_inline_link_click_ctr"] = unique_inline_link_click_ctr
        params["unique_inline_link_clicks"] = unique_inline_link_clicks
        params["unique_link_clicks_ctr"] = unique_link_clicks_ctr
        params["unique_outbound_clicks"] = unique_outbound_clicks
        params["unique_outbound_clicks_ctr"] = unique_outbound_clicks_ctr
        params["unique_social_clicks"] = unique_social_clicks
        params["video_10_sec_watched_actions"] = video_10_sec_watched_actions
        params["video_avg_percent_watched_actions"] = video_avg_percent_watched_actions
        params["video_p100_watched_actions"] = video_p100_watched_actions
        params["video_p25_watched_actions"] = video_p25_watched_actions
        params["video_p50_watched_actions"] = video_p50_watched_actions
        params["video_p75_watched_actions"] = video_p75_watched_actions
        params["video_p95_watched_actions"] = video_p95_watched_actions
        params["website_ctr"] = website_ctr

        try:
            obj, created = AdSetInsight.objects.update_or_create(
                adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
            )
        except Exception:
            try:
                obj, created = AdSetInsight.objects.update_or_create(
                    adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                )
            except Exception:
                try:
                    obj, created = AdSetInsight.objects.update_or_create(
                        adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                    )
                except Exception:
                    try:
                        obj, created = AdSetInsight.objects.update_or_create(
                            adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                        )
                    except Exception:
                        try:
                            obj, created = AdSetInsight.objects.update_or_create(
                                adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                            )
                        except Exception:
                            print(traceback.format_exc())

        # adset_insight.save()
        logger.info('DB INSERT COMPLETE')


    def insert_or_update_carousel_DB(self, item):

        adset_id = item.get('adset_id')
        date_start = item.get('date_start')
        date_stop = item.get('date_stop')
        actions = item.get('actions')

        # ad_set_insight model
        adset_insight = AdSetInsight()

        params = {}
        params["created_by"] = "Module"
        params["updated_by"] = "Module"

        params['carousel_actions'] = actions

        try:
            obj, created = AdSetInsight.objects.update_or_create(
                adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
            )
        except Exception:
            try:
                obj, created = AdSetInsight.objects.update_or_create(
                    adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                )
            except Exception:
                try:
                    obj, created = AdSetInsight.objects.update_or_create(
                        adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                    )
                except Exception:
                    try:
                        obj, created = AdSetInsight.objects.update_or_create(
                            adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                        )
                    except Exception:
                        try:
                            obj, created = AdSetInsight.objects.update_or_create(
                                adset_id=adset_id, date_start=date_start, date_stop=date_stop, defaults=params
                            )
                        except Exception:
                            print(traceback.format_exc())
        # adset_insight.save()
        logger.info('DB CAROUSEL INSERT COMPLETE')