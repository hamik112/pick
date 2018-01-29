from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import os
import io
import xlsxwriter
# from xlsxwriter.utility import xl_rowcol_to_cell
import traceback
import logging
import datetime
from itertools import groupby
import operator
import json
import urllib.request
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

logger = logging.getLogger(__name__)

class ExcelReport():
    def write_workbook(self, file_path, file_name, target_insights):
        try:
            print("FILE : %s"%(os.path.join(file_path, file_name)))
            print("WRITE WORKBOOK")
            workbook = xlsxwriter.Workbook(os.path.join(file_path, file_name))
            format_dict = self.workbook_format(workbook)

            workbook = self.write_worksheet(workbook, target_insights)
            workbook.close()

            print("WRITE WORKBOOK SUCCESS")
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("Workbook Fail")

    def write_worksheet(self, workbook, target_insights):
        try:
            print("WRITE WORKSHEET - %")
            # format_dict = self.workbook_format(workbook)
            integer = workbook.add_format({'num_format': '0'})
            decimal = workbook.add_format({'num_format': '0.00'})
            percentage = workbook.add_format({'num_format': '0.00%'})
            currency = workbook.add_format({'num_format': '₩#,##0'})
            number = workbook.add_format({'num_format': '#,##0'})

            actions_name_list = self.find_insight_actions_name_list(target_insights)
            actions_name_list.remove('pickdata_custom_pixel_event')
            head_list = self.facebook_insight_to_headlist(target_insights, actions_name_list)

            worksheet = workbook.add_worksheet('Report')

            worksheet.write_row('A1', head_list)

            for idx, item in enumerate(target_insights):
                row_name = 'A' + str(idx + 2)
                worksheet.write_row(row_name, self.facebook_insight_to_list(item, actions_name_list))
            for idx, item in enumerate(target_insights):
                row_name = 'T' + str(idx + 2)
                worksheet.write_row(row_name, self.facebook_pickdata_event_to_list(item))
            for idx, item in enumerate(target_insights):
                row_name = 'U' + str(idx + 2)
                worksheet.write_row(row_name, self.facebook_fb_event_to_list(item, actions_name_list))

            worksheet.set_column('I', None, currency)
            worksheet.set_column('J:K', None, number)
            worksheet.set_column('M:N', None, number)
            worksheet.set_column('Q:T', None, number)

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("worksheet Fail")

        return workbook

    def workbook_format(self, workbook):
        # Make format
        title_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})

        merge_format1 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#d3d3d3'})

        merge_format2 = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#4169e1'})

        report_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})

        integer = workbook.add_format({'num_format': '0'})
        decimal = workbook.add_format({'num_format': '0.00'})
        percentage = workbook.add_format({'num_format': '0.00%'})
        currency = workbook.add_format({'num_format': '₩#,##0'})
        number = workbook.add_format({'num_format': '#,##0'})

        format_dict = {}
        format_dict['title_format'] = title_format
        format_dict['merge_format1'] = merge_format1
        format_dict['merge_format2'] = merge_format2
        format_dict['report_format'] = report_format
        format_dict['integer'] = integer
        format_dict['decimal'] = decimal
        format_dict['percentage'] = percentage
        format_dict['currency'] = currency
        format_dict['number'] = number

        return format_dict

    def facebook_insight_to_headlist(self, target_insights, actions_name_list):
        print('headlist')
        head_list = []
        try:
            head_list.append("account_category")
            head_list.append("account_name")
            head_list.append("campaign_name")
            head_list.append("report_date")
            head_list.append("age")
            head_list.append("gender")
            head_list.append("interest_list")
            head_list.append("custom_audience")
            head_list.append("spend")
            head_list.append("impressions")
            head_list.append("reach")
            head_list.append("frequency")
            head_list.append("clicks")
            head_list.append("inline_link_clicks")
            head_list.append("CTR")
            head_list.append("CPC")
            head_list.append("video_10_sec_view")
            head_list.append("video_30_sec_view")
            head_list.append("conversions")
            head_list.append("pickdata_custom_pixel_event")
            # TODO 전환지표
            head_list = head_list + actions_name_list
            print(head_list)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("insight to headlist Fail")
        return head_list

    def facebook_pickdata_event_to_list(self, insight):
        insight_list = []
        try:
            print(insight["pickdata_custom_pixel_event"])
            if insight["pickdata_custom_pixel_event"] != []:
                insight_list.append(insight["pickdata_custom_pixel_event"])
            else:
                insight_list.append('0')

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("insight to list Fail")
        return insight_list

    def facebook_fb_event_to_list(self, insight, actions_name_list):
        print(actions_name_list)
        insight_list = []
        try:
            for actions_name in actions_name_list:
                # insight_list.append('0')
                if actions_name in insight:
                    insight_list.append(insight[actions_name])
                else:
                    insight_list.append('0')
            else:
                insight_list.append('0')

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("insight to list Fail")
        return insight_list

    def facebook_insight_to_list(self, insight, actions_name_list):
        print(insight)
        insight_list = []
        try:
            insight_list.append(insight["account_category"])
            insight_list.append(insight["account_name"])
            insight_list.append(insight["campaign_name"])
            insight_list.append(insight["report_date"])
            insight_list.append(insight["age"])
            insight_list.append(insight["gender"])
            if insight["interest_list"] != []:
                list_item = ', '.join(insight["interest_list"])
                insight_list.append(list_item)
            else:
                insight_list.append('0')
            if insight["custom_audience"] != []:
                list_item = ', '.join(insight["custom_audience"])
                insight_list.append(list_item)
            else:
                insight_list.append('0')
            insight_list.append(insight["spend"])
            insight_list.append(insight["impressions"])
            insight_list.append(insight["reach"])
            insight_list.append(insight["frequency"])
            insight_list.append(insight["clicks"])
            insight_list.append(insight["inline_link_clicks"])
            insight_list.append(insight["ctr"])
            insight_list.append(insight["cpc"])
            if 'video_10_sec_view' in insight:
                insight_list.append(insight["video_10_sec_view"])
            else:
                insight_list.append('0')
            if 'video_30_sec_view' in insight:
                insight_list.append(insight["video_30_sec_view"])
            else:
                insight_list.append('0')

            insight_list.append(insight["conversions"])

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("insight to list Fail")
        return insight_list

    def find_insight_actions_name_list(self, insights):
        print('find_insight_actions')
        name_list = []
        try:
            for insight in insights:
                for elem in insight.keys():
                    if "_event" in elem:
                        name_list.append(elem)
                        name_list = list(set(name_list))
            name_list = sorted(name_list)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("insight actions name list Fail")
        return name_list
