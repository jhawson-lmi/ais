import pathlib
import shutil
import random
import argparse
import logging
import datetime


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_class_dirs(data_dir, out_dir, split_ratio):
    path = pathlib.Path(data_dir)
    classes = [x for x in path.iterdir() if x.is_dir()]
    logger.info(f'found classes: {[x.name for x in classes]}')
    out_dir = pathlib.Path(out_dir)
    for class_dir in classes:
        files = [x for x in class_dir.rglob('*.jpg')] + [x for x in class_dir.rglob('*.png')]
        random.shuffle(files)
        split_index = int(len(files) * split_ratio)
        
        for subset in ['train', 'test']:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            subset_dir = out_dir / subset / class_dir.name / date
            subset_dir.mkdir(exist_ok=True)
            if subset == 'train':
                for file in files[:split_index]:
                    shutil.copy(str(file), str(subset_dir))
            else:
                for file in files[split_index:]:
                    shutil.copy(str(file), str(subset_dir))
                    
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir','-i', type=str, required=True, help='Path to the directory containing class sub-directories')
    parser.add_argument('--output_dir','-o', type=str, required=True)
    parser.add_argument('--split_ratio', type=float, default=0.9, help='Ratio of train data')
    args = parser.parse_args()
    create_class_dirs(args.input_dir, args.output_dir, args.split_ratio)