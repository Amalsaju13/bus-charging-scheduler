class BaseRule:
    def evaluate(self, context):
        return 0


class WaitTimeRule(BaseRule):
    def evaluate(self, context):
        return context["wait_time"]


class OperatorBalanceRule(BaseRule):
    def evaluate(self, context):
        operator_usage = context.get("operator_usage", 0)
        return operator_usage * 2


class NetworkEfficiencyRule(BaseRule):
    def evaluate(self, context):
        queue_size = context.get("queue_size", 0)
        return queue_size

def validate_range(distance, battery_range):
    return distance <= battery_range



def validate_station_order(path_indices):
    return path_indices == sorted(path_indices)



def validate_no_overlap(events):
    events = sorted(events, key=lambda x: x["start"])

    for i in range(len(events) - 1):
        if events[i]["end"] > events[i + 1]["start"]:
            return False

    return True