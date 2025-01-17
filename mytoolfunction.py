import os
import pandas as pd
import numpy as np
import argparse
import time
from datetime import datetime
from sklearn import preprocessing
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split

### 生成列名列表
column_names = ["principal_Component" + str(i) for i in range(1, 79)] + ["Label"]

### 獲取開始or結束時間
def getStartorEndtime(Start_or_End_Str,Start_or_End,fliepath):
    timestamp = time.time()# 用於獲取當前時間的時間戳，返回一個浮點數

    # 將時間戳轉換為日期時間物件
    dt_object = datetime.fromtimestamp(timestamp)
    
    # 格式化日期时间為 "yyyy-mm-dd hh:mm:ss"
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")

    print(f"{Start_or_End}_time: {formatted_time}")
    # 開啟檔案並寫入開始時間
    with open(f"{fliepath}/StartTime_and_Endtime.csv", "a+") as file:
        file.write(f"{Start_or_End_Str}:{str(formatted_time)}\n")

    return timestamp, formatted_time
### 計算花費時間
def CalculateTime(end_IDS, start_IDS):
    #  end_IDS = time.time()
     execution_time = end_IDS - start_IDS
     print(f"Code execution time: {execution_time} seconds")
    
### 檢查資料夾是否存在 回傳True表示沒存在
def CheckFolderExists (folder_name):
    if not os.path.exists(folder_name):
        return True
    else:
        return False
    
### 檢查檔案是否存在
def CheckFileExists (file):
   if os.path.isfile(file):
    print(f"{file} 是一個存在的檔案。")
    return True
   else:
    print(f"{file} 不是一個檔案或不存在。")
    return False
    
### Save data to csv
def SaveDataToCsvfile(df, folder_name, filename):
    # 抓取當前工作目錄名稱
    current_directory = os.getcwd()
    print("當前工作目錄", current_directory)
    # folder_name = filename + "_folder"
    print("資料夾名稱", folder_name)
    folder_name = generatefolder(current_directory + "\\",folder_name)
    csv_filename = os.path.join(current_directory, 
                                folder_name, filename + ".csv")
    print("存檔位置跟檔名", csv_filename)
    df.to_csv(csv_filename, index=False)

### 建立一個資料夾
def generatefolder(fliepath, folder_name):
    if fliepath is None:
        fliepath = os.getcwd()
        print("當前工作目錄", fliepath) 
    
    if folder_name is None:
        folder_name = "my_AnalyseReportfolder"

    file_not_exists  = CheckFolderExists(fliepath +folder_name)
    print("file_not_exists:",file_not_exists)
    # 使用os.path.exists()檢文件夹是否存在
    if file_not_exists:
        # 如果文件夹不存在，就创建它
        os.makedirs(fliepath + folder_name)
        print(f"資料夾 '{fliepath +folder_name}' 創建。")
    else:
        print(f"資料夾 '{fliepath +folder_name}' 已存在，不需再創建。")
        
    return folder_name
### 合併DataFrame成csv
def mergeDataFrameAndSaveToCsv(trainingtype, x_train,y_train, filename, weaklabel, epochs):
    # 创建两个DataFrame分别包含x_train和y_train
    df_x_train = pd.DataFrame(x_train)
    df_y_train = pd.DataFrame(y_train)

    # 使用concat函数将它们合并
    generateNewdata = pd.concat([df_x_train, df_y_train], axis=1)

    # 保存合并后的DataFrame为CSV文件
    if trainingtype == "GAN":
        generateNewdata.columns = column_names
        SaveDataToCsvfile(generateNewdata, f"{trainingtype}_data_{filename}", f"{trainingtype}_data_generate_weaklabel_{weaklabel}_epochs_{epochs}")
    else:
        SaveDataToCsvfile(generateNewdata, f"{filename}_epochs_{epochs}")

def ParseCommandLineArgs(commands):
    
    # e.g
    # python BaseLine.py -h
    # python BaseLine.py --dataset train_half1
    # python BaseLine.py --dataset train_half2
    # python BaseLine.py --epochs 100
    # python BaseLine.py --dataset train_half1 --epochs 100
    # python DoGAN.py --dataset train_half1 --epochs 10 --weaklabel 8
    # default='train_half1'
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='Federated Learning Client')

    # 添加一个参数来选择数据集
    parser.add_argument('--dataset', type=str, choices=['total_train','train_half1', 'train_half2'], default='total_train',
                        help='Choose the dataset for training (total_train or train_half1 or train_half2)')

    # 添加一个参数来设置训练的轮数
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs')

     # 添加一个参数来设置训练的轮数
    parser.add_argument('--weaklabel', type=int, default=8, help='encode of weak label')

    # add load method
    parser.add_argument('--method', type=str, choices=['normal','SMOTE', 'GAN'], default='normal',
                        help='Choose the process method for training (normal or SMOTE or GAN)')
    # 解析命令行参数
    args = parser.parse_args()

    # 根据输入的命令列表来确定返回的参数
    if 'dataset' in commands and 'epochs' in commands and 'method' in commands:
        return args.dataset, args.epochs, args.method
    elif 'dataset' in commands and 'epochs' in commands and 'weaklabel' in commands:
        return args.dataset, args.epochs, args.weaklabel
    elif 'dataset' in commands and 'epochs' in commands:
        return args.dataset, args.epochs
    elif 'dataset' in commands:
        return args.dataset
    elif 'epochs' in commands:
        return args.epochs

# 测试不同的命令
# print(ParseCommandLineArgs(['dataset']))
# print(ParseCommandLineArgs(['epochs']))
# print(ParseCommandLineArgs(['dataset', 'epochs']))
# print(ParseCommandLineArgs(['dataset', 'epochs', 'label']))

### Choose Load np array
def ChooseLoadNpArray(filepath, file, Choose_method):

    if file == 'total_train':
        print("Training with total_train")
        if (Choose_method == 'normal'):
            # x_train = np.load(filepath + "x_train_1.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_1.npy", allow_pickle=True)
            # 20231113 only do labelencode and minmax
            # x_train = np.load(filepath + "x_train_20231113.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_20231113.npy", allow_pickle=True)
            # # 20231114 after 百分百PCAonly do labelencode and minmax
            # x_train = np.load(filepath + "x_train_20231114.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_20231114.npy", allow_pickle=True)
            
            # 20240124 選所有特徵 only do labelencode and minmax
            # x_train = np.load(filepath + "x_train_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_20240124.npy", allow_pickle=True)
			
			#選80個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect80_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect80_20240124.npy", allow_pickle=True)
			
			#選70個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect70_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect70_20240124.npy", allow_pickle=True)
			
			#選60個特徵
            x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect60_20240124.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect60_20240124.npy", allow_pickle=True)
			
			#選55個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect55_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect55_20240124.npy", allow_pickle=True)
			
			#選50個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect50_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect50_20240124.npy", allow_pickle=True)
			
			#選45個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect45_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect45_20240124.npy", allow_pickle=True)
			
			#選40個特徵
            # x_train = np.load(filepath + "x_train_cicids2017_AfterFeatureSelect40_20240124.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_cicids2017_AfterFeatureSelect40_20240124.npy", allow_pickle=True)
            
            # 20240125 PCA only do labelencode and minmax
            #PCA選77個特徵 84特徵=77+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA77_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA77_20240125.npy", allow_pickle=True)
            #PCA選73個特徵 80特徵=73+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA73_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA73_20240125.npy", allow_pickle=True)
            # #PCA選63個特徵 70特徵=63+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA63_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA63_20240125.npy", allow_pickle=True)
            # #PCA選53個特徵 60特徵=53+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA53_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA53_20240125.npy", allow_pickle=True)
            # #PCA選43個特徵 50特徵=43+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA43_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA43_20240125.npy", allow_pickle=True)
            # #PCA選38個特徵 45特徵=38+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA38_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA38_20240125.npy", allow_pickle=True)
            # #PCA選33個特徵 40特徵=33+扣掉'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'Protocol', 'Timestamp' 'Label'
            # x_train = np.load(filepath + "x_train_AfterPCA33_20240125.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_AfterPCA33_20240125.npy", allow_pickle=True)
        elif (Choose_method == 'SMOTE'):
            # x_train = np.load(filepath + "x_total_train_SMOTE_ALL_Label.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_total_train_SMOTE_ALL_Label.npy", allow_pickle=True)
            # x_train = np.load(filepath + "x_total_train_SMOTE_ALL_Label14.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_total_train_SMOTE_ALL_Label14.npy", allow_pickle=True)
            x_train = np.load(filepath + "x_train_half1_20231114.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half1_20231114.npy", allow_pickle=True)
            
        elif (Choose_method == 'GAN'):
            # x_train = np.load(filepath + "x_GAN_data_total_train_weakpoint_14.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_GAN_data_total_train_weakpoint_14.npy", allow_pickle=True)
            x_train = np.load(filepath + "x_train_20231106_afterGAN_Label14.npy", allow_pickle=True)
            # 將複數的資料實部保留並轉換為浮點：
            x_train = x_train.real.astype(np.float64)
            y_train = np.load(filepath + "y_train_20231106_afterGAN_Label14.npy", allow_pickle=True)
        
        client_str = "BaseLine"
        print(Choose_method)

    elif file == 'train_half1':
        if (Choose_method == 'normal'):
            # 20231113 only do labelencode and minmax
            # x_train = np.load(filepath + "x_train_half1_20231113.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_20231113.npy", allow_pickle=True)

            # # 20231114 after 百分百PCAonly do labelencode and minmax
            x_train = np.load(filepath + "x_train_half1_20231114.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half1_20231114.npy", allow_pickle=True)

            # # 20231204 after SMOTE
            # x_train = np.load(filepath + "x_train_half1_AfterSMOTEspilt_20231204.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_AfterSMOTEspilt_20231204.npy", allow_pickle=True)
        elif (Choose_method == 'SMOTE'):
            # #20231121 SMOTE Label 9 1000
            # x_train = np.load(filepath + "x_train_half1_SMOTE_Label_9.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_SMOTE_Label_9.npy", allow_pickle=True)
            # #20231127 SMOTE Lable8 1000 and Label 9 1000
            # x_train = np.load(filepath + "x_train_half1_SMOTE_Label8_and_Label9_20231127.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_SMOTE_Label8_and_Label9_20231127.npy", allow_pickle=True)
            # 20231129 SMOTE Lable8 1000 and Label 9 1000 k=1
            # x_train = np.load(filepath + "x_train_half1_SMOTE_Label8_and_Label9_20231129.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_SMOTE_Label8_and_Label9_20231129.npy", allow_pickle=True)
            # 20231130 borderLineSMOTE1 Lable8 k=2 1000 and Label 9 k=5 M = 10 1000
            # x_train = np.load(filepath + "x_train_half1_BorederlineSMOTE_Label8_and_Label9_20231130.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_BorederlineSMOTE_Label8_and_Label9_20231130.npy", allow_pickle=True)
            # 20231201 SMOTE Lable8 k=2  and Label 9 k=5 Label 9 Label13 k=4  2000
            # x_train = np.load(filepath + "x_train_half1_SMOTE_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_SMOTE_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # 20231201 borderLineSMOTE1 Lable8 k=2  and Label 9 k=5 Label 9 Label13 k=4 M = 10 2000
            # x_train = np.load(filepath + "x_train_half1_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # # 20231201 borderLineSMOTE2 Lable8 k=2 and Label 9 k=5 Label 9 Label13 k=4 M = 10 2000
            # x_train = np.load(filepath + "x_train_half1_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # # 20231204 borderLineSMOTE1 Lable8 k=5 and Label 9 k=5 Label 9 Label13 k=5 M = 10 2000 after SMOTE orignal 兩倍
            # x_train = np.load(filepath + "x_train_half1_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half1_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            # # 20231204 borderLineSMOTE2 Lable8 k=5 and Label 9 k=5 Label 9 Label13 k=5 M = 10 2000 after SMOTE orignal 兩倍
            x_train = np.load(filepath + "x_train_half1_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half1_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
        elif (Choose_method == 'GAN'):
            # 20231114 after 百分百PCAonly do labelencode and minmax
            x_train = np.load(filepath + "x_train_half1_20231114.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half1_20231114.npy", allow_pickle=True)
        print("train_half1 x_train 的形狀:", x_train.shape)
        print("train_half1 y_train 的形狀:", y_train.shape)
        client_str = "client1"
        print("使用 train_half1 進行訓練")
    elif file == 'train_half2':
        if (Choose_method == 'normal'):
            # 20231113 only do labelencode and minmax
            # x_train = np.load(filepath + "x_train_half2_20231113.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_20231113.npy", allow_pickle=True)
            # 20231114 after 百分百PCAonly do labelencode and minmax
            # x_train = np.load(filepath + "x_train_half2_20231114.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_20231114.npy", allow_pickle=True)

            # # 20231204 after SMOTE
            # x_train = np.load(filepath + "x_train_half2_AfterSMOTEspilt_20231204.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_AfterSMOTEspilt_20231204.npy", allow_pickle=True)

            # # 20231204 after SMOTE
            x_train = np.load(filepath + "x_train_half2_AfterSMOTEspilt_20231204.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half2_AfterSMOTEspilt_20231204.npy", allow_pickle=True)
        elif (Choose_method == 'SMOTE'):
            # #20231121 BorderLineSMOTE1 Label 9 1000
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_Label_9.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_Label_9.npy", allow_pickle=True)
            # #20231122 BorderLineSMOTE1 Label 9 1000 k_neighbors=1 m_neighbors =2
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_Label_9_20231122.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_Label_9_20231122.npy", allow_pickle=True)
            # 20231127 BorderLineSMOTE1 Lable and Label 9 1000 k_neighbors=1 m_neighbors =5
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_Label8_and_Label9_20231127.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_Label8_and_Label9_20231127.npy", allow_pickle=True)
            # 20231129 BorderLineSMOTE1 Lable and Label 9 1000 k_neighbors=1 m_neighbors =5
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_Label8_and_Label9_20231129.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_Label8_and_Label9_20231129.npy", allow_pickle=True)
            # 20231130 borderLineSMOTE1 Lable8 k=2 1000 and Label 9 k=5 M = 10 1000
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_Label8_and_Label9_20231130.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_Label8_and_Label9_20231130.npy", allow_pickle=True)
            # 20231201 SMOTE Lable8 k=2 and Label 9 k=5 Label 13 k=4 2000
            # x_train = np.load(filepath + "x_train_half2_SMOTE_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_SMOTE_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # 20231201 borderLineSMOTE1 Lable8 k=2 and Label 9 k=5 Label 13 k=4 M = 10 2000
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # # 20231201 borderLineSMOTE2 Lable8 k=2 and Label 9 k=5 Label 13 k=4 M = 10 2000
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231201.npy", allow_pickle=True)
            # # 20231204 borderLineSMOTE1 Lable8 k=5 and Label 9 k=5 Label 9 Label13 k=5 M = 10 2000 after SMOTE orignal 兩倍
            # x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_borderline-1_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            # # 20231204 borderLineSMOTE2 Lable8 k=5 and Label 9 k=5 Label 9 Label13 k=5 M = 10 2000 after SMOTE orignal 兩倍
            x_train = np.load(filepath + "x_train_half2_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half2_BorederlineSMOTE_borderline-2_Label8_and_Label9_Label13_20231204.npy", allow_pickle=True)
        elif (Choose_method == 'GAN'):
            # 20231114 after 百分百PCAonly do labelencode and minmax
            x_train = np.load(filepath + "x_train_half2_20231114.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_train_half2_20231114.npy", allow_pickle=True)
        print("train_half2 x_train 的形狀:", x_train.shape)
        print("train_half2 y_train 的形狀:", y_train.shape)
        client_str = "client2"
        print("使用 train_half2 進行訓練")

    print("use file", file)
    return x_train, y_train,client_str

# for do one hot
def ChooseTrainDatastes(filepath, my_command,Choose_method):
    # 加载选择的数据集
    
    if my_command == 'total_train':
        if (Choose_method == 'normal'):
            # print("Training with total_train")
            # train_dataframe = pd.read_csv(os.path.join(filepath, 'data', 'train_dataframes_respilt.csv'))
            # x_train = np.array(train_dataframe.iloc[:, :-1])
            # y_train = np.array(train_dataframe.iloc[:, -1])
            dftrain = pd.read_csv(filepath + "data\\dataset_AfterProcessed\\20231113\\train_dataframes_20231113.csv")

            #特徵    
            x_columns = dftrain.columns.drop(dftrain.filter(like='Label_').columns)
            x_train = dftrain[x_columns].values.astype('float32')
            y_train = dftrain.filter(like='Label_').values.astype('float32')
            # 找到每一行中值為 1 的索引
            label_indices = np.argmax(y_train, axis=1)
            # 將 label_indices 賦值給 y_train，這樣 y_train 就包含了整數表示的標籤
            y_train = label_indices
           
        elif (Choose_method == 'SMOTE'):
            # x_train = np.load(filepath + "x_total_train_SMOTE_ALL_Label.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_total_train_SMOTE_ALL_Label.npy", allow_pickle=True)
            x_train = np.load(filepath + "x_total_train_SMOTE_ALL_Label14.npy", allow_pickle=True)
            y_train = np.load(filepath + "y_total_train_SMOTE_ALL_Label14.npy", allow_pickle=True)
            
        elif (Choose_method == 'GAN'):
            # x_train = np.load(filepath + "x_total_train.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_total_train.npy", allow_pickle=True)
            # x_train = np.load(filepath + "x_GAN_data_total_train_weakpoint_14.npy", allow_pickle=True)
            # y_train = np.load(filepath + "y_GAN_data_total_train_weakpoint_14.npy", allow_pickle=True)
            x_train = np.load(filepath + "x_train_20231106_afterGAN_Label14.npy", allow_pickle=True)
            # 將複數的資料實部保留並轉換為浮點：
            x_train = x_train.real.astype(np.float64)
            y_train = np.load(filepath + "y_train_20231106_afterGAN_Label14.npy", allow_pickle=True)
        client_str = "BaseLine"

    elif my_command == 'train_half1':
        print("Training with train_half1")
        dftrain = pd.read_csv(filepath + "data\\dataset_AfterProcessed\\20231113\\train_half1_20231113.csv")

        #特徵    
        x_columns = dftrain.columns.drop(dftrain.filter(like='Label_').columns)
        x_train = dftrain[x_columns].values.astype('float32')
        y_train = dftrain.filter(like='Label_').values.astype('float32')
        # 找到每一行中值為 1 的索引
        label_indices = np.argmax(y_train, axis=1)
        # 將 label_indices 賦值給 y_train，這樣 y_train 就包含了整數表示的標籤
        y_train = label_indices
        client_str = "client1"
        
    elif my_command == 'train_half2':
        print("Training with train_half2")
        print("Training with train_half1")
        dftrain = pd.read_csv(filepath + "data\\dataset_AfterProcessed\\20231113\\train_half2_20231113.csv")
        #特徵    
        x_columns = dftrain.columns.drop(dftrain.filter(like='Label_').columns)
        x_train = dftrain[x_columns].values.astype('float32')
        y_train = dftrain.filter(like='Label_').values.astype('float32')
        # 找到每一行中值為 1 的索引
        label_indices = np.argmax(y_train, axis=1)
        # 將 label_indices 賦值給 y_train，這樣 y_train 就包含了整數表示的標籤
        y_train = label_indices
        client_str = "client2"
        
    # 返回所需的數據或其他變量
    return x_train, y_train, client_str


def ChooseTestDataSet(filepath):
    # test_dataframe = pd.read_csv(os.path.join(filepath, 'data', 'test_dataframes.csv'))
    # x_test = np.array(test_dataframe.iloc[:, :-1])
    # y_test = np.array(test_dataframe.iloc[:, -1])
    dftest = pd.read_csv(filepath + "data\\dataset_AfterProcessed\\20231113\\test_dataframes_20231113.csv")
    #x_columns作用就是丟掉Label_開頭 也就是等於特徵    
    x_columns = dftest.columns.drop(dftest.filter(like='Label_').columns)
    x_test = dftest[x_columns].values.astype('float32')
    y_test = dftest.filter(like='Label_').values.astype('float32')
    # 找到每一行中值為 1 的索引
    label_indices = np.argmax(y_test, axis=1)
    # 將 label_indices 賦值給 y_train，這樣 y_train 就包含了整數表示的標籤
    y_test = label_indices
    
    return x_test, y_test

### sava dataframe to np array 
def SaveDataframeTonpArray(dataframe, filepath ,df_name, filename):
    #選擇了最后一列Lable之外的所有列，即選擇所有feature
    x = np.array(dataframe.iloc[:,:-1])
    y = np.array(dataframe.iloc[:,-1])

    #np.save
    np.save(f"{filepath}\\x_{df_name}_{filename}.npy", x)
    np.save(f"{filepath}\\y_{df_name}_{filename}.npy", y)

### find找到datasets中是string的行
def findStringCloumn(dataFrame):
        string_columns = dataFrame.select_dtypes(include=['object'])
        for column in string_columns.columns:
            print(f"{dataFrame} 中type為 'object' 的列: {column}")
            print(string_columns[column].value_counts())
            print("\n")

### check train_df_half1 and train_df_half2 dont have duplicate data
def CheckDuplicate(dataFrame1, dataFrame2):
    intersection = len(set(dataFrame1.index) & set(dataFrame2.index))
    print(f"{dataFrame1} 和 {dataFrame2} 的index交集数量:", intersection)
    print(f"{dataFrame1} 和 {dataFrame2}是否相同:", dataFrame1.equals(dataFrame2))
    
### print dataset information 
def printFeatureCountAndLabelCountInfo(dataFrame1, dataFrame2):
     # 計算feature數量
    num_features_dataFrame1 = dataFrame1.shape[1] - 1
    num_features_dataFrame2 = dataFrame2.shape[1] - 1 
     # 計算Label數量
    label_counts = dataFrame1['Label'].value_counts()
    label_counts2 = dataFrame2['Label'].value_counts()

    print(f"{str(dataFrame1)} 的feature:", num_features_dataFrame1)
    print(f"{str(dataFrame1)} 的label數:", len(label_counts))
    print(f"{str(dataFrame1)} 的除了最後一列Label列之外的所有列,即選擇feature數:\n", dataFrame1.iloc[:,:-1])
    findStringCloumn(dataFrame1)

    print(f"{str(dataFrame2)} 的feature:", num_features_dataFrame2)
    print(f"{str(dataFrame2)} 的label數:", len(label_counts2))
    print(f"{str(dataFrame2)} 的除了最後一列Label列之外的所有列,即選擇feature數:\n", dataFrame2.iloc[:,:-1])
    findStringCloumn(dataFrame2)

    CheckDuplicate(dataFrame1, dataFrame2)

### label encoding
# def label_Encoding(label):
#     label_encoder = preprocessing.LabelEncoder()
#     mergecompelete_dataset[label] = label_encoder.fit_transform(mergecompelete_dataset[label])
#     mergecompelete_dataset[label].unique()

def label_Encoding(label,df):
    label_encoder = preprocessing.LabelEncoder()
    df[label] = label_encoder.fit_transform(df[label])
    df[label].unique()
    print(f"{label}",df[label].unique())


# ##  清除CIC-IDS-2017 資料集中的dirty data，包含NaN、Infinity、包含空白或小于ASCII 32的字符
def clearDirtyData(df):
    # 檢查第一列featurea名稱是否包含空白或是小于ASCII 32的字元
    first_column = df.columns[0]
    is_dirty = first_column.isspace() or ord(first_column[0]) < 32

    # 將"inf"值替換為NaN
    df.replace("inf", np.nan, inplace=True)

    # 找到包含NaN、Infinity和"inf"值的行，並將其index添加到dropList
    nan_inf_rows = df[df.isin([np.nan, np.inf, -np.inf]).any(axis=1)].index.tolist()

    # 將第一列featurea名稱所在的index添加到dropList
    if is_dirty:
        nan_inf_rows.append(0)

    # 去重dropList中的index
    dropList = list(set(nan_inf_rows))

    # 刪除包含dirty data的行
    df_clean = df.drop(dropList)

    return df_clean

### for sorting the labeled data based on support
def sortingFunction(data):
    return data.shape[0]

# 使用分層劃分資料集 平均劃分資料集 
def splitdatasetbalancehalf(train_dataframes):
    stratified_split = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=42)
    for train_indices, test_indices in stratified_split.split(train_dataframes, train_dataframes['Label']):
        df1 = train_dataframes.iloc[train_indices]
        df2 = train_dataframes.iloc[test_indices]
        label_counts = df1['Label'].value_counts()
        label_counts2 = df2['Label'].value_counts()
        print("train_half1\n",label_counts)
        print("train_half2\n",label_counts2)

    return df1,df2

def spiltweakLabelbalance(weakLabel,original_dataset,size):
    label_data = original_dataset[original_dataset['Label'] == weakLabel]
    # 使用train_test_split分別劃分取Label相等8、9、13、14的數據
    train_label, test_label = train_test_split(label_data, test_size=size, random_state=42)
    return train_label, test_label

def spiltweakLabelbalance_afterOnehot(weak_label, original_dataset,size):

    weak_label_data = original_dataset[weak_label]
    # e.g:找到做完one hot Label_8 列中值等于1的行
    weak_label_data_equals_1_rows = original_dataset[weak_label_data == 1]
    weak_label_train, weak_label_test = train_test_split(weak_label_data_equals_1_rows, test_size=size, random_state=42)
    
    return weak_label_train, weak_label_test

## 將結合weakLabel Label8 的train_half1轉成np array
# gan_dataframe = pd.read_csv("D:\\Labtest20230911\\GAN_data_train_half1\\GAN_data_train_half1_ADD_weakLabel_8.csv")
# SaveDataframeTonpArray(gan_dataframe, "train_half1","weakpoint_8")
# gan_dataframe = pd.read_csv("D:\\Labtest20230911\\GAN_data_total_train\\GAN_data_total_train_ADD_weakLabel_14.csv")
# # # gan_dataframe = pd.read_csv("D:\\Labtest20230911\\GAN_data_train_half1\\GAN_data_train_half1_ADD_weakLabel_9.csv")
# SaveDataframeTonpArray(gan_dataframe, "GAN_data_total_train","weakpoint_14")
### DestinationPort拉出來到mytoolfunction.py單獨從做一次
# df = pd.read_csv("D:\\Labtest20230911\\data\\total_encoded_updated.csv")
# df['DestinationPort'] = df['DestinationPort'].astype(str)


# label_Encoding('DestinationPort',df)
# SaveDataToCsvfile(df, "./data", "total_encoded_updated_20231101")

############################################################# other
# # 命令行參數解析器
# parser = argparse.ArgumentParser(description='Federated Learning Client')

# # 添加一個參數來選擇數據集
# parser.add_argument('--dataset', type=str, choices=['train_half1', 'train_half2'], default='train_half1',
#                     help='選擇訓練數據集 (train_half1 或 train_half2)')

# args = parser.parse_args()

# # 根據命令行參數選擇數據集
# my_command = args.dataset
# # python BaseLine.py --dataset train_half1
# # python BaseLine.py --dataset train_half2

# # 載入選擇的數據集
# if my_command == 'train_half1':
#     # x_train = np.load(filepath + "x_train_half1.npy", allow_pickle=True)
#     # y_train = np.load(filepath + "y_train_half1.npy", allow_pickle=True)
#     x_train = np.load(filepath + "x_train_half1_weakpoint_8.npy", allow_pickle=True)
#     y_train = np.load(filepath + "y_train_half1_weakpoint_8.npy", allow_pickle=True)
#     client_str = "client1"
#     print("使用 train_half1 進行訓練")
# elif my_command == 'train_half2':
#     x_train = np.load(filepath + "x_train_half2.npy", allow_pickle=True)
#     y_train = np.load(filepath + "y_train_half2.npy", allow_pickle=True)
#     client_str = "client2"
#     print("使用 train_half2 進行訓練")

# test time function
# start_IDS = getStartorEndtime("start")
# # 暫停程式執行 5 秒
# time.sleep(10) #sleep 以秒為單位
# end_IDS = getStartorEndtime("end")
# CalculateTime(end_IDS, start_IDS)


### 添加图例
# # 绘制原始数据集
# plt.scatter(x_train[:, 0], x_train[:, 1], c='red', label='Original Data')

# # 绘制SMOTE采样后的数据集
# plt.scatter(X_resampled[:, 0], X_resampled[:, 1], c='blue', marker='x', s=100, label='SMOTE Samples')


# plt.legend()
# plt.show()

# 找到SMOTE采样后的数据中Label 13的索引


# desired_sample_count = 500

# # 对Label14进行SMOTE
# sampling_strategy_label14 = {14: desired_sample_count}
# oversample_label14 = SMOTE(sampling_strategy=sampling_strategy_label14, k_neighbors=k_neighbors, random_state=42)
# X_resampled_label14, y_resampled_label14 = oversample_label14.fit_resample(x_train, y_train)

# # 对Label9进行SMOTE
# sampling_strategy_label9 = {9: desired_sample_count}
# oversample_label9 = SMOTE(sampling_strategy=sampling_strategy_label9, k_neighbors=k_neighbors, random_state=42)
# X_resampled_label9, y_resampled_label9 = oversample_label9.fit_resample(x_train, y_train)

# # 对Label13进行SMOTE
# sampling_strategy_label13 = {13: desired_sample_count}
# oversample_label13 = SMOTE(sampling_strategy=sampling_strategy_label13, k_neighbors=k_neighbors, random_state=42)
# X_resampled_label13, y_resampled_label13 = oversample_label13.fit_resample(x_train, y_train)

# # 对Label8进行SMOTE
# sampling_strategy_label8 = {8: desired_sample_count}
# oversample_label8 = SMOTE(sampling_strategy=sampling_strategy_label8, k_neighbors=k_neighbors, random_state=42)
# X_resampled_label8, y_resampled_label8 = oversample_label8.fit_resample(x_train, y_train)