
class KnowledgeBase:
    """Knowledge Base of Facts (percepts) and Rules (Horn clauses)."""

    def __init__(self):
        self.facts = set()   # unique string facts
        self.rules = []      # tuples: (premise_list, conclusion_string)

    def tell_fact(self, fact_string):
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        self.rules.append((list(premise_list), conclusion_string))

    def clear_facts(self):
        self.facts.clear()

    def forward_chain(self):
        """Data-driven forward chaining: repeat Modus Ponens until a fixed point."""
        new_facts_added = True
        while new_facts_added:
            new_facts_added = False
            for premises, conclusion in self.rules:
                if conclusion not in self.facts:
                    if all(p in self.facts for p in premises):
                        self.facts.add(conclusion)
                        new_facts_added = True