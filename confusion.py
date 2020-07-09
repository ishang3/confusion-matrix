import os
from os import listdir
import shutil
import argparse

def ret_data(path,label,inference=False,threshold=0.5):
    """
    path: path to the kitti files
    label: which class to return all predicted / ground
            truth data from

    This function will return all the predictions from either
    the ground truth file or inferences
    """

    output = {}
    for file in listdir(path):
        if file.split('.')[-1] == 'txt':
            fullpath = path + file
            kitti_ant = open(fullpath, 'r')
            label_total = 0
            for line in kitti_ant:
                item_list = line.strip().split(' ')
                if not inference:
                    if item_list[0] == label:
                        label_total += 1
                if inference:
                    if item_list[0] == label and float(item_list[-1]) > threshold:
                        label_total += 1


            output[file] = label_total

    return output


def process(data_gt,data_inf):
    """
    This will go through the inference and ground truth
    to calculate the true positive rate and false positive rate

    Total Positives = True Positives + False Negatives
    Total Negatives = True Negatives + False Positives


    """
    total_positives = 0
    false_positives_cum = 0
    false_negatives_cum = 0
    true_negatives_cum = 0

    for file in data_gt:
        if data_gt[file] == 0:
            print('true negative')
        total_positives += data_gt[file] #getting the true positives
        try:
            #true positives - predicted
            difference = data_gt[file]- data_inf[file]
            # print(difference)
            if difference < 0:
                false_positives_cum += abs(difference) #less then 0 means false positives
            if difference > 0:
                false_negatives_cum += abs(difference) #greater then 0 means false negative
        except:
            pass

    #True Positives = Total Positives - False Negatives
    true_positives = total_positives - false_negatives_cum

    #True Negatives = Total Negatives - False Positves

    # print(total_positives,'TOTAL POSITIVES')
    # print(true_positives,'true_positives_cum')
    # print(false_positives_cum,'false_positives_cum')
    # print(false_negatives_cum,'false_negatives_cum')
    # print(true_negatives_cum,'true_negatives_cum')

    #great article explaining it: https://medium.com/@klintcho/explaining-precision-and-recall-c770eb9c69e9
    #https://towardsdatascience.com/decoding-the-confusion-matrix-bb4801decbb


    #Precision = True Positives / (True Positives + False Positives)
    PRECISION = true_positives / (true_positives + false_positives_cum)

    #Recall = True Positives / (True Positives + False Negatives)
    RECALL = true_positives / (true_positives + false_negatives_cum)

    print(PRECISION,RECALL)

    #high precisions means that our positive cases are being classified as positive
    #whereas low recall means most p
    #high recall means no positive sample will be classified as negative

if __name__ == '__main__':

    #command line arguments;
    # threshold; ground_truth_data_path; label; inference_data_path

    parser = argparse.ArgumentParser()

    parser.add_argument('-gt', '--groundtruthpath', help="Enter ground truth path")
    parser.add_argument('-inf', '--inferencepath', help="Enter inference file path")
    parser.add_argument('-t', '--threshold', help="Threshold for filter", default=0.5)
    parser.add_argument('-l', '--label', help="Which Class to compute for", default='person')

    args = parser.parse_args()

    ground_truth = ret_data(args.groundtruthpath,args.label,False)
    inference = ret_data(args.inferencepath,args.label,True,threshold=float(args.threshold))
    

    process(ground_truth,inference)