import sys
import glob
from pathlib import Path
from io import TextIOWrapper
# TODO: use this one?
# from difflib import SequenceMatcher
import Levenshtein


def process_lines(fp: TextIOWrapper):
    return [*dict.fromkeys([line.lstrip().rstrip() for line in fp])]


def load_references(directory: str):
    with open(f"{directory}/decision.references.txt") as fp:
        decision_references = process_lines(fp)
    factums_references = dict()
    for factum_references_filename in glob.glob(f"{directory}/interveners/*.references.txt"):
        with open(factum_references_filename) as fp:
            factums_references[Path(factum_references_filename).name.split('.')[0]] = process_lines(fp)
    return decision_references, factums_references


def get_pairwise_references(references1: list[str], references2: list[str], 
                            similarity_threshold: float = 0.6) -> dict:
    pairwise_references = {reference1: [] for reference1 in references1}
    # this is obviously a suboptimal O(n^2) way to do this, but it should work fine for the size of the dataset
    for reference1 in references1:
        for reference2 in references2:
            similarity = Levenshtein.ratio(reference1, reference2, 
                                           processor = lambda reference : reference.lower())
            if similarity_threshold <= similarity:
                pairwise_references[reference1].append((reference2, similarity))

    return pairwise_references


def output_reference_analysis(pairwise_references, fp: TextIOWrapper = None):
    analysis_string = ''
    for factum_reference in pairwise_references:
        analysis_string += f"Matches in the decision of factum reference \"{factum_reference}\":\n"
        if len(pairwise_references[factum_reference]) == 0:
            analysis_string += "NONE"
        else:
            analysis_string += '\n'.join([f" -- \"{factum_reference}\" [Levenshtein ratio {ratio}]" 
                                        for factum_reference, ratio in pairwise_references[factum_reference]])
        analysis_string += "\n\n"
    analysis_string += '\n--------------------------------------------------------------------------\n\n\n'
    
    factum_references_missing_in_decision = [factum_reference for factum_reference in pairwise_references
                                             if len(pairwise_references[factum_reference]) == 0]
    analysis_string += f"The {len(factum_references_missing_in_decision)} factum references that have no match in the decision:\n"
    analysis_string += '\n'.join([f" -- \"{factum_reference}\"" 
                                        for factum_reference in factum_references_missing_in_decision])
    if fp:
        print(f'Writing results to file {fp.name}')
        fp.write(analysis_string)
    else:
        print(analysis_string)


if __name__ == "__main__":
    for directory in sys.argv[1:]:
        decision_references, factums_references = load_references(directory)
        for factum_name in factums_references:
            print(f"Matching references for {factum_name} factum with its decision (no cleaning of references)...")
            pairwise_references = get_pairwise_references(factums_references[factum_name], decision_references)
            with open(f'./results/reference-analysis/{factum_name}-reference-analysis.txt', 'w') as fp: 
                output_reference_analysis(pairwise_references, fp)
            
            # TODO: with cleaning? this is the cleaning lambda
            # lambda references: list(set([reference.split(',')[0] for reference in references]))