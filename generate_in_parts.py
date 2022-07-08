import math
import os
import math
import uuid
import threading
import shutil

data_folder = '../new'
xml_folder = "../xml2"
tf_record_batch_size = 100
tfrecord_output_dir = 'records'


try:
    os.mkdir(tfrecord_output_dir)
except:
    pass


files = os.listdir(data_folder)


# filtered files 
new_files = []
for file in files:
    if file.endswith('.jpg') or file.endswith('.png'):
        new_files.append(file)

loop_times = math.ceil(len(new_files) / tf_record_batch_size)



def GenerateTF(batch,data_folder,new_folder,count):
    
    for file in batch:
        start_path = data_folder + '/' + file
        end_path = new_folder + '/' + file
        # os.rename(start_path, end_path)
        shutil.copy(start_path, end_path)

        # locate the xml file precent in the new folder
        xml_file = file.replace('.jpg', '.xml').replace('.png', '.xml')
        start_path = xml_folder + '/' + xml_file
        end_path = new_folder + '/' + xml_file
        shutil.copy(start_path, end_path)
    paths = {
        "IMAGE_PATH": os.path.abspath( os.path.curdir),
        "ANNOTATION_PATH": os.path.abspath('records'),
    }
    files = {
        "LABELMAP": os.path.abspath('label_map.pbtxt'),
        "TF_RECORD_SCRIPT": "generate_tfrecord.py"
    }
    command = (
        f"python {files['TF_RECORD_SCRIPT']} -x {os.path.join(paths['IMAGE_PATH'], new_folder)} -l {files['LABELMAP']} -o {os.path.join(paths['ANNOTATION_PATH'], 'train_' + str(count) +'.record')}"
    )
    os.system(command)
    # delete the new folder
    shutil.rmtree(new_folder)

my_threads = []

for x in range(loop_times):
    start = x * tf_record_batch_size
    end = (x + 1) * tf_record_batch_size
    batch = new_files[start:end]

    # make new folder
    new_folder = 'temp/' + str(uuid.uuid4())
    # recursive mkdir
    os.makedirs(new_folder)

    # move all the files from batch to temp folder
    thread = threading.Thread(target=GenerateTF, args=(batch,data_folder,new_folder,x))
    my_threads.append(thread)

for thread in my_threads:
    thread.start()
    thread.join()
