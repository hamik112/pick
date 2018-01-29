def insight_actions_to_conversion(actions):
    try:
        total_value = 0
        minus_value = 0

        for action in actions:
            if action.get('action_type') == "offsite_conversion":
                total_value = action.get('value')
            if action.get('action_type').find('offsite_conversion') > -1 and action.get('action_type').find('.custom.') > -1:
                minus_value += int(action.get('value'))

        value = int(total_value) - int(minus_value)

        return str(value)
    except Exception:
        return '0'
