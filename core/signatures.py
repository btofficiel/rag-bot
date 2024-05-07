import dspy

# GenerateCategory builds a signature for categorising queries into two broad categories
class GenerateCategory(dspy.Signature):
    """Classify the whether the query is an AGGREGATE_QUERY or GENERIC_QUERY. An example of aggregate query would be 'Tell me the total number of complains sent via emails' or similar queries asking about the count or total of data. Anything else is a GENERIC_QUERY"""

    query = dspy.InputField(desc="contains a query about the our dataset of complains")
    category = dspy.OutputField(desc="either one of these AGGREGATE_QUERY or GENERIC_QUERY. No other text apart from these two should be sent")


# GenerateAnswer builds a signature for answering generic queries
class GenerateAnswer(dspy.Signature):
    """Answer questions about support messages received and explicityly say 'Sorry, that is beyond my scope' to questions outside provide context """

    context = dspy.InputField(desc="contains comments, the date it occured on and the messaging channel via which the support message was received")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="an answer about either what people are complaining about or on which date or via which messaging channel.")


# FigureAggregateValues builds a signature for answering queries about aggregate data
class FigureAggregateValues(dspy.Signature):
    """Answer the queries about aggregate data such as total number or percentages of complaints. An example query could be 'What % of complains were done using email?'. If question is out of the context provided, then explicitly say 'Sorry, I wasn't able to figure that out' or something similar"""

    context = dspy.InputField(desc="contains total values or counts of data. For example 'Total number of complains using email were: 120' or something similar")
    question = dspy.InputField(desc="contains a query regarding complains data")
    answer = dspy.OutputField(desc="answer should be a number or a percentage. For example '75%' or '120 emails' or similar. No text apart from the format that is mentioned should be sent. In case of question being outside contex, explicitly say 'Sorry, I can't figure that out right now' or something similar")
