from main import main

if __name__ == '__main__':
    # You should not modify this part.
    import argparse
    import csv

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()

    print('args.testing:',args.training)
    print('args.testing:',args.testing)

    output = main(train = args.training, test = args.testing)

    with open(args.output, 'w', newline = '', encoding = 'utf-8') as w:
        writer = csv.writer(w)
        for i in output:
            writer.writerow([i])
