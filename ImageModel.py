from fastai.vision import *
def input_file():
    with open('input.txt','r') as inputfile:
        dataset_name = inputfile.readline().rstrip()
        print('Dataset name: ', dataset_name)
        n = int(inputfile.readline().rstrip())
        print('Number of image classes: ', n)
        for iclass in range(n):
            img_classes.append(inputfile.readline().rstrip())
            print('Class {}: {}'.format(iclass+1, img_classes[iclass]))
        inputfile.close()
        return dataset_name, n, img_classes 

if __name__ == "__main__":
    #variables
    datast_name = ''
    n = 0
    img_classes = []
    img_urls = {}
    #input
    print('Input section: ')
    dataset_name, n, img_classes = input_file()
    path=Path('dataset/'+dataset_name)
    print()
    #directory
    print('Current directory: ', path.ls())
    print()
    #display data
    print('Displaying data ...')
    np.random.seed(42)
    print('Init ImageDataBunch')
    data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, num_workers=4).normalize(imagenet_stats)
    print('Data classes: ', data.classes)
    print('Length of Training Dataset: ', len(data.train_ds))
    print('Length of Validation Dataset: ', len(data.valid_ds))
    print()
    #train model
    print('Training the model ...')
    print('Define resnet50 CNN learner')
    learn = cnn_learner(data, models.resnet50, metrics=error_rate)
    print('Start training')
    learn.fit_one_cycle(4)
