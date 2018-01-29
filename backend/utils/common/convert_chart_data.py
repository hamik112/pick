import traceback
import logging
import time
from utils.common.insight_convertor import insight_actions_to_conversion

logger = logging.getLogger(__name__)


def convert_agegender_chart_data(insights):
    return_data = {}
    total_spend = 0
    total_conversions = 0
    cta = 0

    age_ranges = ["13-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

    male_vals = {}
    female_vals = {}
    for age_range in  age_ranges:
        male_vals[age_range] = 0
        female_vals[age_range] = 0

    for insight in insights:
        age = insight.get('age')
        gender = insight.get('gender')
        spend = insight.get('spend')
        actions = insight.get('actions')
        conversions = insight_actions_to_conversion(actions)

        if gender == "male":
            male_vals[age] = male_vals[age] + int(insight.get('impressions'))
            total_spend += int(spend)
            total_conversions += int(conversions)
        elif gender == "female":
            female_vals[age] = female_vals[age] + int(insight.get('impressions'))
            total_spend += int(spend)
            total_conversions += int(conversions)

    # print(male_vals)
    # print(female_vals)

    male_sum = sum([male_vals[male_val] for male_val in male_vals])
    female_sum = sum([female_vals[female_val] for female_val in female_vals])
    total_sum = male_sum + female_sum

    # print(male_sum)
    # print(female_sum)
    # print(total_sum)

    # male_data = {}
    # female_data = {}

    if total_sum == 0:
        return_data = {
            "legend": ["male", "female"],
            "xAxis": age_ranges,
            "data" :
                {
                    "male":{
                        "weight": 0,
                        "sum": male_sum,
                        "percents":[male_vals[age_range] for age_range in age_ranges],
                        "vals":[male_vals[age_range] for age_range in age_ranges]
                    },
                    "female":{
                        "weight": 0,
                        "sum": female_sum,
                        "percents": [female_vals[age_range] for age_range in age_ranges],
                        "vals":[female_vals[age_range] for age_range in age_ranges]
                    }
                }

        }
    else:
        return_data = {
            "legend": ["male", "female"],
            "xAxis": age_ranges,
            "data": {
                "male":{
                    "weight": male_sum / total_sum * 100,
                    "sum": male_sum,
                    "percents":[male_vals[age_range] / total_sum * 100 for age_range in age_ranges],
                    "vals":[male_vals[age_range] for age_range in age_ranges]
                },
                "female":{
                    "weight": female_sum / total_sum * 100,
                    "sum": female_sum,
                    "percents": [female_vals[age_range] / total_sum * 100 for age_range in age_ranges],
                    "vals":[female_vals[age_range] for age_range in age_ranges]
                }
            }
        }

    if total_conversions > 0:
        cta = total_spend / total_conversions

    return return_data, total_spend, total_conversions, cta



def convert_placement_chart_data(insights):
    try:
        return_data = {}

        legend = ['PC', 'Mobile']

        total_sum = 0
        insights = [insight._json for insight in insights]

        publisher_platforms = [insight.get('publisher_platform') for insight in insights]
        impression_devices = [insight.get('impression_device') for insight in insights]

        publisher_platforms = list(set(publisher_platforms))
        impression_devices = list(set(impression_devices))

        pc_vals = {}
        mobile_vals = {}

        for publisher_platform in publisher_platforms:
            pc_vals[publisher_platform] = 0
            mobile_vals[publisher_platform] = 0

        for insight in insights:
            impression_device = insight.get('impression_device')
            publisher_platform = insight.get('publisher_platform')

            if impression_device == "desktop":
                pc_vals[publisher_platform] = pc_vals[publisher_platform] + int(insight.get('impressions'))
            else:
                mobile_vals[publisher_platform] = mobile_vals[publisher_platform] + int(insight.get('impressions'))

        print("pc_vals : ", pc_vals)
        print("mobile_vals : ", mobile_vals)

        pc_sum = sum([pc_vals[pc_val] for pc_val in pc_vals])
        mobile_sum = sum([mobile_vals[mobile_val] for mobile_val in mobile_vals])
        total_sum = pc_sum + mobile_sum

        if total_sum == 0:
            return_data = {
                "legend": legend,
                "xAxis": publisher_platforms,
                "data":
                    {
                        "PC": {
                            "weight": 0,
                            "sum": pc_sum,
                            "percents": [pc_vals[publisher_platform] for publisher_platform in publisher_platforms],
                            "vals": [pc_vals[publisher_platform] for publisher_platform in publisher_platforms]
                        },
                        "Mobile": {
                            "weight": 0,
                            "sum": mobile_sum,
                            "percents": [mobile_vals[publisher_platform] for publisher_platform in publisher_platforms],
                            "vals": [mobile_vals[publisher_platform] for publisher_platform in publisher_platforms]
                        }
                    }

            }
        else:
            return_data = {
                "legend": legend,
                "xAxis": publisher_platforms,
                "data": {
                    "PC": {
                        "weight": pc_sum / total_sum * 100,
                        "sum": pc_sum,
                        "percents": [pc_vals[publisher_platform] / total_sum * 100 for publisher_platform in publisher_platforms],
                        "vals": [pc_vals[publisher_platform] for publisher_platform in publisher_platforms]
                    },
                    "Mobile": {
                        "weight": mobile_sum / total_sum * 100,
                        "sum": mobile_sum,
                        "percents": [mobile_vals[publisher_platform] / total_sum * 100 for publisher_platform in publisher_platforms],
                        "vals": [mobile_vals[publisher_platform] for publisher_platform in publisher_platforms]
                    }
                }
            }

        return return_data

    except Exception:
        print(traceback.format_exc())
        logger.error(traceback.format_exc())
        return None