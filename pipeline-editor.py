
record_path = "train_0.record"
label_map_path = "label_map.pbtxt"


file = open('pipeline.config','r')
data = file.read()
file.close()

start = data.split('train_input_reader')[0]
start2 = data.split('train_input_reader')[1]

middle = """train_input_reader {{
  label_map_path: "{}"
  tf_record_input_reader {{
    input_path: "{}"
  }}
}}
""".format(label_map_path, record_path)


end = "\n".join(start2.split('\n')[6:])

data = start + middle + end

start = data.split('eval_input_reader')[0]
start2 = data.split('eval_input_reader')[1]

middle = """eval_input_reader {{
  label_map_path: "{}"
  shuffle: false
  num_epochs: 1
  tf_record_input_reader {{
    input_path: "{}"
  }}
}}

""".format(label_map_path, record_path)


# end = "\n".join(start2.split('\n')[8:])
end = ""

data = start + middle + end




file = open('newpipeline.config','w')
file.write(
    data
)
file.close()