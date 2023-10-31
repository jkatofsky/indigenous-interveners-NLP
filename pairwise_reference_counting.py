import sys
import glob
from pathlib import Path
# TODO: use this one?
# from difflib import SequenceMatcher
import Levenshtein


# TODO type return?
def load_references(directory: str):
    with open(f"{directory}/decision.references.txt") as fp:
        decision_references = [line.rstrip() for line in fp]
    factums_references = dict()
    for factum_references_filename in glob.glob(f"{directory}/interveners/*.references.txt"):
        with open(factum_references_filename) as fp:
            factums_references[Path(factum_references_filename).name.split('.')[0]] = [line.rstrip() for line in fp]
    return decision_references, factums_references


# TODO: also do not matching
def get_pairwise_references(references1: list[str], references2: list[str], 
                            similarity_threshold: float = 0.6, cleaning_function = None) -> list[tuple]:
    pairwise_references = dict()

    _references1 = references1 if not cleaning_function else cleaning_function(references1)
    _references2 = references2 if not cleaning_function else cleaning_function(references2)

    # this is obviously a suboptimal O(n^2) way to do this, but it should work fine for the size of the dataset
    for reference1 in _references1:
        for reference2 in _references2:
            ratio = Levenshtein.ratio(reference1, reference2)
            if similarity_threshold <= ratio:
                if reference1 not in pairwise_references:
                    pairwise_references[reference1] = [(reference2, ratio)]
                else:
                    pairwise_references[reference1].append((reference2, ratio))

    return pairwise_references


def print_pairwise_references(pairwise_references):
    for decision_reference in pairwise_references:
        print(f"Matches of decision reference \"{decision_reference}\":")
        for factum_reference, ratio in pairwise_references[decision_reference]:
            print(f" -- [Levenshtein ratio {ratio}] \"{factum_reference}\"")
        print()


if __name__ == "__main__":
    for directory in sys.argv[1:]:
        decision_references, factums_references = load_references(directory)
        for factum_name in factums_references:
            print(f"Matching references for {factum_name} factum with its decision (no cleaning of references)...")
            print()
            print_pairwise_references(get_pairwise_references(decision_references, factums_references[factum_name]))
            print()
            print(f"Matching references for {factum_name} factum with its decision (with cleaning of references)...")
            print()
            print_pairwise_references(get_pairwise_references(decision_references, factums_references[factum_name],
                                        cleaning_function=lambda references: list(set([reference.split(',')[0] for reference in references]))))