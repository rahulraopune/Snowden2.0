import argparse
import json
from nltk.translate.bleu_score import sentence_bleu
from nltk import word_tokenize

def main():
    with open(args.true, "r") as f:
        true_data = json.load(f)
    with open(args.predictions, "r") as f:
        pred_data = json.load(f)

    # Unpack all sentences into a dict where the id is the key
    # and the value the text of the sentence
    true_ids = []
    true_conclusions = []
    for item in true_data:
        true_ids.append(item["id"])
        true_conclusions.append(item["conclusion"])

    pred_conclusions = [pred_data[str(i)] for i in true_ids]


    pred_conclusions = [word_tokenize(c) for c in pred_conclusions]
    true_conclusions = [[word_tokenize(c)] for c in true_conclusions]

    # Calculate actual score
    bleu1_score =  sum([sentence_bleu(true_c, pred_c, weights=(1,0,0,0)) for true_c, pred_c in zip(true_conclusions, pred_conclusions)])/len(true_conclusions)
    bleu2_score =  sum([sentence_bleu(true_c, pred_c, weights=(0,1,0,0)) for true_c, pred_c in zip(true_conclusions, pred_conclusions)])/len(true_conclusions)
    bleu_score  =  sum([sentence_bleu(true_c, pred_c) for true_c, pred_c in zip(true_conclusions, pred_conclusions)])/len(true_conclusions)

    print('BLEU-1: {}, BLEU-2: {}, BLEU:{}'.format(bleu1_score, bleu2_score, bleu_score))

if __name__ == "__main__":
    # Add cli parameters
    parser = argparse.ArgumentParser("Script to evaluate the predictions on a test set.")

    parser.add_argument(
        "--true",
        "-t",
        required=True,
        help="Path to the test data file containing the true conclusions.",
        metavar="TEST_DATA")
    parser.add_argument(
        "--predictions",
        "-p",
        required=True,
        help="Path to the predictions file in the specified format.",
        metavar="PREDICTIONS")

    args = parser.parse_args()

    main()

    print("Done.")
