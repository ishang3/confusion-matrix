

Sample Command:

python confusion.py -gt deep-test-2/test-data/TESTDATA/ -l person -inf deep-test-2/inference-0.5/inf-results/ -t 0.5


Command line arguments:

 parser.add_argument('-gt', '--groundtruthpath', help="Enter ground truth path")
    parser.add_argument('-inf', '--inferencepath', help="Enter inference file path")
    parser.add_argument('-t', '--threshold', help="Threshold for filter", default=0.5)
    parser.add_argument('-l', '--label', help="Which Class to compute for", default='person')
