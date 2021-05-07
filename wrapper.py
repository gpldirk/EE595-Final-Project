import os

# switch working dir
# cd ./C++
os.chdir("./C++")

# run make to compile c++ code
os.system('make')

# run ./main to run c++ code to preprocess data
os.system('./main')

# switch working dir
# cd ../Python
os.chdir('../Python')

# run python3 main_dqn_layer1.py ro start dqn network
os.system('python3 main_ddqn.py')
