from llm.factory import get_llm_strategy

from agents.prd_agent import PRDAgent
from agents.hld_agent import HLDAgent
from agents.lld_agent import LLDAgent
from agents.schema_agent import SchemaAgent
from agents.alignment_agent import AlignmentAgent

from engine.architecture_engine import ArchitectureEngine


def main():
    llm = get_llm_strategy()

    engine = ArchitectureEngine(
        PRDAgent(llm),
        HLDAgent(llm),
        LLDAgent(llm),
        SchemaAgent(llm),
        AlignmentAgent(llm)
    )

    client_input = input("Enter your product idea:\n")
    final_schema = engine.run(client_input)

    print("\n🎯 Final Schema:\n")
    print(final_schema)


if __name__ == "__main__":
    main()