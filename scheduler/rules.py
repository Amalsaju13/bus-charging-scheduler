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