import dspy
from .signatures import GenerateAnswer, GenerateCategory, FigureAggregateValues

class RAG(dspy.Module):
    def __init__(self, num_passages=5):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)
        self.figure_aggregate = dspy.ChainOfThought(FigureAggregateValues)
        self.classify_query = dspy.ChainOfThought(GenerateCategory)

    def forward(self, question):
        # Classify query
        query_classification = self.classify_query(query=question)
        # Generate context from QdrantDB
        context = self.retrieve(question).passages
        if query_classification.category == "AGGREGATE_QUERY":
            prediction = self.figure_aggregate(context=context, question=question)
            return dspy.Prediction(context=context, answer=prediction.answer)
        else:
            prediction = self.generate_answer(context=context, question=question)
            return dspy.Prediction(context=context, answer=prediction.answer)
